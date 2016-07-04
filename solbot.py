import discord
import asyncio
import json
import os
import sys
from git import Git

client = discord.Client()

@client.event
async def on_read():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content == '!test':
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1

		await client.edit_message(tmp, 'You have {} message.'.format(counter))
	elif message.content == '!sleep':
		await asyncio.sleep(5)
		await client.send_message(message.channel, 'Done sleeping')
	elif message.content == '!update':
		g = Git(os.path.dirname(os.path.abspath(__file__)))
		tmp = await client.send_message(message.channel, 'Pulling new code...')
		g.pull()
		await client.edit_message(tmp, 'Code pulled. Restarting...')
		client.logout()
		os.execv(sys.executable, ['python3.5'] + sys.argv)
	elif message.content == '!testingselfupdate':
		await client.send_message(message.channel, 'Success!')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token')) as token_file:
	token = json.load(token_file)['token']
client.run(token)
