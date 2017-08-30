#!/bin/bash
if [ -e "/etc/os-release" -o -e "/etc/redhat-release" -o -e "/etc/SuSE-release" ]; then
  wget -P /tmp https://dev.mysql.com/get/mysql57-community-release-el6-11.noarch.rpm
  rpm -ivh /tmp/mysql57-community-release-el6-11.noarch.rpm
  sudo yum -y install apr-devel apr-util-devel curl-devel gcc gcc-c++ git httpd httpd-devel ImageMagick-devel mysql-community-server mysql-community-devel nano postfix ruby-devel tar wget redhat-rpm-config zlib-devel openssl-devel
  sudo sed -i 's/Listen 80/Listen 8080/g' /etc/httpd/conf/httpd.conf
  for i in httpd mysqld postfix
  do
    service start $i
    chkconfig $i on
  done
  TEMPASSWD=`grep 'A temporary password' /var/log/mysqld.log | tail -1 | awk -F ' ' '{print $NF}'`
  mysqladmin -u root -p"$TEMPASSWD" password 'I0w@c1ty' &> /dev/null
  mysql -uroot -p"$TEMPASSWD" -e "CREATE DATABASE redmine CHARACTER SET utf8;" &> /dev/null
  mysql -uroot -p"$TEMPASSWD" -e "CREATE USER 'redmine'@'localhost' IDENTIFIED BY 'I0w@c1ty';" &> /dev/null
  mysql -uroot -p"$TEMPASSWD" -e "GRANT ALL PRIVILEGES ON redmine.* TO 'redmine'@'localhost';" &> /dev/null
  mysql -uroot -p"$TEMPASSWD" -e "FLUSH PRIVILEGES;" &> /dev/null
  wget -P /tmp http://www.redmine.org/releases/redmine-3.4.2.tar.gz
  tar xfz /tmp/redmine-3.4.2.tar.gz -C /tmp
  cp /tmp/redmine-3.4.2/config/database.yml.example /tmp/redmine-3.4.2/config/database.yml
  sed -i '0,/password: ""/s//password: "I0w@c1ty"/' /tmp/redmine-3.4.2/config/database.yml
  sudo cp -r /tmp/redmine-3.4.2 /var/www/redmine
  sudo chown apache:apache -R /var/www/redmine/files /var/www/redmine/log /var/www/redmine/public/plugin_assets /var/www/redmine/tmp
  gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
  \curl -sSL https://get.rvm.io | bash -s stable --ruby
  source ~/.profile
  rvm install 2.3.4
  rvm use 2.3.4
  gem install bundler
  sudo chmod -R 777 /var/www/redmine
  bundle install --without development test --gemfile /var/www/redmine/Gemfile
  cd /var/www/redmine && RAILS_ENV=production rake db:migrate
  echo | RAILS_ENV=production rake redmine:load_default_data
  gem install passenger --no-rdoc --no-ri
  sudo chmod o+x "/home/ec2-user"
  freeMem = `free -m -t | tail -1 | awk -F' ' '{print $NF}'`
  if [ $freeMem -lt 1024 ]; then
    sudo dd if=/dev/zero of=/swap bs=1M count=1024
    sudo mkswap /swap
    sudo swapon /swap
  fi
  echo | passenger-install-apache2-module
  sudo swapoff /swap
  echo "LoadModule passenger_module /home/ec2-user/.rvm/gems/ruby-2.3.4/gems/passenger-5.1.8/buildout/apache2/mod_passenger.so
     <IfModule mod_passenger.c>
       PassengerRoot /home/ec2-user/.rvm/gems/ruby-2.3.4/gems/passenger-5.1.8
       PassengerDefaultRuby /home/ec2-user/.rvm/gems/ruby-2.3.4/wrappers/ruby
     </IfModule>" > /etc/httpd/conf.modules.d/passenger.conf
  ipAddress=``ip route get 1 | awk '{print $NF;exit}'``
  echo "<VirtualHost *:8080>
    ServerName $ipAddress
    DocumentRoot /var/www/html
    Alias /redmine /var/www/redmine/public
    <Location /redmine>
      PassengerBaseURI /redmine
      PassengerAppRoot /var/www/redmine
    </Location>
    <Directory /var/www/redmine/public>
      AllowOverride all
      Options -MultiViews
    </Directory>
  </VirtualHost>" >> /etc/httpd/conf/httpd.conf
  service httpd restart
fi