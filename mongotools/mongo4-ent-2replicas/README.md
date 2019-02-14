config port: 27020
http://metrics.sc.couchbase.com/



===== install (all 8 servers) ====
sudo service mongod stop
sudo yum erase $(rpm -qa | grep mongodb-org)
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongo

cp mongodb-enterprise.repo /etc/yum.repos.d/mongodb-enterprise.repo
sudo yum install -y mongodb-enterprise


-- 204-207 --
mkdir /data/configdb
mkdir /data/mongodb
mkdir /data/mongodb/shard204
mkdir /data/mongodb/shard205
mkdir /data/mongodb/shard206
mkdir /data/mongodb/shard207




==== configure ====

- create config server replica set  (204-207):
numactl --interleave=all mongod --config cfg/config_server.cfg



- connect to config server replica set member (204):
mongo --host 172.23.100.204 --port 27020

- setup config replicas:
rs.initiate(
  {
    _id: "CFG",
    configsvr: true,
    members: [
      { _id : 0, host : "172.23.100.204:27020" },
      { _id : 1, host : "172.23.100.205:27020" },
      { _id : 3, host : "172.23.100.206:27020" },
      { _id : 4, host : "172.23.100.207:27020" }
    ]
  }
)



- create 4 replica sets with 1 primary 2 replica setup
204:
numactl --interleave=all mongod --config cfg/shard204.cfg
numactl --interleave=all mongod --config cfg/shard205.cfg
numactl --interleave=all mongod --config cfg/shard206.cfg


205:
numactl --interleave=all mongod --config cfg/shard205.cfg
numactl --interleave=all mongod --config cfg/shard204.cfg
numactl --interleave=all mongod --config cfg/shard207.cfg



206:
numactl --interleave=all mongod --config cfg/shard_206.cfg
numactl --interleave=all mongod --config cfg/shard_204.cfg
numactl --interleave=all mongod --config cfg/shard_207.cfg


207:
numactl --interleave=all mongod --config cfg/shard_207.cfg
numactl --interleave=all mongod --config cfg/shard_205.cfg
numactl --interleave=all mongod --config cfg/shard_206.cfg



204:
mongo --host 172.23.100.204 --port 27014
rs.initiate(
  {
    _id: "SHRD204",
    members: [
      { _id : 0, host : "172.23.100.204:27014" },
      { _id : 1, host : "172.23.100.205:27014" }
      { _id : 2, host : "172.23.100.206:27014" }
    ]
  }
)

205:
mongo --host 172.23.100.205 --port 27015
rs.initiate(
  {
    _id: "SHRD205",
    members: [
      { _id : 0, host : "172.23.100.205:27015" },
      { _id : 1, host : "172.23.100.204:27015" }
      { _id : 2, host : "172.23.100.207:27015" }
    ]
  }
)

206:
mongo --host 172.23.100.206 --port 27016
rs.initiate(
  {
    _id: "SHRD206",
    members: [
      { _id : 0, host : "172.23.100.206:27016" },
      { _id : 1, host : "172.23.100.204:27016" }
      { _id : 2, host : "172.23.100.207:27016" }
    ]
  }
)

207:
mongo --host 172.23.100.207 --port 27017
rs.initiate(
  {
    _id: "SHRD207",
    members: [
      { _id : 0, host : "172.23.100.207:27017" },
      { _id : 1, host : "172.23.100.205:27017" }
      { _id : 2, host : "172.23.100.206:27017" }
    ]
  }
)


- config mongos (190-193)
mongos --config mongos_server.cfg


- connect to mongos instance (190)
mongo --host localhost --port 27021

- add shards replica sets to cluster:
sh.addShard("SHRD204/172.23.100.204:27014")
sh.addShard("SHRD205/172.23.100.205:27015")
sh.addShard("SHRD206/172.23.100.206:27016")
sh.addShard("SHRD207/172.23.100.207:27017")


- ycsb db setup -
use ycsb
sh.enableSharding("ycsb")
db.runCommand({shardCollection: "ycsb.usertable", key: {"_id": "hashed"}, numInitialChunks: 450})
db.runCommand({setParameter:1, cursorTimeoutMillis: 60000})