#!/bin/bash
curl -L https://omnitruck.chef.io/install.sh | sudo bash
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
