# cleanup and install mongo
service mongod stop
killall mongod
yum erase $(rpm -qa | grep mongodb-org)
rm -Rf /var/lib/mongo/*
rm -Rf /var/log/mongo/*
rm -rf /var/log/mongod
rm -rf /var/lib/mongo
rm -rf /var/lib/mongod
rm -rf /data/configdb
rm -rf /data/mongodb
cp mongodb-org-2.6.repo /etc/yum.repos.d/mongodb-org-2.6.repo
yum install -y mongodb-org-3.2.13 mongodb-org-server-3.2.13 mongodb-org-shell-3.2.13 mongodb-org-mongos-3.2.13 mongodb-org-tools-3.2.13
cd /data
mkdir configdb
mkdir mongodb
cd /data/mongodb
mkdir shard190
mkdir shard191
mkdir shard192
mkdir shard193

