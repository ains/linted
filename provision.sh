export VE_DIR=/home/vagrant/.envs/linted
export CODE_DIR=/vagrant

#install dependencies
apt-get update
apt-get install -y language-pack-en
apt-get install -y build-essential git
apt-get install -y python-software-properties
apt-get install -y libpq-dev
apt-get install -y postgresql postgresql-contrib

#Install Docker
apt-get install -y linux-image-extra-`uname -r`
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
apt-get update
apt-get install -y lxc-docker

#Add vagrant to docker user group
groupadd docker
gpasswd -a vagrant docker
service docker restart

#Install redis
add-apt-repository -y ppa:chris-lea/redis-server
apt-get update
apt-get install -y redis-server

#Install python packages
apt-get install -y python python-dev python-setuptools
easy_install pip
pip install setuptools --no-use-wheel --upgrade
pip install virtualenv

#Create postgres user / database
sudo -u postgres psql -c "CREATE USER linted WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD 'development'"
sudo -u postgres psql -c "CREATE DATABASE linted WITH OWNER linted"

#Create virtualenv
virtualenv --no-site-packages $VE_DIR
chown -R vagrant $VE_DIR/../
chgrp -R vagrant $VE_DIR/../

sudo -u vagrant $VE_DIR/bin/pip install -r $CODE_DIR/requirements.txt

#Run syncdb to create south specific databases
if [ ! -e /home/vagrant/.provisioned ]
then
    (cd $CODE_DIR && $VE_DIR/bin/python manage.py syncdb --noinput)
    (cd $CODE_DIR && $VE_DIR/bin/python manage.py update_admin_user --username=admin --password=development)

    touch /home/vagrant/.provisioned
fi

#Perform migrations for application
(cd $CODE_DIR && $VE_DIR/bin/python manage.py migrate linted)

#Install enabled scanners
(cd $CODE_DIR && $VE_DIR/bin/python manage.py install_scanners)
