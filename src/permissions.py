
ROLE_ADMIN = 738803963041939567

CHANNEL_ASSIGN_ROLES = 738819172846272553
CHANNEL_SUGGESTIONS = 739621224598208556

CATEGORY_PROJECTS = 738890618956415026


async def check_perms(msg, roles=[], channels=[]): # todo, add categories
	if channels and msg.channel.id not in channels:
		# silently fail
		return False

	if not roles:
		return True

	for role in msg.author.roles:
		if role.id in roles:
			return True
	
	await msg.channel.send("You do not have permission for this command")
	return False
