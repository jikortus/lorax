# NOTE: This specfile is generated from upstream at https://github.com/rhinstaller/lorax
# NOTE: Please submit changes as a pull request
%define debug_package %{nil}

Name:           lorax
Version:        39.0
Release:        1%{?dist}
Summary:        Tool for creating the anaconda install images

License:        GPL-2.0-or-later
URL:            https://github.com/weldr/lorax
# To generate Source0 do:
# git clone https://github.com/weldr/lorax
# git checkout -b archive-branch lorax-%%{version}-%%{release}
# tito build --tgz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       lorax-templates

Requires:       cpio
Requires:       device-mapper
Requires:       dosfstools
Requires:       e2fsprogs
Requires:       findutils
Requires:       gawk
Requires:       xorriso
Requires:       glib2
Requires:       glibc
Requires:       glibc-common
Requires:       gzip
Requires:       isomd5sum
Requires:       module-init-tools
Requires:       parted
Requires:       squashfs-tools >= 4.2
Requires:       util-linux
Requires:       xz-lzma-compat
Requires:       xz
Requires:       pigz
Requires:       pbzip2
Requires:       dracut >= 030
Requires:       kpartx
Requires:       psmisc

# Python modules
Requires:       libselinux-python3
Requires:       python3-mako
Requires:       python3-kickstart >= 3.19
Requires:       python3-dnf >= 3.2.0
Requires:       python3-librepo
Requires:       python3-pycdio

%if 0%{?fedora}
# Fedora specific deps
%ifarch x86_64
Requires:       hfsplus-tools
%endif
%endif

%ifarch x86_64 ppc64le
Requires:       grub2
Requires:       grub2-tools
%endif

%ifarch s390 s390x
Requires:       openssh
Requires:       s390utils >= 2.15.0-2
%endif

# Moved image-minimizer tool to lorax
Provides:       appliance-tools-minimizer = %{version}-%{release}
Obsoletes:      appliance-tools-minimizer < 007.7-3

%description
Lorax is a tool for creating the anaconda install images.

It also includes livemedia-creator which is used to create bootable livemedia,
including live isos and disk images. It can use libvirtd for the install, or
Anaconda's image install feature.

%package docs
Summary: Lorax html documentation
Requires: lorax = %{version}-%{release}

%description docs
Includes the full html documentation for lorax, livemedia-creator, and the pylorax library.

%package lmc-virt
Summary:  livemedia-creator libvirt dependencies
Requires: lorax = %{version}-%{release}
Requires: qemu

# Fedora edk2 builds currently only support these arches
%ifarch x86_64 aarch64
Requires: edk2-ovmf
%endif
Recommends: qemu-kvm

%description lmc-virt
Additional dependencies required by livemedia-creator when using it with qemu.

%package lmc-novirt
Summary:  livemedia-creator no-virt dependencies
Requires: lorax = %{version}-%{release}
Requires: anaconda-core
Requires: anaconda-tui
Requires: anaconda-install-env-deps
Requires: system-logos
Requires: python3-psutil

%description lmc-novirt
Additional dependencies required by livemedia-creator when using it with --no-virt
to run Anaconda.

%package templates-generic
Summary:  Generic build templates for lorax and livemedia-creator
Requires: lorax = %{version}-%{release}
Provides: lorax-templates = %{version}-%{release}

%description templates-generic
Lorax templates for creating the boot.iso and live isos are placed in
/usr/share/lorax/templates.d/99-generic

%prep
%autosetup -p1 -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

%files
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS
%doc docs/lorax.rst docs/livemedia-creator.rst docs/product-images.rst
%doc docs/*ks
%{python3_sitelib}/pylorax
%{python3_sitelib}/*.egg-info
%{_sbindir}/lorax
%{_sbindir}/mkefiboot
%{_sbindir}/livemedia-creator
%{_bindir}/mkksiso
%{_bindir}/image-minimizer
%dir %{_sysconfdir}/lorax
%config(noreplace) %{_sysconfdir}/lorax/lorax.conf
%dir %{_datadir}/lorax
%{_mandir}/man1/lorax.1*
%{_mandir}/man1/livemedia-creator.1*
%{_mandir}/man1/mkksiso.1*
%{_mandir}/man1/image-minimizer.1*
%{_tmpfilesdir}/lorax.conf

%files docs
%doc docs/html/*

%files lmc-virt

%files lmc-novirt

%files templates-generic
%dir %{_datadir}/lorax/templates.d
%{_datadir}/lorax/templates.d/*

%changelog
* Mon Feb 20 2023 Brian C. Lane <bcl@redhat.com> 38.7-1
- Don't strip gtk4 binaries or libtiff (#2170716) (awilliam@redhat.com)
- image-minimizer: Use RuntimeError instead of Exception (bcl@redhat.com)
- creator: Use RuntimeError instead of Exception (bcl@redhat.com)
- treebuilder: Use RuntimeError instead of Exception (bcl@redhat.com)
- mount: Use RuntimeError instead of Exception (bcl@redhat.com)
- ltmpl: Use RuntimeError instead of Exception (bcl@redhat.com)
- spec: Use autosetup to make patching easier (bcl@redhat.com)
- Revert "templates.d/99-generic/live: Enable automatic persistence for live media" (awilliam@redhat.com)
- Strip some things from gtk4 (awilliam@redhat.com)

* Tue Feb 14 2023 Brian C. Lane <bcl@redhat.com> 38.6-1
- templates.d/99-generic/live: Enable automatic persistence for live media (ngompa@fedoraproject.org)
- Update for Noto CJK Variable Fonts (pwu@redhat.com)

* Wed Feb 08 2023 Brian C. Lane <bcl@redhat.com> 38.5-1
- Fix using --dracut-conf with DracutChroot (bcl@redhat.com)
- tests: Fix DataHolder for CreatorTest (bcl@redhat.com)
- runtime-install: Update for
  https://fedoraproject.org/wiki/Changes/NotoFontsForMoreLang (akira@tagoh.org)
- SPDX migration (bcl@redhat.com)
- rsyslogd.conf: Rewrite using current config syntax (bcl@redhat.com)
- Add comment for squashfs-only (dick@mrns.nl)
- runtime-install: exclude some more unneeded firmware packages (awilliam@redhat.com)
- runtime-install: stop excluding bfa-firmware again (retired) (awilliam@redhat.com)

* Mon Dec 12 2022 Brian C. Lane <bcl@redhat.com> 38.4-1
- runtime-cleanup: drop old versions of qed firmware (awilliam@redhat.com)
- runtime-cleanup: drop Mediatek SoC firmwares (awilliam@redhat.com)
- runtime-install: drop bfa-firmware (awilliam@redhat.com)
- mkksiso: Disable running mkefiboot in container tests (bcl@redhat.com)
- mkksiso: Rebuild efiboot.img for UEFI enabled isos (bcl@redhat.com)
- gitleaks: Add config file to ignore known fake secrets (bcl@redhat.com)
- fedora-livemedia.ks: Use livesys-scripts (bcl@redhat.com)
- workflows: Switch to actions/checkout@v3 (bcl@redhat.com)

* Mon Nov 28 2022 Brian C. Lane <bcl@redhat.com> 38.3-1
- Use unicode.pf2 from /usr/share/grub/ (bcl@redhat.com)
- On ppc64le Use core.elf from grub2 package (bcl@redhat.com)

* Wed Nov 09 2022 Brian C. Lane <bcl@redhat.com> 38.2-1
- runtime-postinstall: Disable sshd.socket (bcl@redhat.com)
- docs: Document mock and SELinux not working together (bcl@redhat.com)
- imgutils: Don't delete dirs created for DracutChroot (bcl@redhat.com)
- tito: Use .tito instead of old ./rel-eng directory (bcl@redhat.com)
- setup.py: Set the version number (bcl@redhat.com)
- Improvement of unmounting /proc, /dev and binds (soksanichenko@cloudlinux.com)

* Tue Oct 11 2022 Brian C. Lane <bcl@redhat.com> 38.1-1
- livemedia-creator: Allow file: url without networking (bcl@redhat.com)
- Update kdump addon package name (vslavik@redhat.com)
- Drop anaconda auditd replacement (vslavik@redhat.com)

* Fri Sep 30 2022 Brian C. Lane <bcl@redhat.com> 38.0-1
- New lorax documentation - 38.0 (bcl@redhat.com)
- tests: Update test_creator.py for new cmdline options (bcl@redhat.com)
- livemedia-creator: Add release, variant, bugurl, and isfinal cmdline flags (cappy@cappuchino.xyz)
- Drop 32-bit ARM and x86 support (awilliam@redhat.com)
- Update anaconda's crash messages to watch (vslavik@redhat.com)
- livemedia-creator: Add --product to cmdline args (bcl@redhat.com)
- fedora-livemedia: Make sure GNOME Software service isn't started (bcl@redhat.com)
- fonts packages syncup in template files (akira@tagoh.org)
- tests: Add tzdata package to minimizer test setup (bcl@redhat.com)

* Mon Jul 25 2022 Brian C. Lane <bcl@redhat.com> 37.8-1
- mkksiso: Optionally support 3 arguments or --ks (bcl@redhat.com)
- mkksiso: Add -U to xorriso on ppc64le (bcl@redhat.com)
- mkksiso: Fix passing -iso-level to xorriso (bcl@redhat.com)
- pylorax: SafeConfigParser is now ConfigParser (bcl@redhat.com)
- test: Update test code for new pylint version (bcl@redhat.com)
- tests: Switch back to rawhide for tests (bcl@redhat.com)
- workflow: Remove sudo from workflow (bcl@redhat.com)

* Wed Jul 13 2022 Brian C. Lane <bcl@redhat.com> 37.7-1
- mkksiso: Set u+rw permission on extracted files and directories (bcl@redhat.com)
- Add option to boot local drive to the x86 BIOS grub2 menu (bcl@redhat.com)

* Tue Jun 28 2022 Brian C. Lane <bcl@redhat.com> 37.6-1
- tests: Use Fedora 36 for test-in-podman (bcl@redhat.com)
- Add include for architecture specific packages to example kickstarts (bcl@redhat.com)
- templates: adjust for mellanox firmware split to subpackage (awilliam@redhat.com)
- mkksiso: Fix s390x support (bcl@redhat.com)
- spec: Don't require grub2 on x86-32 (bcl@redhat.com)
- mkksiso: Remove use of os.path.join (bcl@redhat.com)
- Makefile: Add mkksiso and image-minimizer to coverage report (bcl@redhat.com)
- tests: Add tests for mkksiso (bcl@redhat.com)
- mkksiso: Add kernel cmdline customization support (bcl@redhat.com)
- mkksiso: Move kickstart to --ks KICKSTART (bcl@redhat.com)
- mkksiso: Add helper functions for kernel cmdline modifications (bcl@redhat.com)

* Fri Jun 03 2022 Brian C. Lane <bcl@redhat.com> 37.5-1
- example ks: Drop syslinux and add grub2-tools package for livemedia (bcl@redhat.com)
- templates: Set @ISOLABEL@ in the bios-grub.cfg file to the isolabel (bcl@redhat.com)
- Update spec for syslinux->grub2 switch (awilliam@redhat.com)

* Wed Jun 01 2022 Brian C. Lane <bcl@redhat.com> 37.4-1
- mkksiso: Fix grub2 editing error (bcl@redhat.com)

* Wed Jun 01 2022 Brian C. Lane <bcl@redhat.com> 37.3-1
- Add grub2 BIOS boot support to live iso template (bcl@redhat.com)
  Resolves: rhbz#2092065
- Drop grafting variables (bcl@redhat.com)
- Drop macboot.img and simplify efiboot.img use (bcl@redhat.com)
- Add grub2 BIOS boot support (bcl@redhat.com)
- Remove syslinux support (bcl@redhat.com)

* Mon May 23 2022 Brian C. Lane <bcl@redhat.com> 37.2-1
- cleanup: drop phanfw.bin from linux-firmware (awilliam@redhat.com)
- cleanup: strip more mellanox firmware files (awilliam@redhat.com)
- cleanup: strip qcom/vpu* from linux-firmware (awilliam@redhat.com)
- cleanup: drop qcom/apq8096 firmwares (awilliam@redhat.com)

* Wed May 11 2022 Brian C. Lane <bcl@redhat.com> 37.1-1
- New lorax documentation - 37.1 (bcl@redhat.com)
- docs: Update the mkksiso documentation (bcl@redhat.com)
- setup.py: Install mkksiso to /usr/bin (bcl@redhat.com)
- pylorax: Move variable out of try block (bcl@redhat.com)
- setup.py: Use setup from setuptools not distutils (bcl@redhat.com)
- Makefile: Remove -it options for test-in-podman (bcl@redhat.com)
- mkksiso: Rewrite to use xorriso features (bcl@redhat.com)
- docs: Fix typo in index.html (bcl@redhat.com)

* Mon Mar 28 2022 Brian C. Lane <bcl@redhat.com> 37.0-1
- New lorax documentation - 37.0 (bcl@redhat.com)
- runtime-cleanup: keep 'unshare' binary present from util-linux-core (kkoukiou@redhat.com)

* Mon Feb 28 2022 Brian C. Lane <bcl@redhat.com> 36.9-1
- Don't move the restart-anaconda file (vponcova@redhat.com)

* Wed Feb 16 2022 Brian C. Lane <bcl@redhat.com> 36.8-1
- runtime-cleanup: Remove ncurses package (bcl@redhat.com)

* Mon Feb 14 2022 Brian C. Lane <bcl@redhat.com> 36.7-1
- postinstall: Restore reproducible build timestamps on /usr/share/fonts (bcl@redhat.com)
- tests: Fix the image minimizer test dnf usage (bcl@redhat.com)
- runtime-cleanup: drop kernel drivers/iio (awilliam@redhat.com)
- runtime-cleanup: drop gallium-pipe drivers from mesa-dri-drivers (awilliam@redhat.com)
- runtime-cleanup: drop yelp's local MathJax library copy (awilliam@redhat.com)
- runtime-cleanup: drop eapol_test from wpa_supplicant (awilliam@redhat.com)
- runtime-cleanup: drop /usr/bin/cyrusbdb2current (awilliam@redhat.com)
- runtime-cleanup: drop systemd-analyze (awilliam@redhat.com)
- runtime-cleanup: drop mtools and glibc-gconv-extra (awilliam@redhat.com)
- runtime-cleanup: drop guile22's ccache (awilliam@redhat.com)
- runtime-cleanup: fix warnings from old or changed packages (awilliam@redhat.com)
- runtime-cleanup: drop Italic from google-noto-sans-vf-fonts (awilliam@redhat.com)
- runtime-install: drop some unnecessary font packages (awilliam@redhat.com)

* Fri Feb 04 2022 Brian C. Lane <bcl@redhat.com> 36.6-1
- mkksiso: Fix check for unsupported arch error (bcl@redhat.com)

* Thu Feb 03 2022 Brian C. Lane <bcl@redhat.com> 36.5-1
- mkksiso: Improve debug message about unsupported arch (bcl@redhat.com)
- mkksiso: Fix the order of the ppc mkisofs command (bcl@redhat.com)
- mkksiso: mkfsiso argument order matters (bcl@redhat.com)
- mkksiso: Add kickstart to s390x cdboot.prm (bcl@redhat.com)
- cleanup: handle RPM database move to /usr (awilliam@redhat.com)
- Install the variable font of the Cantarell font (akira@tagoh.org)
- Update the template for f36 Change proposal:
  https://fedoraproject.org/wiki/Changes/DefaultToNotoFonts (akira@tagoh.org)
- Update Malayalam font to its new renamed package name rit-meera-new-fonts (pnemade@fedoraproject.org)
- Enable sftp when using inst.sshd (bcl@redhat.com)
- Add inst.rngd cmdline option (bcl@redhat.com)
- docs: Update docs for image-minimizer (bcl@redhat.com)
- tests: Add tests for image-minimizer (bcl@redhat.com)
- image-minimizer: Check for missing root directory (bcl@redhat.com)
- image-minimizer: Fix utf8 error and add docs (bcl@redhat.com)

* Tue Dec 14 2021 Brian C. Lane <bcl@redhat.com> 36.4-1
- cleanup: remove binaries from lilv (awilliam@redhat.com)
- runtime-cleanup: remove pipewire-related packages (awilliam@redhat.com)
- New lorax documentation - 36.3 (bcl@redhat.com)

* Thu Dec 09 2021 Brian C. Lane <bcl@redhat.com> 36.3-1
- mkksiso: Check the length of the filenames (bcl@redhat.com)
- mkksiso: Check the iso's arch against the host's (bcl@redhat.com)
- mkksiso: Add missing implantisomd5 tool requirements (bcl@redhat.com)
- mkksiso: Raise error if no volume id is found (bcl@redhat.com)
- mount: Add s390x support to IsoMountopoint (bcl@redhat.com)
- mkksiso: Skip mkefiboot for non-UEFI isos (bcl@redhat.com)
- mkksiso: Add -joliet-long (bcl@redhat.com)
- mkksiso: Return 1 on errors (bcl@redhat.com)
- Fix monitor problem with split UTF8 characters (bcl@redhat.com)

* Wed Nov 10 2021 Brian C. Lane <bcl@redhat.com> 36.2-1
- Remove memtest86+ from example kickstarts (bcl@redhat.com)
- fedora-livemedia: Update example kickstart (bcl@redhat.com)
- mount: Switch to using pycdio instead of pycdlib (bcl@redhat.com)
- Move default releasever into pylorax DEFAULT_RELEASEVER (bcl@redhat.com)
- runtime-postinstall: Drop raidstart/stop stub code (bcl@redhat.com)
- runtime-install: Fix grub2 epoch, it is 1 not 0 (bcl@redhat.com)
- Update runtime-install/cleanup for Marvell Prestera fw split (awilliam@redhat.com)

* Thu Oct 28 2021 Brian C. Lane <bcl@redhat.com> 36.1-1
- dnfbase: Handle defaults better (bcl@redhat.com)
- ltmpl: Add version compare support to installpkg (bcl@redhat.com)

* Mon Oct 11 2021 Brian C. Lane <bcl@redhat.com> 36.0-1
- New lorax documentation - 36.0 (bcl@redhat.com)
- docs: Remove logging command from examples (bcl@redhat.com)
- runtime-install: exclude liquidio and netronome firmwares (awilliam@redhat.com)
- runtime-cleanup: drop Marvell Prestera firmware files (awilliam@redhat.com)
- runtime-cleanup: drop some Qualcomm smartphone firmwares (awilliam@redhat.com)
- Fix pylint warnings about string formatting (bcl@redhat.com)
- tests: Ignore new pylint warnings (bcl@redhat.com)
- Add fstrim to disk and filesystem image creation (bcl@redhat.com)

* Tue Sep 07 2021 Brian C. Lane <bcl@redhat.com> 35.7-1
- templates: Remove memtest86+ (bcl@redhat.com)

* Thu Jul 08 2021 Brian C. Lane <bcl@redhat.com> 35.6-1
- Install unicode.pf2 from new directory (bcl@redhat.com)
- Makefile: Use sudo to fix ownership of docs (bcl@redhat.com)
- Makefile: Make sure container is built before docs (bcl@redhat.com)
- Makefile: Add local-srpm target to create a .src.rpm from HEAD (bcl@redhat.com)
- mkksiso: cmdline should default to empty string (bcl@redhat.com)
- runtime-install: Remove gfs2-utils (bcl@redhat.com)
- mount.py: Fix docstring (jkucera@redhat.com)

* Fri Jun 11 2021 Brian C. Lane <bcl@redhat.com> 35.5-1
- pylorax: Fix mksparse ftruncate size handling (bcl@redhat.com)

* Thu Jun 10 2021 Brian C. Lane <bcl@redhat.com> 35.4-1
- livemedia-creator: Check for mkfs.hfsplus (bcl@redhat.com)
- Drop retired icfg (zbyszek@in.waw.pl)

* Tue May 25 2021 Brian C. Lane <bcl@redhat.com> 35.3-1
- Add a context manager for dracut (bcl@redhat.com)
  Resolves: rhbz#1962975
- Remove unneeded aajohan-comfortaa-fonts (bcl@redhat.com)

* Wed May 05 2021 Brian C. Lane <bcl@redhat.com> 35.2-1
- runtime-cleanup: Use branding package name instead of product.name (bcl@redhat.com)
- treebuilder: Add branding package to template variables (bcl@redhat.com)
- livemedia-creator: Use inst.ks on cmdline for virt (bcl@redhat.com)
- docs: Remove composer-cli.1 (bcl@redhat.com)

* Mon Apr 26 2021 Brian C. Lane <bcl@redhat.com> 35.1-1
- New lorax documentation - 35.1 (bcl@redhat.com)
- Makefile: Use podman as a user for testing and docs (bcl@redhat.com)
- composer-cli: Remove all traces of composer-cli (bcl@redhat.com)
- livemedia-creator: Add rhgb to live iso cmdline (#1943312) (bcl@redhat.com)
- tests: Fix pocketlint use of removed pylint messages (bcl@redhat.com)
- Disable X11 forwarding from installation environment. (vslavik@redhat.com)
- Remove display-related packages (vslavik@redhat.com)
- Drop trying to install reiserfs-utils (kevin@scrye.com)
- test: Fix URL to bots testmap (martin@piware.de)
- Change khmeros-base-fonts to khmer-os-system-fonts. (pnemade@fedoraproject.org)
- Fix output path in docs (vslavik@redhat.com)
- runtime-cleanup: don't wipe /usr/bin/report-cli (#1937550) (awilliam@redhat.com)
- xorg-x11-font-utils is now four packages, remove all of them (peter.hutterer@who-t.net)
- xorg-x11-server-utils was split up in Fedora 34, so adjust templates (kevin@scrye.com)
* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com> 35.0-1
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)

* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com>
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)
