use ycsb
sh.enableSharding("ycsb")
use admin
db.runCommand({shardCollection: "ycsb.usertable", key: {"_id": "hashed"}, numInitialChunks: 450})
