import discord
import subprocess
import random
from discord.ext import commands
import sys

sys.path.append('')
import lib.file as file

class ButtonFunction(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label='엄 출력하기', style=discord.ButtonStyle.blurple)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("엄")

class Botplus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "print", help = "입력한 내용을 출력합니다 (원본 메시지 삭제)")
    async def printctx(self, ctx, *, abc):
        await ctx.channel.purge(limit=1)
        await ctx.send(abc)
    
    @commands.command(name = "random", help = "주어진 단어 중 하나를 선택합니다. ")
    async def randomword(self, ctx, *words):
        await ctx.send(random.choice(words))

    # @commands.group(name = "list", help = "리스트 랜덤추첨 관련")
    # async def levellist(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         await ctx.send("명령어가 올바르지 않습니다. ")
    # 
    # @levellist.command(name = "create", help = "리스트를 만듭니다. ")
    # async def createlist(self, ctx, *, listname):
    #     exi = file.islist(listname)
    #     file.openfile("levellist", listname, True)
    #     if exi:
    #         await ctx.send("{} 리스트가 이미 존재합니다. ".format(listname))
    #     else:
    #         await ctx.send("{} 리스트가 생성되었습니다. ".format(listname))
    # 
    # @levellist.command(name = "append", help = "리스트에 항목을 추가합니다. ")
    # async def appendlist(self, ctx, listname, *, level):
    #     if file.islist(listname):
    #         file.appendfile("levellist", listname, str(len(file.listsplit("levellist", listname))+1) + ". " + level + "\n")
    #         await ctx.send("완료")
    #     else:
    #         await ctx.send("{} 리스트가 존재하지 않습니다. ".format(listname))
    # 
    # @levellist.command(name = "file", help = "리스트에 첨부파일을 저장합니다. ")
    # async def appendlist(self, ctx, *, listname):
    #     if file.islist(listname):
    #         await discord.Attachment.save(fp="levellist\\input.txt")
    #         await ctx.send("완료")
    #     else:
    #         await ctx.send("{} 리스트가 존재하지 않습니다. ".format(listname))

    @commands.command(name = "um", help = "엄")
    async def bttest(self, ctx):
        await ctx.send("어음", view=ButtonFunction())
    
async def setup(bot):
    await bot.add_cog(Botplus(bot))