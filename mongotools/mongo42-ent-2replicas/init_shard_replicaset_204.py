from pymongo import MongoClient

c = MongoClient('172.23.100.204', 27014)

config = { '_id': "SHRD204",
           'members': [ { '_id' : 0, 'host' : "172.23.100.204:27014" },
                      { '_id' : 1, 'host' : "172.23.100.205:27014" },
                      { '_id' : 2, 'host' : "172.23.100.206:27014" } ] }

c.admin.command("replSetInitiate", config)
