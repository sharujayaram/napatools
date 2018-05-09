
- create config server replica set  (211, 39, 40):
numactl --interleave=all mongod --config config_server.cfg


- connect to config server replica set member (210):
mongo --host 172.23.99.211 --port 27020

- setup config replicas:
rs.initiate(
  {
    _id: "CFG",
    configsvr: true,
    members: [
      { _id : 0, host : "172.23.99.211:27020" },
      { _id : 1, host : "172.23.99.39:27020" },
      { _id : 3, host : "172.23.99.40:27020" }
    ]
  }
)


- create 4 replica sets with 1 node only
211:
numactl --interleave=all mongod --config shard_211.cfg

39:
numactl --interleave=all mongod --config shard_39.cfg

40:
numactl --interleave=all mongod --config shard_40.cfg



210:
mongo --host 172.23.99.211 --port 27018
rs.initiate(
  {
    _id: "SHRD211",
    members: [
      { _id : 0, host : "172.23.99.211:27018" }
    ]
  }
)

210:
mongo --host 172.23.99.39 --port 27018
rs.initiate(
  {
    _id: "SHRD39",
    members: [
      { _id : 0, host : "172.23.99.39:27018" }
    ]
  }
)

210:
mongo --host 172.23.99.40 --port 27018
rs.initiate(
  {
    _id: "SHRD40",
    members: [
      { _id : 0, host : "172.23.99.40:27018" }
    ]
  }
)


- config mongos (210)
mongos --config mongos_server.cfg


- connect to mongos instance (210)
mongo --host localhost --port 27021

- add shards replica sets to cluster:
sh.addShard("SHRD211/172.23.99.211:27018")
sh.addShard("SHRD39/172.23.99.39:27018")
sh.addShard("SHRD40/172.23.99.40:27018")


- wiki db setup -
use wiki
sh.enableSharding("wiki")
db.runCommand({shardCollection: "wiki.bucket1", key: {"_id": "hashed"}, numInitialChunks: 450})
db.runCommand({setParameter:1, cursorTimeoutMillis: 60000})
