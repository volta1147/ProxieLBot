import discord
from discord.ext import commands
import os
import sys
sys.path.append('')

import lib.beforerun as bs
import lib.file as file

pffile = open("res" + os.path.sep + "memoprefix.txt")
pf = pffile.read()
pffile.close()

def getusercolor(ctx, userid):
    color = 0x000000
    for i in ctx.guild.roles:
        if userid in [j.id for j in i.members]:
            color = str(i.color)
    return int("0x"+color[1:], 16)

async def sendprofileembed(ctx, userinfo, pfver = -1):
    name = userinfo.name
    userid = userinfo.id
    if os.path.exists("profilerev" + os.path.sep + str(userid)):
        if pfver + 1:
            ver = pfver
        else:
            ver = file.getver('profilerev', str(userid))
        if file.isrev('profilerev', str(userid), ver):
            embed = discord.Embed(title = name, description = file.openrev("profilerev", str(userid), ver), color = getusercolor(ctx, userid))
            embed.set_footer(text = file.memover('profile', str(name), ver))
            await ctx.send(embed = embed)
        else:
            await ctx.send("해당 버전이 없습니다. ")
    else:
        await ctx.send("아직 작성된 자기소개가 없습니다. 자기소개를 작성하려면 ```" + bs.prefix + "introduce 자기소개```를 입력해주세요.")

class Memo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help = "메모 입출력 관련")
    async def memo(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("명령어가 올바르지 않습니다. ")

    @memo.command(name = "open", help = "메모를 출력합니다.")
    async def openm(self, ctx, *, filenamein):
        if (file.openfile("memo", filenamein).split())[0] == pf + "redirect":
            filename = " ".join((file.openfile("memo", filenamein).split())[1:])
        else:
            filename = filenamein
        if file.ismemo(filename):
            embed = discord.Embed(title = filename, description = file.openfile("memo", filename), color = 0xbdb092)
            embed.set_footer(text = file.memover('memo', filename, file.getver('rev', filename)))
            await ctx.send(embed = embed)
        else:
            await ctx.send(filename+" 메모가 없습니다. "+filename+" 메모를 생성하려면 \n```"+bs.prefix+"memo edit "+filename+" 메모 내용```\n 을 입력하세요.")

    @memo.command(help = "메모를 작성/수정합니다. ")
    async def edit(self, ctx, filenamein, *, memoin):
        if filenamein[0] == "'":
            tmpmemolist = memoin.split("'")
            filename = filenamein[1:] + " " + tmpmemolist[0]
            memo = ("'".join(tmpmemolist[1:]))[1:]
        else:
            filename = filenamein
            memo = memoin
        isexist = file.ismemo(filename)
        file.editfile("memo", filename, memo)
        file.rev("rev", filename, memo)
        if isexist:
            await ctx.send("**{}** 수정됨".format(filename))
        else:
            await ctx.send("**{}** 생성됨".format(filename))
    
    @memo.command(help = "메모를 삭제합니다. ")
    async def delete(self, ctx, filename):
        file.delfile("memo", filename)
        await ctx.send("삭제됨")

    @commands.command(help = "맨션한 사람(또는 자신)의 유저 정보를 출력합니다. ")
    async def profile(self, ctx, user = " "):
        if user == " ":
            userinfo = ctx.message.author
        else:
            userinfo = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        await sendprofileembed(ctx, userinfo, -1)

    @commands.command(help = "자기소개를 작성/수정합니다. ")
    async def introduce(self, ctx, *, memo):
        userid = ctx.message.author.id
        file.editfile("profile", str(userid), memo)
        file.rev("profilerev", str(userid), memo)
        await ctx.send("수정 완료")

    @commands.group(help = "메모 리버전 관련")
    async def rev(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("명령어가 올바르지 않습니다. ")

    @rev.command(name = "memo", help = "메모 리버전을 엽니다. ")
    async def memo2(self, ctx, filename, ver):
        if file.isrev("rev", filename, ver):
            embed = discord.Embed(title = filename, description = file.openrev("rev", filename, ver), color = 0xbdb092)
            embed.set_footer(text = file.memover('memo', filename, ver))
            await ctx.send(embed = embed)
        else:
            await ctx.send("해당 버전이 없습니다. ")

    # @rev.command(name = "memohistory", help = "메모 리버전 목록을 엽니다. ")
    # async def imemo(self, ctx, filename, ver):
    #     if file.isrev("rev", filename, ver):
    #         embed = discord.Embed(title = filename, description = file.openrev("rev", filename, ver), color = 0xbdb092)
    #         embed.set_footer(text = file.memover('memo', filename, ver))
    #         await ctx.send(embed = embed)
    #     else:
    #         await ctx.send("해당 버전이 없습니다. ")

    @rev.command(name = "profile", help = "맨션한 유저의 유저 정보 리버전을 불러옵니다. ")
    async def pfrev(self, ctx, user, pfver = -1):
        userinfo = await commands.MemberConverter.convert(self=commands.MemberConverter, ctx=ctx, argument=user)
        await sendprofileembed(ctx, userinfo, pfver)

    @rev.command(name = "myprofile")
    async def mypfrev(self, ctx, pfver = -1):
        userinfo = ctx.message.author
        await sendprofileembed(ctx, userinfo, pfver)
    
    @commands.group(name = "back", help = "메모 되돌리기 관련")
    async def backrev(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("명령어가 올바르지 않습니다. ")

    @backrev.command(name = "memo", help = "메모를 해당 버전으로 되돌립니다. ")
    async def memo3(self, ctx, filename, ver):
        if file.isrev("rev", filename, ver):
            file.editfile("memo", filename, file.openrev("rev", filename, ver))
            file.rev("rev", filename, file.openrev("rev", filename, ver))
            await ctx.send("되돌리기 완료!")
        else:
            await ctx.send("해당 버전이 없습니다. ")
        
async def setup(bot):
    await bot.add_cog(Memo(bot))