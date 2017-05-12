config port: 27020
http://metrics.sc.couchbase.com/



===== install (all 8 servers) ====
sudo service mongod stop
sudo yum erase $(rpm -qa | grep mongodb-org)
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongo
cp mongodb-org-2.6.repo /etc/yum.repos.d/mongodb-org-2.6.repo
yum install -y mongodb-org-3.2.13 mongodb-org-server-3.2.13 mongodb-org-shell-3.2.13 mongodb-org-mongos-3.2.13 mongodb-org-tools-3.2.13

-- 190-194 --
mkdir /data/configdb
mkdir /data/mongodb
mkdir /data/mongodb/shard190
mkdir /data/mongodb/shard191
mkdir /data/mongodb/shard192
mkdir /data/mongodb/shard193



==== configure ====

- create config server replica set  (190-194):
numactl --interleave=all mongod --config config_server.cfg


- connect to config server replica set member (204):
mongo --host 172.23.100.190 --port 27020

- setup config replicas:
rs.initiate(
  {
    _id: "CFG",
    configsvr: true,
    members: [
      { _id : 0, host : "172.23.100.190:27020" },
      { _id : 1, host : "172.23.100.191:27020" },
      { _id : 3, host : "172.23.100.192:27020" },
      { _id : 4, host : "172.23.100.193:27020" }
    ]
  }
)



- create 4 replica sets with 1 primary 1 replica setup
190:
numactl --interleave=all mongod --config shard_190.cfg
numactl --interleave=all mongod --config shard_193.cfg


191:
numactl --interleave=all mongod --config shard_191.cfg
numactl --interleave=all mongod --config shard_190.cfg


192:
numactl --interleave=all mongod --config shard_191.cfg
numactl --interleave=all mongod --config shard_192.cfg

193:
numactl --interleave=all mongod --config shard_192.cfg
numactl --interleave=all mongod --config shard_193.cfg


204:
mongo --host 172.23.100.190 --port 27019
rs.initiate(
  {
    _id: "SHRD190",
    members: [
      { _id : 0, host : "172.23.100.190:27019" },
      { _id : 1, host : "172.23.100.191:27019" }
    ]
  }
)

mongo --host 172.23.100.191 --port 27018
rs.initiate(
  {
    _id: "SHRD191",
    members: [
      { _id : 0, host : "172.23.100.191:27018" },
      { _id : 1, host : "172.23.100.192:27018" }
    ]
  }
)

mongo --host 172.23.100.192 --port 27017
rs.initiate(
  {
    _id: "SHRD192",
    members: [
      { _id : 0, host : "172.23.100.192:27017" },
      { _id : 1, host : "172.23.100.193:27017" }
    ]
  }
)

mongo --host 172.23.100.193 --port 27016
rs.initiate(
  {
    _id: "SHRD193",
    members: [
      { _id : 0, host : "172.23.100.193:27016" },
      { _id : 1, host : "172.23.100.190:27016" }
    ]
  }
)


- config mongos (204-207)
mongos --config mongos_server.cfg


- connect to mongos instance (204)
mongo --host localhost --port 27021

- add shards replica sets to cluster:
sh.addShard("SHRD190/172.23.100.190:27019")
sh.addShard("SHRD191/172.23.100.191:27018")
sh.addShard("SHRD192/172.23.100.192:27017")
sh.addShard("SHRD193/172.23.100.193:27016")


- ycsb db setup -
use ycsb
sh.enableSharding("ycsb")
db.runCommand({shardCollection: "ycsb.usertable", key: {"_id": "hashed"}, numInitialChunks: 450})
db.runCommand({setParameter:1, cursorTimeoutMillis: 60000})