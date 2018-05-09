set -x

chmod 777 /data

service mongod stop
killall -9 mongod
yum erase $(rpm -qa | grep mongodb)
rm -rf /var/log/mongo
rm -rf /var/log/mongod
rm -rf /var/lib/mongo
rm -rf /var/lib/mongod
rm -rf /data/configdb
rm -rf /data/mongodb
cp mongodb-enterprise.repo /etc/yum.repos.d/mongodb-enterprise.repo
yum install -y mongodb-enterprise
cd /data
mkdir configdb
mkdir mongodb
cd /data/mongodb
mkdir shard211
mkdir shard39
mkdir shard40

ulimit -n 32000
