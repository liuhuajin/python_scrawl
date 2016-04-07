#-*- encoding:utf-8 -*-
from pymongo import MongoClient
import ConfigParser

def singleton(cls, *args, **kw):
	instances = {}
	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]
	return _singleton

@singleton
class DBOperation(object):
	def __init__(self):
		conf = ConfigParser.ConfigParser()
		conf.read('pro.cfg')
		self._host = conf.get('db_config', 'host')
		self._port = int(conf.get('db_config', 'port'))
		self._db_name =  conf.get('db_config', 'db_name')
		self._client = MongoClient(self._host, self._port)
		self.db = getattr(self._client, self._db_name)

if __name__ == '__main__':
	db_1 = DBOperation()
	db_2 = DBOperation()
	print id(db_1)
	print id(db_2)
