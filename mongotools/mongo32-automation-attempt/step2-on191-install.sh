set -x

# install
bash scripts/install-3.2.sh

# os config
ulimit -n 10270

# create config server replica set
numactl --interleave=all mongod --config cfg/config_server.cfg
