#!/bin/bash
if [ -e "/etc/redhat-release" ]; then
  RELEASE="$(awk '/release/ {print $7}' /etc/redhat-release)"
  MAJOR_RELEASE=$(echo $RELEASE | cut -d "." -f 1)
  if [ "$MAJOR_RELEASE" -eq 7 ]; then
    PKG=https://packages.chef.io/files/current/chef-server/12.16.9/el/7/chef-server-core-12.16.9-1.el7.x86_64.rpm
  else
    PKG=https://packages.chef.io/files/current/chef-server/12.16.9/el/6/chef-server-core-12.16.9-1.el6.x86_64.rpm
  fi
elif [ -e "/etc/os-release" ]; then
  PKG=https://packages.chef.io/files/current/chef-server/12.16.9/el/6/chef-server-core-12.16.9-1.el6.x86_64.rpm
elif [ -e "/etc/SuSE-release" ]; then
  PKG=https://packages.chef.io/files/current/chef-server/12.16.9/sles/12/chef-server-core-12.16.9-1.sles12.x86_64.rpm
elif [ -e "/etc/debian_version" ]; then
  PKG=https://packages.chef.io/files/current/chef-server/12.16.9/ubuntu/16.04/chef-server-core_12.16.9-1_amd64.deb
else
    echo 'Unknown Distribution, exiting...'
    exit 0
fi
wget -P /tmp $PKG
PKGRPM=`ls /tmp | grep chef-*`
if [ -e "/etc/os-release" -o -e "/etc/redhat-release" -o -e "/etc/SuSE-release" ]; then
  rpm -Uvh /tmp/$PKGRPM
elif [ -e "/etc/debian_version" ]; then
  dpkg -i /tmp/$PKGRPM
else
    echo 'Unknown Distribution, exiting...'
    exit 0
fi
chef-server-ctl reconfigure
chef-server-ctl user-create admin admin chef dummy@example.net 'password' --filename /tmp/chef_user.txt
chef-server-ctl install chef-manage
chef-server-ctl reconfigure
chef-manage-ctl reconfigure
chef-server-ctl install opscode-push-jobs-server
chef-server-ctl reconfigure
opscode-push-jobs-server-ctl reconfigure
chef-server-ctl install opscode-reporting
chef-server-ctl reconfigure
opscode-reporting-ctl reconfigure