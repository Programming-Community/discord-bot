
ROLE_ADMIN = 738803963041939567

CHANNEL_ASSIGN_ROLES = 738819172846272553
CHANNEL_SUGGESTIONS = 739621224598208556
CHANNEL_TESTING = 739578107115339796

CATEGORY_PROJECTS = 738890618956415026


async def check_scope_perms(msg, channels, categories):
	category_id = getattr(getattr(msg, 'category', None), 'id', None)

	return not ((channels or categories) and
		(not channels or msg.channel.id not in channels) and
		(not categories or category_id not in categories))

async def check_role_perms(msg, roles):
	if not roles:
		return True

	for role in msg.author.roles:
		if role.id in roles:
			return True
	return False
