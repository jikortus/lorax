#!/bin/bash
# Note: execute this file from the project root directory

set -e

. /usr/share/beakerlib/beakerlib.sh
. $(dirname $0)/lib/lib.sh

CLI="${CLI:-./src/bin/composer-cli}"

rlJournalStart
    rlPhaseStartSetup
        repodir_backup=$(mktemp -d composerrepos-XXXXX)
        composer_stop
        rlRun -t -c "mv /var/lib/lorax/composer/repos.d/* $repodir_backup"
    rlPhaseEnd

    rlPhaseStartTest "Run lorax-composer with --no-system-repos option and empty repos.d"
        composer_start --no-system-repos

        # check that there are no composer repos available
        rlRun -t -c "$CLI sources list | grep -v '^$' | wc -l | grep '^0$'"
        present_repos=$(ls /var/lib/lorax/composer/repos.d)
        if [ -z "$present_repos" ]; then
            rlPass "No repos found in repos.d"
        else
            rlFail "The following repos were found in repos.d: $present_repos"
        fi

        # starting a compose without available repos should fail due to a depsolving error
        rlRun -t -c "tmp_output='$($CLI compose start example-http-server partitioned-disk 2>&1)'"
        rlRun -t -c "echo '$tmp_output' | grep -q 'Problem depsolving example-http-server:'"
        MANUAL=1 composer_stop
    rlPhaseEnd

    rlPhaseStartTest "Run lorax-composer with --no-system-repos and manually created content in repos.d"
        RHEL_VERSION=$(. /etc/os-release; echo $VERSION_ID)
        if grep -qE "https?://.*/nightly/" /etc/yum.repos.d/*; then
            RELEASE_TYPE="nightly"
            # there are only -latest symlinks with major version for nightlies
            RHEL_VERSION=7
        else
            RELEASE_TYPE="rel-eng"
        fi

        echo "[server]
name=Server
baseurl=http://download.devel.redhat.com/rhel-7/$RELEASE_TYPE/RHEL-7/latest-RHEL-$RHEL_VERSION/compose/Server/\$basearch/os/
enabled=1
gpgcheck=0

[server-optional]
name=Server-optional
baseurl=http://download.devel.redhat.com/rhel-7/$RELEASE_TYPE/RHEL-7/latest-RHEL-$RHEL_VERSION/compose/Server-optional/\$basearch/os/
enabled=1
gpgcheck=0

" > /var/lib/lorax/composer/repos.d/test.repo

        composer_start --no-system-repos
        present_repos=$(ls /var/lib/lorax/composer/repos.d/)
        rlAssertEquals "Only test.repo found in repos.d" "$present_repos" "test.repo"

        UUID=$(composer-cli compose start example-http-server partitioned-disk)
        rlAssertEquals "exit code should be zero" $? 0
        UUID=$(echo $UUID | cut -f 2 -d' ')

        wait_for_compose $UUID
    rlPhaseEnd

    rlPhaseStartCleanup
        $CLI compose delete $UUID
        MANUAL=1 composer_stop
        rlRun -t -c "rm -rf /var/lib/lorax/composer/repos.d"
        rlRun -t -c "mv $repodir_backup /var/lib/lorax/composer/repos.d"
        composer_start
    rlPhaseEnd
rlJournalEnd
rlJournalPrintText