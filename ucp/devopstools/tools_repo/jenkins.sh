#!/bin/bash
if [ -e "/etc/os-release" -o -e "/etc/redhat-release" -o -e "/etc/SuSE-release" ]; then
  sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
  sudo rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
  sudo yum -y install jenkins
  sudo yum -y install java-1.8.0-openjdk
  sudo update-alternatives --set java /usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin/java
  sudo service jenkins start
  sudo chkconfig jenkins on &> /dev/null
  sudo systemctl enable jenkins &> /dev/null
elif [ -e "/etc/debian_version" ]; then
  wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
  sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
  sudo apt-get update
  sudo apt-get install jenkins
else
    echo 'Unknown Distribution, exiting...'
    exit 0
fi