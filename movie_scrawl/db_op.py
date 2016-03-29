#-*- encoding:utf-8 -*-
from pymongo import MongoClient

class DBOperation(object):
	def __init__(self, host, port):
		self.host = host
		self.prot = port
	
	def get_client(self):
		pass
