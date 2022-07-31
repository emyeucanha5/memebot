import os
from dotenv import load_dotenv
import discord
import requests
import json

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND = os.getenv('DISCORD_COMMAND_ROOT')
SUBREDDIT_COMMAND = os.getenv('DISCORD_COMMAND_SUBREDDIT')
client = discord.Client()


def getRandomMemes(count):
    try:
        response = requests.get(f"https://meme-api.herokuapp.com/gimme/{count}")
    except error:
        return error
    json_data = json.loads(response.text)
    return json_data

def getRandomMemeFromSubreddits(subReddit, count):
    try:
        response = requests.get(f"https://meme-api.herokuapp.com/gimme/{subReddit}/{count}")
    except error:
        return error
    if(response.status_code == 404):
        return 'fail'
    json_data = json.loads(response.text)
    return json_data

def checkLinkDie(link):
    try:
        response = requests.get(link)
    except :
        return False
    if(response.status_code == 404):
        return False
    return True

    
@client.event
async def on_message(message):
    if (message.content == COMMAND):
        randomMeme = getRandomMemes(1)['memes'][0]
        while(checkLinkDie(randomMeme['url']) == False):
            randomMeme = getRandomMemes(1)['memes'][0]
            
        await message.channel.send(randomMeme['url'])
        
    if(message.content.startswith(COMMAND + ' ') and len(message.content) <= len(COMMAND) + 2 and message.content[9].isnumeric()):
       randomMemes = getRandomMemes(int(message.content[9]))['memes']
       randomMemesImageLink = [e['url'] for e in randomMemes]
       for link in randomMemesImageLink:
           if(checkLinkDie(link)==False):
            continue;
           else:
            await message.channel.send(link)
            
    if(message.content.startswith(SUBREDDIT_COMMAND)):
        subreddit = message.content[len(SUBREDDIT_COMMAND)+1:]
        randomMeme = getRandomMemeFromSubreddits(subreddit,1)
        if(isinstance(randomMeme, str)):
            await message.channel.send('Sub reddit is not found')
            return
        randomMemeSubReddit = randomMeme['memes'][0];
        while(checkLinkDie(randomMemeSubReddit['url']) == False):
            randomrandomMemeSubRedditMeme = getRandomMemeFromSubreddits(subreddit,1)['memes'][0]
        await message.channel.send(randomMemeSubReddit['url'])   
    
client.run(TOKEN)
