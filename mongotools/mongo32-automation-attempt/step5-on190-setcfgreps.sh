set -x

# set replicas for config server
mongo  --port 27020 < js/setup-config-replicas.js

# os config
ulimit -n 24000

# start mongod replica set
numactl --interleave=all mongod --config cfg/shard_190.cfg

# set mongod replicas
mongo  --port 27018 < js/setup-data-replicas-for-190.js

# set cursor timeout
mongo --port 27018 < js/set-cursor-timeout.js
