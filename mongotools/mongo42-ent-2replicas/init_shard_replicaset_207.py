from pymongo import MongoClient

c = MongoClient('172.23.100.124', 27017)

config = { '_id': "SHRD207",
           'members': [ { '_id' : 0, 'host' : "172.23.100.124:27017" },
                      { '_id' : 1, 'host' : "172.23.100.122:27017" },
                      { '_id' : 2, 'host' : "172.23.100.123:27017" } ] }

c.admin.command("replSetInitiate", config)

