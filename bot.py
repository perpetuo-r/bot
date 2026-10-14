import discord
import asyncio
import random
from discord.ext import commands

from bot_logic import gen_pass
from config import TOKEN
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def password(ctx, size=10):
    await ctx.send(gen_pass(size))

@bot.command()
async def shitpost(ctx):
    escolha = random.choice(os.listdir('memes'))
    with open(f'memes/{escolha}', 'rb') as f:  # noqa: ASYNC230
        image = discord.File(f)
    await ctx.send(file=image)

@bot.command()
async def larp(ctx):

    text = "***EXCUSE ME SIR***"

    with open(f"sounds/larp.mp3", "rb") as f:
        sound = discord.File(f)
        await ctx.send(text, file=sound)

@bot.command()
async def larp_call(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Você precisa estar em um canal de voz!")
        return

    channel = ctx.author.voice.channel


    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        voz = await channel.connect()
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)
        voz = voice_client
    else:
        voz = voice_client

    caminho_audio =  "sounds/larp.mp3"

    if voz.is_playing():
        voz.stop()
        
    voz.play(discord.FFmpegPCMAudio(caminho_audio))

    while voz.is_playing():
        await asyncio.sleep(1)
    await voz.disconnect()


bot.run(TOKEN)