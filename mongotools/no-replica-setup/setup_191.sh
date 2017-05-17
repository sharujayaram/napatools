# install
bash scripts/install-3.2.sh

# create config server replica set
numactl --interleave=all mongod --config cfg/config_server.cfg

# os config
ulimit -n 10270

# start mongod replica set
numactl --interleave=all mongod --config cfg/shard_191.cfg

# set mongod replicas
mongo  --port 27018 < js/setup-data-replicas-for-191.js

# set cursor timeout
mongo --port 27018 < js/set-cursor-timeout.js
