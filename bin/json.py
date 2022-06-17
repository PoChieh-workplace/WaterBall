import json



def open_json_member_inf():
    with open('./config/json/member_inf.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_member_inf(data):
    with open('./config/json/member_inf.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


def open_json_date():
    with open('./config/json/DateCalculate.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_date(data):
    with open('./config/json/DateCalculate.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)

#臉書介面
def open_json_FBpost():
    with open('./config/json/facebook.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_FBpost(data):
    with open('./config/json/facebook.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)



# 加入與離開訊息
def open_json_JoinAndLeave():
    with open('./config/json/JoinAndLeave.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_JoinAndLeave(data):
    with open('./config/json/JoinAndLeave.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)

# 權限
def open_json_permission():
    with open("./config/json/permission.json",'r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_permission(data):
    with open("./config/json/permission.json",'w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


# 日期倒數

def openDate():
    with open('./config/json/DateCalculate.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def writeDate(data):
    with open('./config/json/DateCalculate.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)