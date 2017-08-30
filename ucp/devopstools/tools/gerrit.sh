#!/bin/bash
echo | sudo adduser gerrit
sudo su gerrit
wget -P https://www.gerritcodereview.com/download/gerrit-2.14.3.war
java -jar gerrit.war init --batch -d ~/gerrit_testsite