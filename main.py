import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.getenv("PREFIX") or "!", intents=intents)
user_id = "prod"

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Bot er online som {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Jasså ja klarer ikke å skrive en enkel komando engang. Skriv !help for å få hjelp")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Vennligst oppgi alle nødvendige argumenter for denne kommandoen.")
    else:
        await ctx.send(f"En feil oppstod: {error}")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Jada",
        description="Dette er det jeg kan:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!help", value="Få hjelp", inline=False)
    embed.add_field(name="!analyser <aksjekode>", value="gjør en analyse av et selskap. eksempel på aksjekode: FRO for Frontline", inline=False)
    await ctx.send(embed=embed)

# router til n8n

@bot.command()
async def analyser(ctx, aksjekode: str = ""):
    url = "https://nn.andreh.dev/webhook/543dfa45-54d4-4498-a523-a971e4bc37d6"

    payload = {
        "code" : aksjekode
    }

    headers = {
        "Content-Type": "application/json"
    }       

    if aksjekode:
        await ctx.send("Sparker analytikerene i gang.")
        requests.post(url, json=payload, headers=headers)
        
    else:
        await ctx.send("Du manglet aksjekode")

print("Starter...")

if not os.getenv("BOT_TOKEN"):
    print("Ingen BOT_TOKEN funnet i .env-filen. Vennligst legg til en gyldig token.")
else:
    print("BOT_TOKEN funnet, starter boten...")
    bot.run(os.getenv("BOT_TOKEN"))
