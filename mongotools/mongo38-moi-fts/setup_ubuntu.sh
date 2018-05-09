set -x

service mongod stop
killall -9 mongod
apt-get purge mongodb-org*

rm -rf /var/log/mongo
rm -rf /var/log/mongod
rm -rf /var/lib/mongo
rm -rf /var/lib/mongod
rm -rf /data/configdb
rm -rf /data/mongodb

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64,ppc64el,s390x ] http://repo.mongodb.com/apt/ubuntu xenial/mongodb-enterprise/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-enterprise.list
sudo apt-get update
sudo apt-get install -y mongodb-enterprise

cd /data
mkdir configdb
mkdir mongodb
cd /data/mongodb
mkdir shard211
mkdir shard39
mkdir shard40

ulimit -n 32000
