import requests
import json
import hashlib
import threading
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

def getUserid(user_id,user_pw):
    _url = "https://dcid.dcinside.com/join/mobile_app_login.php"
    _hd  = {
    "User-agent" : "dcinside.app",
    "Referer" : "http://www.dcinside.com"
    }
    _data = {
        "user_id" : user_id,
        "user_pw" : user_pw
    }
    req = requests.post(url=_url,headers=_hd,data=_data)
    data = req.json()
    return data[0]["user_id"]

def getVersion():
    _url = "http://json2.dcinside.com/json0/app_check_A_rina.php"
    _hd  = {
    "User-agent" : "dcinside.app",
    "Referer" : "http://www.dcinside.com"
    }
    req = requests.get(url=_url,headers=_hd)
    data = req.json()
    return data[0]['ver']

def hashValueToken():
    now = datetime.now()
    str1 = "dcArdchk_%04d%02d%02d%02d" % (now.year,now.month,now.day,now.hour)
    data = hashlib.sha256(str1.encode()).hexdigest()
    return data

def getAppid():
    value_token = hashValueToken()
    version = getVersion()
    _url = "https://dcid.dcinside.com/join/mobile_app_key_verification_3rd.php"
    _hd  = {
    "User-agent" : "dcinside.app",
    "Referer" : "http://www.dcinside.com"
    }
    _data = {
    "value_token" : value_token,
    "signature" : "ReOo4u96nnv8Njd7707KpYiIVYQ3FlcKHDJE046Pg6s=",
    "pkg" : "com.dcinside.app",
    "vCode" : "30037",
    "vName" : version
    }

    req = requests.post(url=_url,headers=_hd,data=_data)
    data = req.json()
    return data[0]["app_id"]



def deletereq(id,app_id,user_id,v):
    data = v.split(",")
    _url = "http://m.dcinside.com/api/comment_del.php"
    _hd = {
        "User-agent" : "dcinside.app",
        "Referer" : "http://www.dcinside.com"
    }
    _data = {
        "user_id" : user_id,
        "id" : data[1],
        "no" : data[0],
        "comment_no" : data[2],
        "mode" : "comment_del",
        "app_id" : app_id
    }
    try:
        req = requests.post(url=_url,headers=_hd,data=_data)
        print(req.text)
    except:
        sleep(10)


def deletelist(id,pw,lists):
    user_id = getUserid(id,pw)
    app_id = getAppid()
    for v in lists:
        try:
            deletereq(id,app_id,user_id,v)
        except:
            print("차단먹혔습니다 잠시후 10초후 다시실행합니다")
            sleep(10)


def returnlistcnt(list):
    return len(list)

def main(id,pw,commentlist,label):
    label.setText("삭제중...")
    onelist = commentlist[int((len(commentlist)/2)):]
    twolist = commentlist[:int((len(commentlist)/2))]
    t1 = threading.Thread(target=deletelist, args=(id,pw,onelist))
    t1.start()
    t2 = threading.Thread(target=deletelist, args=(id,pw,twolist))
    t2.start()
    label.setText("댓글 삭제 완료!")