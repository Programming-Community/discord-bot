from client import Client
from tables import ROLE_JOIN_MSGS
from permissions import *
import re
import os

TOKEN = os.getenv("DISCORD_TOKEN2")
COMMAND_PREFIX = ["/"]

client = Client(command_prefix=COMMAND_PREFIX)

@client.command(name='say', pass_context=True)
async def say(ctx):
	text = ctx.message.content.split(maxsplit=1)[1]
	await ctx.channel.send(text)

@client.command(name='rolejoin')
async def rolejoin(ctx):
	if not await check_perms(ctx.message, roles=[ROLE_ADMIN], channels=[CHANNEL_ASSIGN_ROLES]):
		return

	await ctx.channel.send("React to any of the following messages to join the corresponding role")

	for role in ctx.message.role_mentions:
		msg = await ctx.channel.send(f" - {role.mention}")
		ROLE_JOIN_MSGS[msg.id] = role.id
		await msg.add_reaction(u"\U0001F44D")

@client.command(name='deletemsg')
async def deletemsg(ctx, count):
	if not await check_perms(ctx.message, roles=[ROLE_ADMIN]):
		return

	async for msg in ctx.channel.history(limit=int(count) + 1):
		await msg.delete()

@client.command(name='suggest')
async def suggest(ctx):
	if not await check_perms(ctx.message, channels=[CHANNEL_SUGGESTIONS]):
		return

	suggestion = ctx.message.content.split(maxsplit=1)[1]
	title = re.sub(r"[^\w\-]", "", re.sub(r" +", "-", suggestion)) # alphanumeric + "_" and "-"

	if len(title) > 20:
		await ctx.channel.send("Project title must be no more than 20 characters")
		return

	category = client.get_channel(CATEGORY_PROJECTS)
	project_channel = await category.create_text_channel(title)

	await project_channel.send(
f"This channel is for discussion of the {project_channel.name} project. Here you can hash out requirements, scope, etc., \
before diving into the project itself and writing any code. \n\
Refer to the channels under `Help` and `Templates` for info on setting up your team \
using any of our provided templates. Of course, they are entirely optional, and exist solely \
to help you team get started.")
	
	msg = await ctx.channel.send(f"React to this message to vote for \"{title}\". Checkout {project_channel.mention} for discussion")
	await msg.add_reaction(u"\U0001F44D")

client.run(TOKEN)
