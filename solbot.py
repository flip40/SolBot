import discord
import asyncio
import json
import os

client = discord.Client()

@client.event
async def on_read():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith('!test'):
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1

		await client.edit_message(tmp, 'You have {} message.'.format(counter))
	elif message.content.startswith('!sleep'):
		await asyncio.sleep(5)
		await client.send_message(message.channel, 'Done sleeping')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token')) as token_file:
	token = json.load(token_file)['token']
client.run(token)
