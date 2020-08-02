from discord.ext.commands import Bot
import os

TOKEN = os.getenv("DISCORD_TOKEN2")
BOT_PREFIX = ["/"]

class CustomBot(Bot):
	
	async def on_ready(self):
		print(f"{self.user.name} now connected")

	async def on_message(self, message):
		if message.author == self.user:
			return

		print('said something')
		await super().on_message(message)

	async def on_raw_reaction_add(self, payload):
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)

		channel = self.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)


client = CustomBot(command_prefix=BOT_PREFIX)

@client.command(
			name='say',
			description='Repeat phrase back to user',
			aliases=['announce', 'broadcast'],
			pass_context=True)
async def say_command(context):
	channel = context.message.channel
	text = context.message.content.split(maxsplit=1)[1]
	await channel.send(text)


client.run(TOKEN)
