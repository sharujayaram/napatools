
#use admin
#db.shutdownServer({force: true})
#db.runCommand( { serverStatus: 1 } )
#db.runCommand( { getCmdLineOpts: 1 } )

db.collection.createIndex( { <field1>: <type>, <field2>: <type2>, ... } )
db.collection.createIndex( {"address.country":1, "age_group":1, "dob":1} )
db.collection.createIndex({"address.prev_address.zip":1})
db.collection.createIndex({"devices":1})
db.usertable.createIndex({"visited_places.country":1, "visited_places.cities":1})
db.usertable.createIndex({"visited_places.country":1})
db.usertable.createIndex({"visited_places.cities":1})

db.usertable.createIndex({"address.zip":1})
db.usertable.createIndex({"address.zip":1, "order_list":1})
db.usertable.createIndex({"month":1})
db.usertable.createIndex({"sale_price":1})
db.usertable.createIndex({"month":1, "sale_price":1})

- create config server replica set  (190-194):
numactl --interleave=all mongod --config config_server.cfg


- connect to config server replica set member (190):
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

191:
numactl --interleave=all mongod --config shard_191.cfg

192:
numactl --interleave=all mongod --config shard_192.cfg

193:
numactl --interleave=all mongod --config shard_193.cfg



204:
mongo --host 172.23.100.190 --port 27019
rs.initiate(
  {
    _id: "SHRD190",
    members: [
      { _id : 0, host : "172.23.100.190:27019" }
    ]
  }
)

mongo --host 172.23.100.191 --port 27018
rs.initiate(
  {
    _id: "SHRD191",
    members: [
      { _id : 0, host : "172.23.100.191:27018" }
    ]
  }
)

mongo --host 172.23.100.192 --port 27017
rs.initiate(
  {
    _id: "SHRD192",
    members: [
      { _id : 0, host : "172.23.100.192:27017" }
    ]
  }
)

mongo --host 172.23.100.193 --port 27016
rs.initiate(
  {
    _id: "SHRD193",
    members: [
      { _id : 0, host : "172.23.100.193:27016" }
    ]
  }
)exit


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