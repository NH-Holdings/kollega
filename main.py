import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot er online som {bot.user}")

# @bot.command
# async def help(ctx):
#     helpText = """
#         Jada    
#     """
#     await ctx.send(helpText)

@bot.command
async def hei(ctx):
    await ctx.send("""helpText""")


print("hello world")
bot.run("")
