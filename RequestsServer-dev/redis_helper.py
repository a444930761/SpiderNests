#如何在redis中优雅地存入多维数据
# redis_helper.py
# redis 数据处理
# Author : Lengyue

import redis

class helper:
    def __init__(self):
        rdp = redis.ConnectionPool(host='127.0.0.1', port=6379,db=9)
        self.dbc = redis.StrictRedis(connection_pool=rdp)


    def Transform(self,arr):
        temp = {}
        if type(arr) == type([]):
            for i in range(len(arr)):
                temp[i] = arr[i]
            next = temp
            return self.Transform(next)
        elif type(arr) == type({}):
            a = {}
            for i in arr.keys():
                deep = self.Transform(arr[i])
                if type(deep) == type({}):
                    for j in deep.keys():
                        temp = str(i) + "::" + str(j)
                        a[temp] = deep[j]
                else:
                    temp = str(i)
                    a[temp] = deep
            return a
        return arr

    def DeTransform(self,plain):
        arr = {}
        #nclist = []
        for i in plain.keys():
            s = i.split("::")
            #print(s)
            if len(s)!=0 and s != ['']:
                if s[0] not in arr.keys():
                    #nclist.append(s[0])
                    arr[s[0]] = {}
                    #print(nclist)
            else:
                return plain['']
        for i in arr.keys():
            temp = {}
            for j in plain.keys():
                s = j.split("::")
                if len(s) != 0 and s[0] == i:
                    temp["::".join(s[1:])] = plain[j]
            #print(temp)
            arr[i] = self.DeTransform(temp)
        return arr

if __name__ == "__main__":
    import json
    a = {
  "db":{
      "redis":{
        "ip":"127.0.0.1",
        "port":6379,
        "password":""
      }
  },

  "API_Settings":{
    "Connection_key":"a61a6b836f3d72684dc35f28cbae4b2d"
  },

  "Flask_Settings":{
    "host":"0.0.0.0",
    "port":5000
  },
  "Modules":[
    {
      "path":"libs",
      "name":"usercore",
      "version":1,
      "author":"Lengyue",
      "blueprints":[
        "usercore"
      ]
    },
    {
      "path":"libs",
      "name":"taskcore",
      "version":1,
      "author":"Lengyue",
      "blueprints":[
        "taskcore"
      ]
    },
    {
      "path":"libs",
      "name":"servercore",
      "version":1,
      "author":"Lengyue",
      "blueprints":[
        "servercore"
      ]
    },{
      "path":"libs",
      "name":"main",
      "version":1,
      "author":"Lengyue",
      "blueprints":[
        "main"
      ]
    }
  ],

  "log":{
    "file":"log.txt"
  }
}
    traded = helper().Transform(a)
    print(json.dumps(traded))
    print(json.dumps(helper().DeTransform(traded)))