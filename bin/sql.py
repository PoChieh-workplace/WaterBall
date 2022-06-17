
from bin.embed import getembed
from bin.rpg.rpgsql import check_data
from config.emoji import BACK
from discord import Member, User
import mysql.connector

from config.color import RED



class db:
    db = mysql.connector.connect(
        host = "localhost",
        user = "waterball",
        passwd = "water@0724",
        database = "WaterBall"
    )

    def connect(self) ->tuple:
        try:db.ping()
        except:
            db = mysql.connector.connect(
                host = "localhost",
                user = "waterball",
                passwd = "water@0724",
                database = "WaterBall"
            )
        return (db.cursor(),db)

sys = db()


#學號註冊用
def check_whsh_id(user:User,school_id:str):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `discord_id` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
    if len(mycursor.fetchall())!=0:return getembed(f"{BACK} | 你已經註冊過了","",RED)
    mycursor.execute(f"SELECT `school_uuid` FROM `whsh_inf` WHERE `school_uuid` = '{school_id}'")
    if len(mycursor.fetchall())!=0:return getembed(f"{BACK} | {school_id} 學號似乎已經註冊過了","",RED)
    return False


#一般查詢是否有
def check_if_whsh(user:User):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `discord_id` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
    if len(mycursor.fetchall())!=0:return True
    return False


#回傳資料
def get_whsh_inf(user:User):
    if check_if_whsh(user)==True:
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT `discord_id`,`name`,`school_uuid`,`classroom` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
        return mycursor.fetchall()[0]
    else:return None

def add_whsh_id(user:User,name:str,school_id:str,classroom:int):
    mycursor,db = sys.connect()
    a = check_whsh_id(user,school_id)
    if a==False:
        check_data(user.id)
        try:mycursor.execute(f"INSERT INTO `whsh_inf` (`discord_id`,`name`,`school_uuid`,`classroom`) VALUES({user.id},'{name}','{school_id}',{classroom})")
        except:return getembed(f"{BACK} | 發生問題，如果重複發生請通知開發者","",RED)
        db.commit()

#儲存暫時暱稱
def set_tmp_nickname(user:Member):
    mycursor,db = sys.connect()
    if user.nick==None:
        if get_tmp_nickname(user)!=None:return del_tmp_nickname(user)
        else:return
    if get_tmp_nickname(user)==None:mycursor.execute(f"INSERT INTO `nickname_tmp` (`id`,`nickname`) VALUES({user.id},'{user.nick}')")
    else:mycursor.execute(f"UPDATE `nickname_tmp` SET `nickname` = '{user.nick}' WHERE `id` = {user.id};")
    db.commit()

def get_tmp_nickname(user:User):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `nickname` FROM `nickname_tmp` WHERE `id` = {user.id}")
    a = mycursor.fetchall()
    if len(a)==0:return None
    else:return a[0][0]


def del_tmp_nickname(user:User):
    mycursor,db = sys.connect()
    try:
        mycursor.execute(f"DELETE FROM `nickname_tmp` WHERE `id` = {user.id}")
        db.commit()
        return True
    except:return False