from client import Client
from tables import ROLE_JOIN_MSGS
from permissions import *
from discord import Embed, Color
from discord.errors import NotFound
from contextlib import suppress
import re
import os

TOKEN = os.getenv("DISCORD_TOKEN2")
COMMAND_PREFIX = ["/"]

client = Client(command_prefix=COMMAND_PREFIX)

COLOR_GREEN = 0x447744
COLOR_RED = 0xAA4444

async def rich_send(channel, text, title=None, color=None):
	color = Color(color) if color else Color.blue() 
	title = title or ""
	embed = Embed(title=title, description=text, color=color)
	return await channel.send('\n', embed=embed)


def command(name, roles=None, channels=None, categories=None, delete_parent=False):
	def decorator(func):
		async def f(ctx, *args, **kwargs):
			channel = ctx.channel
			if not await check_scope_perms(ctx.message, channels, categories):
				return
			if not await check_role_perms(ctx.message, roles):
				await rich_send(channel, "You do not have permissions to run this command", title='Permission Denied', color=COLOR_RED)
				return

			try:
				await func(ctx, *args, **kwargs)
			except Exception as e:
				await rich_send(channel, str(e), title='Internal Error', color=COLOR_RED)
				await ctx.message.add_reaction(u"\u274C")
			else:
				with suppress(NotFound):
					await ctx.message.add_reaction(u"\u2705")
					if delete_parent:
						await ctx.message.delete(delay=3)
		return client.command(name=name)(f)
	return decorator
					
@command(name='say')
async def say(ctx, *args):
	text = ctx.message.content.split(maxsplit=1)[1]
	await rich_send(ctx.channel, text, color=COLOR_GREEN)

@command(name='rolejoin', roles=[ROLE_ADMIN], channels=[CHANNEL_ASSIGN_ROLES])
async def rolejoin(ctx, *args):
	await rich_send(ctx.channel, "React to any of the following messages to join the corresponding role")

	for role in ctx.message.role_mentions:
		msg = await rich_send(ctx.channel, f" - {role.mention}")
		ROLE_JOIN_MSGS[msg.id] = role.id
		await msg.add_reaction(u"\U0001F44D")

@command(name='deletemsg', roles=[ROLE_ADMIN])
async def deletemsg(ctx, count):
	async for msg in ctx.channel.history(limit=int(count) + 1):
		await msg.delete()

@command(name='suggest', channels=[CHANNEL_SUGGESTIONS])
async def suggest(ctx, *args):
	length_limit = 30
	suggestion = ctx.message.content.split(maxsplit=1)[1]
	title = re.sub(r"[^\w\-]", "", re.sub(r" +", "-", suggestion)) # alphanumeric + "_" and "-"

	if len(title) > length_limit:
		await rich_send(ctx.channel, f"Project title must be no more than {length_limit} characters")
		return

	category = client.get_channel(CATEGORY_PROJECTS)
	project_channel = await category.create_text_channel(title)

	await rich_send(project_channel,
f"This channel is for discussion of the {project_channel.name} project. Here you can hash out requirements, scope, etc., \
before diving into the project itself and writing any code. \n\
Refer to the channels under `Help` and `Templates` for info on setting up your team \
using any of our provided templates. Of course, they are entirely optional, and exist solely \
to help you team get started.")
	
	msg = await rich_send(ctx.channel, f"React to this message to vote for \"{title}\". Checkout {project_channel.mention} for discussion")
	await msg.add_reaction(u"\U0001F44D")

client.run(TOKEN)
