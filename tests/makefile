# Windows
#APT_GET=env APT_CONFIG=$(PWD)/apt.conf /usr/local/apt-0.7.9ubuntu17.2/bin/apt-get
# Linux
APT_GET=env APT_CONFIG=$(PWD)/apt.conf apt-get

all: apt_config

packages: soma_3.2.deb axon_3.2.deb

soma_3.2.deb: soma/DEBIAN/control
	cp -a soma no_svn
	find no_svn -name .svn -exec rm -Rf '{}' \; -prune
	dpkg -b no_svn soma_3.2.deb
	rm -Rf no_svn

axon_3.2.deb: axon/DEBIAN/control
	cp -a axon no_svn
	find no_svn -name .svn -exec rm -Rf '{}' \; -prune
	dpkg -b no_svn axon_3.2.deb
	rm -Rf no_svn

repository: 
	rm -Rf apt_repository;
	mkdir apt_repository;
	cp *.deb apt_repository;
	env PATH="$(PWD):$(PATH)" dpkg-scanpackages apt_repository /dev/null | gzip -9 > apt_repository/Packages.gz

dpkg_error:
	./dpkg --force-not-root --force-bad-path --root /home/yann/brainvisa-installer_tests/apt_install --admindir=/home/yann/brainvisa-installer_tests/apt_admin/lib/dpkg --log=/home/yann/brainvisa-installer_tests/apt_admin/lib/dpkg/dpkg.log --status-fd 1 --unpack --auto-deconfigure /home/yann/brainvisa-installer_tests/apt_repository/soma_3.2.deb
	./dpkg --force-not-root --force-bad-path --root /home/yann/brainvisa-installer_tests/apt_install --admindir=/home/yann/brainvisa-installer_tests/apt_admin/lib/dpkg --log=/home/yann/brainvisa-installer_tests/apt_admin/lib/dpkg/dpkg.log --status-fd 1 --configure soma
	
config: repository apt.conf.in
	rm -Rf apt_install
	mkdir apt_install
	
	rm -Rf apt_admin
	mkdir apt_admin
	touch apt_admin/status
	mkdir apt_admin/updates
	touch apt_admin/available
	mkdir apt_admin/lib
	mkdir apt_admin/lib/dpkg
	mkdir apt_admin/lib/apt
	touch apt_admin/lib/dpkg/lock
	touch apt_admin/lib/dpkg/status
	mkdir apt_admin/lib/dpkg/updates
	touch apt_admin/lib/dpkg/available
	mkdir apt_admin/lib/dpkg/triggers
	mkdir apt_admin/lib/dpkg/info
	mkdir apt_admin/cache
	mkdir apt_admin/cache/apt
	mkdir apt_admin/log
	mkdir apt_admin/log/apt
	echo "deb file:$(PWD) apt_repository/" > apt_admin/sources.list
	touch apt_admin/preferences
	mkdir apt_admin/archives
	mkdir apt_admin/archives/partial
	mkdir apt_admin/lists
	mkdir apt_admin/lists/partial
	touch apt_admin/lists/lock
	cp apt.conf.in apt.conf
	perl -pi -e "s#MAIN_DIR#$(PWD)#" apt.conf
	$(APT_GET) -c apt.conf update

dpkg_config:
	rm -Rf dpkg_admin
	rm -Rf dpkg_install
	
	mkdir dpkg_admin
	mkdir dpkg_install
	touch dpkg_admin/status
	mkdir dpkg_admin/updates
	touch dpkg_admin/available
	mkdir dpkg_admin/triggers
	mkdir dpkg_admin/info

dpkg_install: packages dpkg_config
	dpkg --force-not-root --force-bad-path --root $(PWD)/dpkg_install --admindir=$(PWD)/dpkg_admin -i soma_3.2.deb
	dpkg --force-not-root --force-bad-path --root $(PWD)/dpkg_install --admindir=$(PWD)/dpkg_admin -i axon_3.2.deb
	dpkg-query --admindir=$(PWD)/dpkg_admin -l

clean:
	rm -Rf *.deb *~ */DEBIAN/*~ no_svn apt_repository apt_install apt_admin dpkg_admin dpkg_install apt.conf

test:
	echo $(PWD)



