import requests

class MovieScrawl(object):
	def __init__(self, url, pages):
		self.start_url = url
		self.total_pages = pages
	
	def scrawl_url(self, url):
		try:
			print 'start scrawl %s'%surl
			url_response = requests.get(url, timeout=5)
			
		except:
			pass
	
	def start_scrawl(self):
		pool = threadpool.ThreadPool(8)
		urls = [self.start_url+str(page) for page in xrange(1, self.total_pages+1)]
		reqs = threadpool.makeRequests(lambda url:self.scrawl_url(url), urls)
		[pool.putrequest(req) for req in reqs]
		pool.wait()
