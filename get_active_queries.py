
#
# curl -X POST 'http://172.23.100.190:8093/admin/settings' -u Administrator:password -d '{"completed-threshold":1000, "completed-limit":10000}'
#
# {"completed-limit":10000,"completed-threshold":1000,"controls":false,"cpuprofile":"","debug":false,"keep-alive-length":16384,"loglevel":"INFO","max-parallelism":1,"memprofile":"","pipeline-batch":16,"pipeline-cap":512,"pretty":true,"profile":"off","request-size-cap":67108864,"scan-cap":0,"servicers":192,"timeout":0}
#
# http://172.23.100.190:8093/admin/completed_requests
#
#
import requests
from requests.auth import HTTPBasicAuth


_server = "172.23.100.190"


r = requests.get('http://{}:8093/admin/active_requests'.format(_server), auth=HTTPBasicAuth('Administrator',
																							   'password'))
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
