from pymongo import MongoClient

c = MongoClient('172.23.100.125', 27021)


c.admin.command('addshard', 'SHRD204/172.23.100.121:27014')

c.admin.command('addshard', 'SHRD205/172.23.100.122:27015')

c.admin.command('addshard', 'SHRD206/172.23.100.123:27016')

c.admin.command('addshard','SHRD207/172.23.100.124:27017')


c.admin.command('enablesharding', 'tpcc')

#c.admin.command('shardCollection', 'ycsb.usertable', key={'_id': 'hashed'}, numInitialChunks=450)

