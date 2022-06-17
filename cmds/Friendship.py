from bin.rpg.friendship.confession import confession_system
from bin.rpg.friendship.relationship import check_user_relation, relation_give_gift, relation_make_friend
from discord import User
from discord.ext.commands import command,Context
from config.zh_tw import PRE
from core.classes import Cog_Extension


# 關係查詢

class Relationship(Cog_Extension,name = "感情系統"):

    @command(
        name="relationship",
        aliases=['r', 'relative', 'friendship'],
        brief = '查詢人脈或兩人間關係',
        usage = f'{PRE}r [@人] [@人]',
        description = (
            "範例：\n"
            f"`{PRE}r @水球` 顯示水球的人脈\n\n"
            f"`{PRE}r @水球 @雪球` 查詢水球與雪球的關係\n\n"
        )
    )
    async def _check_relationship(self, ctx:Context, user: User = None, user2: User = None):
        return await check_user_relation(self.bot,ctx,user,user2)

    @command(
        name="friend",
        aliases=['fd', 'makefriend'],
        brief = '交個朋友杯！我很和善的',
        usage = f'{PRE}friend <@人>',
        description = (
            "範例：\n"
            f"`{PRE}fd @水球` 跟水球交朋友\n\n"
        )
    )
    async def _make_friend(self, ctx:Context, user:User):
        return await relation_make_friend(ctx,user)

    @command(
        name="gift",
        aliases=['feed', 'worship', 'give'],
        brief = '贈送禮物給朋友或伴侶',
        usage = f'{PRE}gift <@人>',
        description = (
            "今日情人節，是不是該送個禮物呢？\n"
            "喔對！我忘了你沒有女友\n"
            "範例：\n"
            f"`{PRE}r @水球` 送水球禮物\n\n"
        )
    )
    async def give_gift(self, ctx:Context, user:User):
        return await relation_give_gift(ctx,user)
    
    @command(
        name = "confession",
        aliases = ['reveal','confess'],
        brief = 'wwww，我想告白',
        usage = f'{PRE}confess <@人>',
        description = (
            "🎈：我...現在想跟你說一件事，"
            "就是...我...我...喜歡你，請你跟我交往！"
        )
    )
    async def _confession(self,ctx:Context,user:User):
        return await confession_system(ctx,user)




# 交友



async def setup(bot):
    await bot.add_cog(Relationship(bot))
