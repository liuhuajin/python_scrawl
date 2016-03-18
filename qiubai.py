#-*- coding:UTF-8 -*-
import urllib2
import re
import threading

class MyThread(threading.Thread):
	def __init__(self):
		super(MyThread, self).__init__()

	def run(self):
		global file_handle
		global g_mutex
		global count
		result = []
		while True:
			g_mutex.acquire()
			count += 1
			g_mutex.release()
			if count > 200: break;
			data = self.catch_data_from_page(count)
			result.extend(data)
		g_mutex_2.acquire()
		file_handle.writelines(result)
		print '%s catch %s data>>>>>>>>>>>>'%(self.name, len(result))
		g_mutex_2.release()

	def catch_data_from_page(self, page):
		global words
		url = 'http://6our.com/best?&p=' + str(page)
		contents = []
		try: 
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
			headers = {'User-Agent':user_agent}
			request = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request, timeout = 3)
			body = response.read()
			response.close()
			del response
			pattern = re.compile('<div.*?class="content".*?title=".*?".*?id=".*?">(.*?)</div>', re.S)
			items = re.findall(pattern, body)
			def f(x):
				if not words:return True
				for w in words:
					if w in x:
						return True
				return False
			contents = filter(lambda x: f(x), items)
			print '%s catch page %s data success'%(self.name, page)
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				print e.code
			if hasattr(e, 'reason'):
				print e.reason
			print '%s catch page %s data fail'%(self.name, page)
		finally:
			return contents

file_handle = open('shudong.txt', 'w')
words = ['']
g_mutex = threading.Lock()
g_mutex_2 = threading.Lock()
count = 0

def find_hot():
	global count
	pool = []
	for i in xrange(20):
		t = MyThread()
		t.start()
		pool.append(t)
	for t in pool:
		t.join(30)
	file_handle.close()
	print 'finish crawl %s data got'%count

if __name__ == '__main__':
	find_hot()