#-*- encoding:utf-8 -*-
from pymongo import MongoClient

def singleton(cls, *args, **kw):
	instances = {}
	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]
	return _singleton

@singleton
class DBOperation(object):
	def __init__(self, host, port):
		self._host = host
		self._prot = port
		self._db_name = dbname
		self._client = MongoClient(self._host, self._port)
		self.db = getattr(self._client, self._db_name)
