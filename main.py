import discord
from settings import settings
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="Sancochanos.exe"))

@bot.event
async def on_ready():
    print("Hola Sancochano")

@bot.command(pass_context=True)
async def connect(ctx):
    canal = ctx.message.author.voice.channel
    if not canal:
        await ctx.send("Primero conectate a un canal de voz puem")
        return
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move.to(canal)
    else:
        voz = await canal.connect()
bot.run(settings["TOKEN"])
