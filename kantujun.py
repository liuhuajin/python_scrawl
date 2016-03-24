import requests
from bs4 import BeautifulSoup
import threadpool
import re

class ImageCatcher(object):
	def __init__(self):
		self.start_url = None
		self.num = 0

	def set_start_url(self, url, num):
		self.start_url = url
		self.num = num
	
	def walk_url(self, url):
		print 'start walk url:%s'%url
		response = requests.get(url)
		name_first = re.search('page=(.*)', url).group(1)
		content = response.content
		soup = BeautifulSoup(content, 'html.parser')
		tags = soup.find_all('img', alt='')
		for tag in tags:
			src = tag.get('src')
			if not src:return
			img_response = requests.get(src)
			name = './image/' + name_first + '_' + src[-13:]
			with open(name, 'wb') as f:
				f.write(img_response.content)
	
	def walks_all(self):
		pool = threadpool.ThreadPool(4)
		urls = [self.start_url + str(page) for page in xrange(1, self.num)]
		reqs = threadpool.makeRequests(lambda url:self.walk_url(url), urls)
		[pool.putRequest(req) for req in reqs]
		pool.wait()

if __name__ == '__main__':
	ic = ImageCatcher()
	url = 'http://www.xxxxx.com/index/douban?page='
	num = 86
	ic.set_start_url(url, num)
	ic.walks_all()