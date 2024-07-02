import discord
from discord.ext import commands
import os
import lib.botsetup as bs

bs.varset()

def getuserid(user):
    return int(user[2:len(user)-1])

bot = commands.Bot(command_prefix=bs.prefix, intents=discord.Intents.all())

async def load_extensions():
    cogsnum = 0
    errd = []
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            cogsnum += 1
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
                print("{} 불러오기 완료.".format(filename[:-3]))
            except Exception as err:
                print("{} 불러오기 실패.".format(filename[:-3]))
                errd[filename[:-3]] = err
    if len(errd) == 0:
        print("{0}개 중 {0}개 추가 기능 불러오기 완료.".format(cogsnum))
    else:
        print("{0}개 중 {1}개 추가 기능에서 오류가 발생했습니다. ".format(cogsnum, len(errd)))
        for i in list(errd.items()):
            print(i[0]+" :"+str(i[1]).split(":")[2])
    synced = await bot.tree.sync()
    print(f"{len(synced)}개의 슬래시 커맨드 활성화")

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    await load_extensions()
    await bot.change_presence(activity=discord.Game(name='Geometry Dash'))

@bot.command(help = "테스트")
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

@bot.command(help = "입력한 내용을 출력합니다")
async def echo(ctx, *, abc):
    await ctx.send(abc)

@bot.command(help = "봇을 종료합니다. 봇 관리자만 이용 가능")
async def shutdown(ctx):
    if ctx.message.author.id == int(bs.myid):
        await ctx.send("종료중...")
        await bot.close()
    else:
        await ctx.send("개발자만 종료할 수 있습니다. ")
bot.run(bs.token)

# ProxieLBot
# based on VoltaBot 2.2
# made by volta1538(VoltLamp)
# original bot made by volta1538(VoltLamp)
# e-mail : dnaipoz.noipdsa@gmail.com