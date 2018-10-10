# Work with Python 3.6
import discord
import requests
import re
import datetime
import asyncio
from bs4 import BeautifulSoup

url = "https://menus.calpolycorporation.org/805kitchen/"
# hdr = {'User-Agent':'Mozilla/5.0',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# for s in soup.find_all('p'):
#     print(s.get_text())
# s = ''
# for item in soup.find_all('p'):
#     print(item.format())

TOKEN = 'insert bot token here'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!805'):
        msgs = get_message_list()
        for msg in msgs:
            await client.send_message(message.channel, msg)


async def scheduled_message():
    await client.wait_until_ready()
    channel = discord.Object(id='insert channel id here')
    while not client.is_closed:
        t = datetime.datetime.now()
        if t.hour == 8 and t.minute == 5:
            msgs = get_message_list()
            for msg in msgs:
                await client.send_message(channel, msg)
        await asyncio.sleep(60)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def get_message_list():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    msg = ''
    lst = []
    for s in soup.find_all(['h2', 'h4', 'p']):
        premsg = s.get_text()
        premsg = premsg.replace('\t', '')
        premsg = re.sub('\n+', '', premsg)
        premsg = premsg.strip()
        if s.name == 'h2':
            premsg = '\n**' + premsg + '**'
        elif s.name == 'h4':
            premsg = '\n\t*' + premsg + '*'
        elif s.name == 'p':
            premsg = '\t\t' + premsg
            for img in s.find_all('img'):
                if img['alt'] == 'Vegetarian':
                    premsg += ' <:vegetarian:499693084117041153>'
                if img['alt'] == 'Vegan':
                    premsg += ' <:vegan:499693108825554945>'
        premsg += '\n'
        msg += premsg
        if len(msg) > 1900:
            lst.append(msg)
            msg = ''
    if len(msg) > 0:
        lst.append(msg)
    return lst


client.loop.create_task(scheduled_message())
client.run(TOKEN)