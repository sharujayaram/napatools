# install
bash scripts/install-3.2.sh

# os config
ulimit -n 24000

# start mongos
mongos --config cfg/mongos_server.cfg

# set cursor timeout
mongo --port 27021 < js/set-cursor-timeout.js

