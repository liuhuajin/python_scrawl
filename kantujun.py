import requests
from bs4 import BeautifulSoup
import threadpool
import re
import os

class ImageCatcher(object):
	def __init__(self):
		self.start_url = None
		self.num = 0

	def set_start_url(self, url, num, path):
		self.start_url = url
		self.num = num
		if not os.path.exists(os.path.join(os.getcwd(),path)):
			os.mkdir(path)
		self.path = path
	
	def walk_url(self, url):
		print 'start walk url:%s'%url
		response = requests.get(url, timeout=3)
		name_first = re.search('page=(.*)', url).group(1)
		content = response.content
		soup = BeautifulSoup(content, 'html.parser')
		tags = soup.find_all('img', alt='')
		for tag in tags:
			src = tag.get('src')
			if not src:return
			img_response = requests.get(src, timeout=3)
			name = self.path + name_first + '_' + src[-13:]
			with open(name, 'wb') as f:
				f.write(img_response.content)
	
	def walks_all(self):
		pool = threadpool.ThreadPool(8)
		urls = [self.start_url + str(page) for page in xrange(1, self.num)]
		reqs = threadpool.makeRequests(lambda url:self.walk_url(url), urls)
		[pool.putRequest(req) for req in reqs]
		pool.wait()

if __name__ == '__main__':
	ic = ImageCatcher()
	url = 'http://www.xxxx.com/index/douban?page='
	num = 86
	path = './image/'
	ic.set_start_url(url, num, path)
	ic.walks_all()
