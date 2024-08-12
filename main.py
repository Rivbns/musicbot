import discord
from settings import settings
from discord import FFmpegPCMAudio
import os
import youtube_dl
from urllib import parse, request
import re
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="Sancochanos.exe"))

@bot.event
async def on_ready():
    print("Hola Sancochano")

@bot.command(pass_context=True)
async def connect(ctx):
    canal = ctx.author.voice
    if (ctx.author.voice):
        canal = ctx.message.author.voice.channel
    else:
        await ctx.send("Primero conectate a un canal de voz puem")
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz = await canal.connect()
@bot.command(pass_context=True)
async def disconnect(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("me fui")
    else:
        await ctx.send("No estoy en ningun canal de voz, locazo/a")

@bot.command(pass_context=True)
async def play(ctx, url:str):
    """query_string = parse.urlencode({"search_query" : search})
    html_content = request.urlopen("http://www.youtube.com/results?" + query_string)
    re.findall('href=\"\\/watch\\?v=(.{11})')"""

    cancionactiva = os.path.isfile("cancion.mp3")
    try:
        if cancionactiva:
            os.remove("cancion.mp3")
            print("se fue")
    except PermissionError:
        print ("Hay una canción reproduciendose")
        await ctx.send("Error:Cancion reproduciendose")
        return
    await ctx.send("Todo listo")

    voz = get(bot.voice_clients,guild=ctx.guild)

    ydl_op = {
        "format" : "bestaudio/best",
        "postprocessors" : [{
            "key" : "FFmpegExtractAudio",
            "preferredcodec" : "mp3",
            "preferredquality" : "192",
        }],
    }

    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        print("Descargar Cancion")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name2 = file
            print(f"Renombrando Archivo: {file}")
            os.rename(file, "cancion.mp3")

    voz.play(discord.FFmpegPCMAudio("cancion.mp3"))
    voz.source = discord.PCMVolumeTransformer(voz.source)
    voz.source.volume = 0.06

    nombre = name2.rsplit("-",2)
    await ctx.send(f"reproduciendo: {nombre[0]}")
bot.run(settings["TOKEN"])
