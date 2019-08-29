from pymongo import MongoClient

c = MongoClient('172.23.100.206', 27016)

config = { '_id': "SHRD206",
           'members': [ { '_id' : 0, 'host' : "172.23.100.206:27016" },
                      { '_id' : 1, 'host' : "172.23.100.204:27016" },
                      { '_id' : 2, 'host' : "172.23.100.207:27016" } ] }

c.admin.command("replSetInitiate", config)

