import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)

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
    embed.add_field(name="!rapport", value="Gjør en ny rapport samme som dagelig", inline=False)
    embed.add_field(name="!rapport <aksje>", value="Gjør en rapport for en aksje", inline=False)
    embed.add_field(name="!legg til <aksjekode>", value="Legger til en aksje i overvåkningslisten eksempel på aksjekode: FRO for Frontline", inline=False)
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
    if aksjekode:
        await ctx.send(f"Aksjen du skrev er: {aksjekode} men å legge ting i overvåkning er ikke en ting enda.")
    else:
        await ctx.send("Vennligst oppgi en aksjekode for å legge til i overvåkningslisten.")

@bot.command()
async def fjern(ctx, aksjekode: str = None):
    if aksjekode:
        await ctx.send(f"Aksje {aksjekode} kan ikke fjernes siden det ikke er implementert en fjern funksjonn.")
    else:
        await ctx.send("Vennligst oppgi en aksjekode for å fjerne fra overvåkningslisten.")

@bot.command()
async def list(ctx):
    # Placeholder for the list command
    await ctx.send("Dette er overvåkningslisten: \n1. FRO - Frontline\n2. DNB - DNB ASA\n3. EQNR - Equinor ASA (bare et eksempel da)")

print("Starter...")

if not os.getenv("BOT_TOKEN"):
    print("Ingen BOT_TOKEN funnet i .env-filen. Vennligst legg til en gyldig token.")
else:
    print("BOT_TOKEN funnet, starter boten...")
    bot.run(os.getenv("BOT_TOKEN"))
