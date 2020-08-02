from client import Client
import os

TOKEN = os.getenv("DISCORD_TOKEN2")
COMMAND_PREFIX = ["/"]

client = Client(command_prefix=COMMAND_PREFIX)

@client.command(name='say', pass_context=True)
async def say_command(context):
	channel = context.message.channel
	text = context.message.content.split(maxsplit=1)[1]
	await channel.send(text)

client.run(TOKEN)
