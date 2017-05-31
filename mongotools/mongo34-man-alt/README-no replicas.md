
- create config server replica set  (204-206):
numactl --interleave=all mongod --config config_server.cfg


- connect to config server replica set member (190):
mongo --host 172.23.100.204 --port 27020

- setup config replicas:
rs.initiate(
  {
    _id: "CFG",
    configsvr: true,
    members: [
      { _id : 0, host : "172.23.100.204:27020" },
      { _id : 1, host : "172.23.100.205:27020" },
      { _id : 3, host : "172.23.100.206:27020" }
    ]
  }
)



- create 4 replica sets with 1 primary 1 replica setup
204:
numactl --interleave=all mongod --config shard_204.cfg

205:
numactl --interleave=all mongod --config shard_205.cfg

206:
numactl --interleave=all mongod --config shard_206.cfg

207:
numactl --interleave=all mongod --config shard_207.cfg



190:
mongo --host 172.23.100.204 --port 27018
rs.initiate(
  {
    _id: "SHRD204",
    members: [
      { _id : 0, host : "172.23.100.204:27018" }
    ]
  }
)

190:
mongo --host 172.23.100.205 --port 27018
rs.initiate(
  {
    _id: "SHRD205",
    members: [
      { _id : 0, host : "172.23.100.205:27018" }
    ]
  }
)

190:
mongo --host 172.23.100.206 --port 27018
rs.initiate(
  {
    _id: "SHRD206",
    members: [
      { _id : 0, host : "172.23.100.206:27018" }
    ]
  }
)

190:
mongo --host 172.23.100.207 --port 27018
rs.initiate(
  {
    _id: "SHRD207",
    members: [
      { _id : 0, host : "172.23.100.207:27018" }
    ]
  }
)

- config mongos (192-193)
mongos --config mongos_server.cfg


- connect to mongos instance (190)
mongo --host localhost --port 27021

- add shards replica sets to cluster:
sh.addShard("SHRD204/172.23.100.204:27018")
sh.addShard("SHRD205/172.23.100.205:27018")
sh.addShard("SHRD206/172.23.100.206:27018")
sh.addShard("SHRD207/172.23.100.207:27018")


- ycsb db setup -
use ycsb
sh.enableSharding("ycsb")
db.runCommand({shardCollection: "ycsb.usertable", key: {"_id": "hashed"}, numInitialChunks: 450})
db.runCommand({setParameter:1, cursorTimeoutMillis: 60000})