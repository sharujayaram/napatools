from pymongo import MongoClient

c = MongoClient('172.23.100.125', 27021)


c.admin.command('addshard', 'SHRD204/172.23.100.121:27014')

c.admin.command('addshard', 'SHRD205/172.23.100.122:27015')

c.admin.command('addshard', 'SHRD206/172.23.100.123:27016')

c.admin.command('addshard','SHRD207/172.23.100.124:27017')


c.admin.command('enablesharding', 'tpcc')

c.admin.command('shardCollection', 'tpcc.ITEM', key={'_id': 'hashed'}, numInitialChunks=450)

c.admin.command('shardCollection', 'tpcc.CUSTOMER', key={'C_ID':1})

c.admin.command('shardCollection', 'tpcc.DISTRICT', key={'D_ID': 1})

c.admin.command('shardCollection', 'tpcc.HISTORY', key={'_id': 'hashed'}, numInitialChunks=450)

c.admin.command('shardCollection', 'tpcc.NEW_ORDER', key={'NO_O_ID': 1})

c.admin.command('shardCollection', 'tpcc.ORDERS', key={'O_ID': 1})

c.admin.command('shardCollection', 'tpcc.ORDER_LINE', key={'_id': 'hashed'}, numInitialChunks=450)

c.admin.command('shardCollection', 'tpcc.STOCK', key={'S_I_ID': 1})

c.admin.command('shardCollection', 'tpcc.WAREHOUSE', key={'_id': 'hashed'}, numInitialChunks=450)

#c.admin.command('shardCollection', 'tpcc.ITEM', key={'_id': 'hashed'}, numInitialChunks=450)



