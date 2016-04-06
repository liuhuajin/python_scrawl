#-*- encoding:utf-8 -*-
from pymongo import MongoClient

class DBOperation(object):
	def __init__(self, host, port):
		self.host = host
		self.prot = port
		self.client = None

	def get_client(self):
		self.client = MongoClient('localhost', 3000)
