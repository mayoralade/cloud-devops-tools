#!/bin/bash
yum update -y
yum install -y wget
wget -P /tmp http://s3.amazonaws.com/cfengine.packages/quick-install-cfengine-enterprise.sh && sudo bash /tmp/quick-install-cfengine-enterprise.sh hub
sudo /var/cfengine/bin/cf-agent --bootstrap `ip route get 1 | awk '{print $NF;exit}'`