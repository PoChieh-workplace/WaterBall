from distutils import command
from bin.json import open_json_FBpost,write_json_FBpost
import requests
import facebook
import urllib3
import json





def getFbPost(name):
    data = open_json_FBpost()
    id = data[name]["url"]
    token = data[name]["token"]
    took = facebook.GraphAPI(access_token=token, version ='2.10')
    getdata = took.request(id)
    return getdata

def updateNowId(name,getdata):
    data = open_json_FBpost()
    data[name]["id"] = getdata['posts']['data'][0]["id"]
    write_json_FBpost(data)

def getCount(name,getdata):
    data = open_json_FBpost()
    for i in range(100):
        try:fbdata = getdata['posts']['data'][99-i]
        except:continue
        if(str(fbdata['id']) == data[name]["id"]):
            updateid = 99-i
            break
        else:
            updateid = -1
    return updateid