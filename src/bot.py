from client import Client
from tables import ROLE_JOIN_MSGS
import os

TOKEN = os.getenv("DISCORD_TOKEN2")
COMMAND_PREFIX = ["/"]

ADMIN_ROLE_ID = 738803963041939567

client = Client(command_prefix=COMMAND_PREFIX)

def is_admin(member):
	for role in member.roles:
		if role.id == ADMIN_ROLE_ID:
			return True
	return False

@client.command(name='say', pass_context=True)
async def say(ctx):
	text = ctx.message.content.split(maxsplit=1)[1]
	await ctx.channel.send(text)

@client.command(name='rolejoin')
async def rolejoin(ctx):
	print('doing rolejoin thing')
	await ctx.channel.send("React to any of the following messages to join the corresponding role")

	for role in ctx.message.role_mentions:
		msg = await ctx.channel.send(f" - {role.mention}")
		ROLE_JOIN_MSGS[msg.id] = role.id
		await msg.add_reaction(u"\U0001F44D")

@client.command(name='deletemsg')
async def deletemsg(ctx, count):
	if not is_admin(ctx.message.author):
		await ctx.channel.send("You do not have permission for this command")
		return

	async for msg in ctx.channel.history(limit=int(count) + 1):
		await msg.delete()

client.run(TOKEN)
