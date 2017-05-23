set -x

service mongod stop
killall mongod
yum erase $(rpm -qa | grep mongodb-org)
rm -rf /var/log/mongo
rm -rf /var/log/mongod
rm -rf /var/lib/mongo
rm -rf /var/lib/mongod
rm -rf /davim ta/configdb
rm -rf /data/mongodb
cp mongodb-org-2.6.repo /etc/yum.repos.d/mongodb-org-2.6.repo
yum install mongodb-org
cd /data
mkdir configdb
mkdir mongodb
cd /data/mongodb
mkdir shard204
mkdir shard205
mkdir shard206
mkdir shard207
