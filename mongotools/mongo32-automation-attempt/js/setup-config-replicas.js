rs.initiate(
  {
    _id: "CFG",
    configsvr: true,
    members: [
      { _id : 0, host : "172.23.100.190:27020" },
      { _id : 1, host : "172.23.100.191:27020" },
      { _id : 3, host : "172.23.100.192:27020" },
      { _id : 4, host : "172.23.100.193:27020" }
    ]
  }
)