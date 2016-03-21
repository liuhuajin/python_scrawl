#-*- coding:utf-8 -*-
import requests
import re
import threadpool
import functools
from bs4 import BeautifulSoup

class ImageCatcher(object):
	def __init__(self, email, password):
		self.email = email
		self.password = password
		self.s = self.login_user()
		self.parsed_url = []
	
	def login_user(self):
		s = requests.session()
		login_data = {'email': self.email, 'password': self.password}
		s.post('http://www.zhihu.com/login', login_data)
		print 'login in'
		return s
	
	def get_search_result(self, key_word):
		url = 'http://www.zhihu.com/search?type=content&q=' + key_word
		search_result = None
		try:
			search_result = self.s.get(url)
		except Exception,e:
			pass
		finally:
			if not search_result or not search_result.status_code == 200: return
		print 'get search_result successful'
		search_content = search_result.content
		search_soup = BeautifulSoup(search_content, 'lxml')
		results = search_soup.find_all('a')
		for r in results:
			if r.get('target') == '_blank' and r.get('class') and r.get('class')[0] == 'js-title-link':
				href = r.get('href')
				print href
				if not re.match('/question/', href): continue
				answer_url = 'http://www.zhihu.com' + href
				self.get_image_contents(answer_url)
	
	def get_image_contents(self, url):
		r = None
		try:
			r = self.s.get(url)
		except Exception, e:
			pass
		finally:
			if not r or not r.status_code == 200: return
		content = r.content
		soup = BeautifulSoup(content, 'lxml')
		images = soup.find_all('img')
		i = 0
		for image in images:
			image_path = image.get('data-original')
			name = './image/' + url[-8:]+ '_' + str(i) + '.jpg'
			self.save_image(image_path, name)			
			i += 1

	def save_image(self, image_path, name):
		if image_path:
			if image_path in self.parsed_url:return
			self.parsed_url.append(image_path)
			image_response = requests.get(image_path)
			if not image_response.status_code == 200: return False
			image_content = image_response.content
			if not image_content: return False
			with(open(name, 'wb')) as f:
				f.write(image_content)
			print 'save %s success'%name
			return True	

def testcase():
	key_word = ''
	my_catcher = ImageCatcher('address@mail.com', 'password')
	my_catcher.get_search_result(key_word)	

if __name__ == '__main__':
	testcase()
