import discord
import asyncio
import json
import os
import sys
from git import Git
import re

client = discord.Client()
sleeping = False

@client.event
async def on_ready():
	await client.send_message(client.get_channel('199025108713603072'), 'SolBot online!')

@client.event
async def on_message(message):
	if sleeping:
		if message.content == '!wake':
			sleeping = False
			await client.send_message(message.channel, 'SolBot online!')
	else:
		if message.content == '!test':
			counter = 0
			tmp = await client.send_message(message.channel, 'Calculating messages...')
			async for log in client.logs_from(message.channel, limit=100):
				if log.author == message.author:
					counter += 1

			await client.edit_message(tmp, 'You have {} message.'.format(counter))
		elif message.content == '!sleep':
			sleeping = True
			await client.send_message(message.channel, 'Going to sleep...')
		elif message.content == '!update':
			g = Git(os.path.dirname(os.path.abspath(__file__)))
			tmp = await client.send_message(message.channel, 'Pulling new code...')
			g.pull()
			await client.edit_message(tmp, 'Code pulled. Restarting...')
			client.logout()
			os.execv(sys.executable, ['python3.5'] + sys.argv)
		elif message.content == '!gitstatus':
			g = Git(os.path.dirname(os.path.abspath(__file__)))
			tmp = await client.send_message(message.channel, 'Checking status...')
			g.fetch()
			p = re.compile('Your branch is.*by (\d+) commits.*')
			m = p.match(g.status())
			if m:
				await client.edit_message(tmp, 'I am behind by {} commits'.format(m.group(1)))
			else:
				await client.edit_message(tmp, 'I am up to date!')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token')) as token_file:
	token = json.load(token_file)['token']
client.run(token)
