set -x

mongod --config cfg/shard_207.cfg

mongod --config cfg/shard_205.cfg

mongod --config cfg/shard_206.cfg

