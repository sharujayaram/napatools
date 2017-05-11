sudo service mongod stop
sudo yum erase $(rpm -qa | grep mongodb-org)
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongo
cp mongodb-org-2.6.repo /etc/yum.repos.d/mongodb-org-2.6.repo
yum install -y mongodb-org-3.2.13 mongodb-org-server-3.2.13 mongodb-org-shell-3.2.13 mongodb-org-mongos-3.2.13 mongodb-org-tools-3.2.13
mkdir /data/configdb
mkdir /data/mongodb
mkdir /data/mongodb/shard190
mkdir /data/mongodb/shard191
mkdir /data/mongodb/shard192
mkdir /data/mongodb/shard193