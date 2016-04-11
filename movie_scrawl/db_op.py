#-*- encoding:utf-8 -*-
from pymongo import MongoClient
import MySQLdb
import ConfigParser

def singleton(cls, *args, **kw):
	instances = {}
	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]
	return _singleton

@singleton
class MongoDBO(object):
	def __init__(self):
		conf = ConfigParser.ConfigParser()
		conf.read('pro.cfg')
		self._host = conf.get('mongo_config', 'host')
		self._port = int(conf.get('mongo_config', 'port'))
		self._db_name =  conf.get('mongo_config', 'db_name')
		self._client = MongoClient(self._host, self._port)
		self.db = getattr(self._client, self._db_name)

@singleton
class MySQLDBO(object):
	def __init__(self):
		conf = ConfigParser.ConfigParser()
		conf.read('pro.cfg')
		self._host = conf.get('mysql_config', 'host')
		self._user_name = conf.get('mysql_config', 'user_name')
		self._password = conf.get('mysql_config', 'password')
		self._db_name = conf.get('mysql_config', 'db_name')
		self.mysql_db = MySQLdb.connect(self._host, self._user_name, self._password, self._db_name)

if __name__ == '__main__':
	db_1 = MongoDBO()
	db_2 = MongoDBO()
	db_3 = MySQLDBO()
	db_4 = MySQLDBO()
	print id(db_1)
	print id(db_2)
	print id(db_3)
	print id(db_4)
