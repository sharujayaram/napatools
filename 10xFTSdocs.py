import sys
from threading import Thread
from couchbase.bucket import Bucket
import json
import pymongo
import datetime

#SERVER = "localhost"
SERVER = "172.23.99.211"


def transfer(threads, cbpassword, cbbucket, offset):
    batch_size = 1000000 / int(threads)

    for i in range(0, int(threads)):
        print "process {} started".format(i)
        new_thread = Thread(target=run_batch, args=(batch_size, i, cbpassword, cbbucket, offset))
        new_thread.start()


def run_batch(size, id, cbpassword, cbbucket, offset):
    if cbpassword != "":
        cb = Bucket("couchbase://{}/{}?operation_timeout=10".format(SERVER, cbbucket), password=cbpassword)
    else:
        cb = Bucket("couchbase://{}/{}?operation_timeout=10".format(SERVER))

    min = id * size + 1 + int(offset)
    max = min + size

    for i in range (min, max):
        doc_id = "{}".format(i)
        doc = cb.get(doc_id).value
        for n in range (1, 10):
            key = "{}_{}".format(i,n)
            cb.upsert(key, doc)
            print "inserted doc {}".format(key)

threads = 20
cbpassword = ""
cbbucket = "bucket-1"
offset = 0

for i, item in enumerate(sys.argv):
    if item == "-threads":
        threads = sys.argv[i + 1]
    elif item == "-cbpassword":
        cbpassword = sys.argv[i + 1]
    elif item == "-cbbucket":
        cbbucket = sys.argv[i + 1]
    elif item == "-offset":
        offset = sys.argv[i + 1]


transfer(threads, cbpassword, cbbucket, offset)
