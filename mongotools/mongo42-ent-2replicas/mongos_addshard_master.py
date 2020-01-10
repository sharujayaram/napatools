from pymongo import MongoClient

c = MongoClient('172.23.100.190', 27021)


c.admin.command('addshard', 'SHRD204/172.23.100.204:27014')

c.admin.command('addshard', 'SHRD205/172.23.100.205:27015')

c.admin.command('addshard', 'SHRD206/172.23.100.206:27016')

c.admin.command('addshard','SHRD207/172.23.100.207:27017')


c.admin.command('enablesharding', 'ycsb')

c.admin.command('shardCollection', 'ycsb.usertable', key={'_id': 'hashed'}, numInitialChunks=450)

