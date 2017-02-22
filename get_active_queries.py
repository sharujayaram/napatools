import requests
import sys
from requests.auth import HTTPBasicAuth


_server = None
_usr = None
_pwd = None

for i,item in enumerate(sys.argv):
    if item == "-s":
        _server = sys.argv[i+1]
    if item == "-u":
        _usr = sys.argv[i+1]
    if item == "-p":
        _pwd = sys.argv[i+1]

if not (_server and _usr and _pwd):
    print "Usage get_active_queries.py -s <server> -u <user> -p <password>"
    sys.exit()


r = requests.get('http://{}:8093/admin/active_requests'.format(_server), auth=HTTPBasicAuth(_usr, _pwd))

resp = r.json()
print resp
for item in resp:
    if 'elapsedTime' in item:
        elapsed_time = item['elapsedTime']
        elapsed_time_str = elapsed_time
        l,r = elapsed_time.split(".")
        if "ms" in r:
            elapsed_time = int(l)
        elif "s" in r:
            r = r[:(len(r)-1)]
            if len(r)>2:
                r = r[:3]
            if "m" in l:
                ll, lr = l.split("m")
                l = int(int(ll) * 60 + int(lr))
            elapsed_time = int(l) * 1000 + int(r)
        item['elapsedTime'] = elapsed_time

sorted_resp = sorted(resp, key=lambda k: k['elapsedTime'], reverse=True)
out_table = list()
counter = 0
out_row = {}
all_keys = ("elapsedTime",
             "executionTime",
             "requestId",
            "requestTime",
            "scanConsistency",
             "state",
             "statement")

for item in sorted_resp:
    out_row = {}

    for k in all_keys:
        out_row[k] = "none"

    for k in all_keys:
        if k in item:
            out_row[k] = item[k]
    out_table.append(out_row)
    print out_row

    with open("to_queries.csv", 'w') as fp:
        print >> fp, "{},{},{},{},{},{},{}".format("elapsedTime",
                                                    "executionTime",
                                                    "requestId",
                                                   "requestTime",
                                                   "scanConsistency",
                                                   "state",
                                                   "statement")
        for row in out_table:
            print >> fp, "{},{},{},{},{},{},\"{}\"".format(row["elapsedTime"],
                                                           row["executionTime"],
                                                           row["requestId"],
                                                           row["requestTime"],
                                                           row["scanConsistency"],
                                                           row["state"],
                                                           row["statement"])
