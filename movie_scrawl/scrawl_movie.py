#-*- encoding:utf-8 -*-
import requests
import threadpool
import db_op
from bs4 import BeautifulSoup
import sys
import re

class MovieScrawl(object):
	def __init__(self, url, pages):
		self.start_url = url
		self.total_pages = pages
		self.retry_list = []
		self.mongo_db = db_op.MongoDBO() 
		self.mysql_db = db_op.MySQLDBO()
		self.cursor = self.mysql_db.db.cursor()
		self.cursor.execute('drop table if exists movie_info')
		sql = 'create table movie_info (name char(100), des char(200), link char(100), tag char(30), size char(30))'
		self.cursor.execute(sql)
	def scrawl_url(self, url):
		try:
			print 'start scrawl %s'%url
			url_response = requests.get(url, timeout=5)
			if not url_response.status_code == 200:
				self.retry_list.append(url)
			else:
				content = url_response.content
				self.parse_content(content)
		except:
			import traceback
			traceback.print_exc()
			self.retry_list.append(url)
	
	def parse_content(self, content):
		soup = BeautifulSoup(content, 'html.parser')
		movie_list = soup.find_all('div',class_='home-list-item-left')
		for movie in movie_list:
			link = movie.a['href']
			spans = movie.a.find_all('span')	
			tag = spans[0].text
			size = spans[1].text
			name_and_actors = movie.p.text
			pattern = re.compile(u'影片名称: (.*)  - 主演：(.*)')
			match = pattern.match(name_and_actors)
			try:
				name = match.groups()[0]
				actors = match.groups()[1]
				print '--------'
				print name
				print actors
			except:
				pass

	def start_scrawl(self):
		pool = threadpool.ThreadPool(8)
		urls = [self.start_url%page for page in xrange(1, self.total_pages+1)]
		reqs = threadpool.makeRequests(lambda url:self.scrawl_url(url), urls)
		[pool.putRequest(req) for req in reqs]
		pool.wait()


if __name__ == '__main__':
	url = 'http://www.bt0.com/list/0-0-0-0-%s.html'
	pages = 1
	movie_scrawl = MovieScrawl(url, pages)
	movie_scrawl.start_scrawl()
