from asyncore import read
from operator import truediv
import discord
import random
import os
from discord.ext import commands
import asyncio
from os.path import exists


client = commands.Bot(command_prefix= '.')


@client.event
async def on_ready():
        print('Bot is online')


async def ch_pr():
    await client.wait_until_ready()

    statuses = [f'over {len(client.guilds)} servers | .help', f'{round(client.latency * 1000)}ms | .help', f'your mom | .help']
    while not client.is_closed():
        status = random.choice(statuses)

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        await asyncio.sleep(5)


@client.command()
async def ping(ctx):
    await ctx.send(f'Ping: {round(client.latency * 1000)}ms')

@client.command(aliases=['set'])
async def set_channel_id(ctx, channelid:int):
    if ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.administrator:

        guildid = ctx.guild.id
        channelname = await client.fetch_channel(channelid)
        await ctx.channel.send(f'**{channelname}** has been set to reconnect channel.')
        with open(f'{guildid}.txt', 'w') as f:
            f.write(str(channelid))
    else:
        ctx.channel.send(f'Insufficient permissions.')

#with open('id.txt', 'r') as f:
    #f_contents = f.read()
    #globalchannel = int(f_contents)

@client.command()
async def id(ctx):
    guildid = ctx.guild.id
    with open(f'{guildid}.txt', 'r') as f:
        f_contents = f.read()
        globalchannel = int(f_contents)
    send = globalchannel
    await ctx.send(f'ID of reconnect channel is set to {send}')

@client.command(aliases=['rc'])
async def reconnect(ctx, member: discord.Member=None):
        if ctx.author.guild_permissions.move_members or ctx.author.guild_permissions.administrator:

            guildid = ctx.guild.id
            file_exists = exists(f'{guildid}.txt')
            if file_exists == True:
                with open(f'{guildid}.txt', 'r') as f:
                    f_contents = f.read()
                    globalchannel = int(f_contents)
                if member == None:  
                    member = ctx.message.author
                channel2 = ctx.message.author.voice.channel
                channel1 = await client.fetch_channel(globalchannel)
                await member.move_to(channel1)
                await member.move_to(channel2)
            else:
                await ctx.channel.send(f'Channel ID not set, use **.set**.')
        else:
            await ctx.channel.send(f'Insufficient permissions.')


client.loop.create_task(ch_pr())
client.run('OTk0MzYxMDQ0MzU5MTg0NDg1.GEwHdD.fhFI86TqlNXJUEJgN8nUClwU_Cs4qfVnKw_iUg')
