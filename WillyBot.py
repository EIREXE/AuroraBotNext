import discord
from pybooru import Pybooru
from musicbot.config import Config, ConfigDefaults

import urllib.request
import urllib.parse
import re
import random
import praw
import requests
import json
import asyncio

r = praw.Reddit(user_agent='Aurora @ Discord')
client = discord.Client()
help_file = open('help.txt', 'r');
help_file = help_file.read();
william_file = open('sargisson.txt', encoding='utf-8');
william_lines = william_file.readlines();
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('.hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    if message.content.startswith('.hentai'):
        content = message.content[7:];
        content = content.split(' ');
        url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=sort:score+sort:score+rating:explicit" + '+'.join(content);

        resp = requests.get(url=url)
        data = json.loads(resp.text)
        image = random.choice(data)
        await client.send_message(message.channel, image["file_url"] + "\n " + image["tags"])
    if message.content.startswith('.youtube'):
        content = message.content[8:];
        query_string = urllib.parse.urlencode({"search_query" : content});
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string);
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode());
        await client.send_message(message.channel, "http://www.youtube.com/watch?v=" + search_results[0]);
    if message.content.startswith('.syncvideo'):
        await client.send_message(message.channel, "https://www.watch2gether.com/rooms/icrash-fr5405bt3f33m573")
    if message.content.startswith('.help'):
        await client.send_message(message.author, help_file);
    if message.content.startswith('.william'):
        content = message.content[8:];
        if(content.strip() == "help"):
            final_message = list();
            final_message.append("**WillyBot citas de sargisson**\n")
            for line in william_lines:
                final_message.append(str(william_lines.index(line)+1) + " - " + line);
            await client.send_message(message.author, "".join(final_message));
            return;
        if(content.strip() != ""):
            value = int(content);
            await client.send_message(message.channel, william_lines[value-1], tts=True);

        else:
            await client.send_message(message.channel, random.choice(william_lines), tts=True);
    if message.content.startswith('.h3h3'):

        messages = list();
        submissionsLength = 50;
        submissionLengthI = 0;
        while(len(messages) < submissionsLength):
            submissionsLengthI = submissionLengthI + 5;
            submissions = r.get_subreddit('h3h3productions').get_hot(limit=50, is_self=False);
            for x in submissions:
                if(x.is_self == False):
                    messages.append(x);
        await client.send_message(message.channel, random.choice(messages).url);
@client.event
async def on_ready():
    wprint('WillyBot is on startup')
    wprint('Logged in as:')
    wprint(client.user.name)
    wprint(client.user.id)
    wprint('------')

def wprint(message):
    print("WillyBot: ",message)

client.run("")
