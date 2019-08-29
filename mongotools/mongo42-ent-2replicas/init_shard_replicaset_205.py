from pymongo import MongoClient

c = MongoClient('172.23.100.205', 27015)

config = { '_id': "SHRD205",
           'members': [ { '_id' : 0, 'host' : "172.23.100.205:27015" },
                      { '_id' : 1, 'host' : "172.23.100.204:27015" },
                      { '_id' : 2, 'host' : "172.23.100.207:27015" } ] }

c.admin.command("replSetInitiate", config)

