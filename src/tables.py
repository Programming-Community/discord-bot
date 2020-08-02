from collections import UserDict
import pickle

class KVStore(UserDict):
	def __init__(self, path):
		self.path = path
		super().__init__()

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.write()

	def write(self):
		with open(self.path, 'wb') as f:
			pickle.dump(self.data, f)

ROLE_JOIN_MSGS = KVStore('./tables/role-joins.pkl')
USER_LAST_ACTIVE = KVStore('./tables/last-active.pkl')
