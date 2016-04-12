import requests
import threadpool

class MovieScrawl(object):
	def __init__(self, url, pages):
		self.start_url = url
		self.total_pages = pages
	
	def scrawl_url(self, url):
		try:
			print 'start scrawl %s'%url
			url_response = requests.get(url, timeout=5)
			if not url_response.status_code == 200:
                            self.retry_list.append(url)
                        else:
                            content = url_response.content
                            soup = BeautifulSoup(content, 'html.parser')
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
	pages = 15
	movie_scrawl = MovieScrawl(url, pages)
	movie_scrawl.start_scrawl()
