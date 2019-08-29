from pymongo import MongoClient

c = MongoClient('172.23.100.204', 27020)

config = { '_id': 'CFG', 'configsvr': True, 'members':
    [ { '_id' : 0, 'host' : "172.23.100.204:27020" },
      { '_id' : 1, 'host' : "172.23.100.205:27020" },
      { '_id' : 3, 'host' : "172.23.100.206:27020" },
      { '_id' : 4, 'host' : "172.23.100.207:27020" } ] }

c.admin.command("replSetInitiate", config)

