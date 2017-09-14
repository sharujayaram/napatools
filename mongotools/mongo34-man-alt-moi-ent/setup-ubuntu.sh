set -x

rm -rf /var/log/mongo
rm -rf /var/log/mongod
rm -rf /var/lib/mongo
rm -rf /var/lib/mongod
rm -rf /data/configdb
rm -rf /data/mongodb

service mongod stop
killall -9 mongod

apt-get remove mongodb-enterprise
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64,ppc64el,s390x ] http://repo.mongodb.com/apt/ubuntu xenial/mongodb-enterprise/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-enterprise.list
apt-get update
apt-get install -y mongodb-enterprise


cd /data
mkdir configdb
mkdir mongodb
cd /data/mongodb
mkdir shard204
mkdir shard205
mkdir shard206
mkdir shard207

ulimit -n 32000
