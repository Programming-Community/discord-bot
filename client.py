from discord.ext.commands import Bot

class Client(Bot):
	async def on_ready(self):
		print(f"{self.user.name} now connected")

	async def on_message(self, message):
		if message.author == self.user:
			return

		# TODO update message.author 's last_active ts

		await super().on_message(message)

	async def on_raw_reaction_add(self, payload):
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)

		channel = self.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)

		# TODO check if msg.id is a role-join, and if so add user to role
	
	async def on_raw_reaction_remove(self, payload):
		guild = self.get_guild(payload.guild_id)
		user = guild.get_member(payload.user_id)

		channel = self.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)
		
		# TODO check if msg.id is a role-join, and if so remove user from role
