import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import stock_db as db

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)
user_id = "prod"

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Bot er online som {bot.user}")
    stocks = db.get_stocks(user_id)
    stock_list = ", ".join(stocks)
    await bot.change_presence(activity=discord.Game(name=f"Overvåker: {stock_list}"))

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
    embed.add_field(name="!rapport", value="Gjør en ny rapport samme som dagelig", inline=False)
    embed.add_field(name="!rapport <aksje>", value="Gjør en rapport for en aksje", inline=False)
    embed.add_field(name="!legg_til <aksjekode>", value="Legger til en aksje i overvåkningslisten eksempel på aksjekode: FRO for Frontline", inline=False)
    embed.add_field(name="!fjern <aksjekode>", value="Fjerner en aksje fra overvåkningslisten eksempel på aksjekode: FRO for Frontline", inline=False)
    embed.add_field(name="!list", value="Viser overvåkningslisten", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def rapport(ctx, aksjekode: str = None):
    if aksjekode:
        await ctx.send(f"Aksjen du skrev er: {aksjekode} men rapportering er ikke implementert enda.")
    else:
        await ctx.send("Ikke implement enda")

@bot.command()
async def legg_til(ctx, aksjekode: str = None):
    #TODO legg til aksjekode i databasen med stock_db.py
    if aksjekode:
        if aksjekode.isalpha() and len(aksjekode) <= 5:
            db.add_stock(user_id, aksjekode.upper())
            await ctx.send(f"Aksje {aksjekode} lagt til i overvåkningslisten.")
            
            stocks = db.get_stocks(user_id)
            stock_list = ", ".join(stocks)
            await bot.change_presence(activity=discord.Game(name=f"Overvåker: {stock_list}"))
        else:
            await ctx.send("Ugyldig aksjekode. Vennligst oppgi en gyldig aksjekode (kun bokstaver, maks 5 tegn).")
    else:    
        await ctx.send("Vennligst oppgi en aksjekode for å legge til i overvåkningslisten.")

@bot.command()
async def fjern(ctx, aksjekode: str = None):
    stocks = db.get_stocks(user_id)
    if aksjekode in stocks:
        db.remove_stocks(user_id, aksjekode.upper())
        await ctx.send(f"Aksje {aksjekode} fjernet fra overvåkningslisten.")
        stocks = db.get_stocks(user_id)
        stock_list = ", ".join(stocks)
        await bot.change_presence(activity=discord.Game(name=f"Overvåker: {stock_list}"))
    elif not stocks:
        await ctx.send("Du har ingen aksjer i overvåkningslisten å fjerne.")
    elif not aksjekode:
        await ctx.send("Vennligst oppgi en aksjekode for å fjerne fra overvåkningslisten.")
    elif aksjekode not in stocks:
        await ctx.send(f"Aksje {aksjekode} finnes ikke i overvåkningslisten.")

@bot.command()
async def list(ctx):
    stocks = db.get_stocks(user_id)
    if not stocks:
        await ctx.send("Du har ingen aksjer i overvåkningslisten.")
        return
    # Display the stocks in the user's watchlist
    stock_list = "\n - " + "\n - ".join(stocks)
    await ctx.send(f"Din overvåkningsliste:{stock_list}")

print("Starter...")

if not os.getenv("BOT_TOKEN"):
    print("Ingen BOT_TOKEN funnet i .env-filen. Vennligst legg til en gyldig token.")
else:
    print("BOT_TOKEN funnet, starter boten...")
    bot.run(os.getenv("BOT_TOKEN"))
