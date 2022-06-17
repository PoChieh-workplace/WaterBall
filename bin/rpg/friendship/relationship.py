
from discord import Client
from bin.embed import getembed
from bin.image.friendship import friend_exp_img
from bin.rpg.friendship.config import RELATION_LIMIT
from bin.rpg.rpgsql import check_relation, delete_data, friend_count
from bin.View.relationship import confession_check_button,make_friendship,feed_friend
from config.zh_tw import PRE
from config.color import *
from config.emoji import RED_HEART,YELLOW_HEART,GREEN_HEART,BACK
from discord import User




#### 關係列表

async def check_user_relation(c:Client,ctx,user:User=None,user2:User=None):
    if user2 == None:
        if user == None:user = ctx.author
        list1 = friend_count(user.id)
        for i in list1:
            for k in i:
                if c.get_user(k)==None:delete_data(k)
        return await ctx.send(embed=getembed(
            f"❤ | {user.name} 的關係列表",
            f"{RED_HEART} 配偶數：`{len(list1[2])}` 人 \n"
            f"` {'`、`'.join([c.get_user(v).name for v in list1[2] if c.get_user(v)!=None])}` \n\n"
            f"{YELLOW_HEART} 伴侶數：`{len(list1[1])}` 人 \n"
            f"` {'`、`'.join([c.get_user(v).name for v in list1[1] if c.get_user(v)!=None])}`\n\n"
            f"{GREEN_HEART} 朋友數：`{len(list1[0])}` 人 \n"
            f"` {'`、`'.join([c.get_user(v).name for v in list1[0] if c.get_user(v)!=None])}`\n\n",
            LIGHT_ORANGE
        ))
    else:
        if user2.id == ctx.author.id and user.id == ctx.author.id:return await ctx.send(embed=getembed(f"{BACK} | 我與我的關係？", "這必須要掌控在四次元裡才看的出來！", RED))
        relation = friend_count(user.id, user2.id)
        if relation == -1:return await ctx.send(embed=getembed(f"{user.name} 與 {user2.name} 只是陌生人而已", "", BLACK))
        elif relation[3] == 0:embed=getembed(f"{GREEN_HEART} | {user.name} 與 {user2.name} 為朋友關係", f"親密度：`{relation[2]}`\n交友紀念日： `{relation[4]}` ", BLUE)
        elif relation[3] == 1:embed=getembed(f"{YELLOW_HEART} | {user.name} 與 {user2.name} 為情侶關係", f"親密度：`{relation[2]}`\n\n交友紀念日： `{relation[4]}` \n交往紀念日：`{relation[5]}`", YELLOW)
        elif relation[3] == 2:embed=getembed(f"{RED_HEART} | {user.name} 與 {user2.name} 是夫妻關係喔", f"親密度：`{relation[2]}`\n\n交友紀念日： `{relation[4]}` \n交往紀念日：`{relation[5]}` \n結婚紀念日：`{relation[6]}`", RED)
        file = friend_exp_img(relation[2],0,RELATION_LIMIT[relation[3]])
        embed.set_image(url='attachment://image.png')
        return await ctx.send(embed = embed, view=confession_check_button(),file=file)


#### 交朋友指令

async def relation_make_friend(ctx,user:User):
    if user.id == ctx.author.id:return await ctx.send(embed=getembed(f"{BACK} | 你似乎有點孤單", "", RED))
    elif user.bot:return await ctx.send(embed=getembed(f"{BACK} | 過久的等待不太好，換個人吧", "", RED))
    check = check_relation(ctx.author.id, user.id)
    if check == -1:return await ctx.send(embed=getembed(f"{GREEN_HEART} 只是朋友...", f"{user.mention}，{ctx.author.name} 想和你當朋友", GREEN), view=make_friendship(ctx.author, user))
    elif check[3] == 0:return await ctx.send(embed=getembed(f"{BACK} | 你們已經是朋友了", f"想更近一步？試試 `{PRE}confession` 或 `{PRE}proposal` 吧", RED))
    elif check[3] == 1:return await ctx.send(embed=getembed(f"{BACK} | 怎麼能忘掉自己的情侶？", f"想更近一步？試試 `{PRE}proposal` 吧", RED))
    elif check[3] == 2:return await ctx.send(embed=getembed(f"{BACK} | 你有在尊重這段感情嗎？你們已經是夫妻了！", "", RED))

async def relation_give_gift(ctx,user):
    if user.id == ctx.author.id:return await ctx.send(embed=getembed(f"{BACK} | 你似乎有點孤單", "", RED))
    check = check_relation(ctx.author.id, user.id)
    if check == -1:return await ctx.send(embed=getembed(f"{BACK} | 你們不曾相識", "", RED))
    else:return await ctx.send(embed=getembed(f"🍡禮物", f"請選擇贈禮 {user.name} 的方式", LIGHT_BLUE), view=feed_friend(ctx.author, user, check[3]))
