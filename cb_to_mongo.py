import sys
from threading import Thread
from couchbase.bucket import Bucket
import json
import pymongo
import datetime

#SERVER = "localhost"
SERVER = "172.23.100.190"


def transfer(threads, customers, cbpassword, cbbucket, mongodb, mongotable):
    batch_size = int(customers) / int(threads)

    for i in range(0, int(threads)):
        print "process {} started".format(i)
        new_thread = Thread(target=run_batch, args=(batch_size, i, cbpassword, cbbucket, mongodb, mongotable))
        new_thread.start()


def insert_to_mongo(id, doc, mdb, mcoll):
    post_id = mcoll.insert_one(doc).inserted_id
    print "document {} has been inserted to mongo".format(post_id)


def run_batch(size, id, cbpassword, cbbucket, mongodb, mongotable):
    if cbpassword != "":
        cb = Bucket("couchbase://{}/{}?operation_timeout=10".format(SERVER, cbbucket), password=cbpassword)
    else:
        cb = Bucket("couchbase://{}/{}?operation_timeout=10".format(SERVER))

    client = pymongo.MongoClient("mongodb://{}:27017/".format(SERVER))
    mdb = client[mongodb]
    mcollection = mdb[mongotable]

    min = id * size + 1
    max = min + size

    for i in range (min, max):
        doc_id = "customer:::{}".format(i)
        doc = cb.get(doc_id).value

        orders = []
        orders = doc["order_list"]
        y,m,d = doc["dob"].split("-")
        doc["dob"] = datetime.datetime(int(y), int(m), int(d))

        insert_to_mongo(id, doc, mdb, mcollection)

        for order in orders:
            orderdoc = cb.get(order).value
            insert_to_mongo(id, orderdoc, mdb, mcollection)

threads = 20
customers = 10000000
cbpassword = ""
cbbucket = "bucket-1"
mongodb = "soe"
mongotable = "bucket"

for i, item in enumerate(sys.argv):
    if item == "-threads":
        threads = sys.argv[i + 1]
    elif item == "-customers":
        customers = sys.argv[i + 1]
    elif item == "-cbpassword":
        cbpassword = sys.argv[i + 1]
    elif item == "-cbbucket":
        cbbucket = sys.argv[i + 1]
    elif item == "-mongodb":
        mongodb = sys.argv[i + 1]
    elif item == "-mongotable":
        mongotable = sys.argv[i + 1]

transfer(threads, customers, cbpassword, cbbucket, mongodb, mongotable)
