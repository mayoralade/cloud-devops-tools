#!/bin/bash
echo | sudo adduser gerrit
if [ -e "/etc/os-release" -o -e "/etc/redhat-release" -o -e "/etc/SuSE-release" ]; then
  sudo yum -y install java-1.8.0-openjdk git
  sudo update-alternatives --set java /usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin/java
elif [ -e "/etc/debian_version" ]; then
  sudo apt-get -y install oracle-java8-installer
  sudo update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
else
    exit 0
sudo su - gerrit
wget https://www.gerritcodereview.com/download/gerrit-2.14.3.war -O gerrit.war
java -jar gerrit.war init --batch -d ~/gerrit_testsite
# Change tge canonicalWebUrl to http://<publicIpAddress>:8080/ in ~/gerrit_testsite/bin/gerrit.config
# Then restart gerrit
~/gerrit_testsite/bin/gerrit.sh start
logout