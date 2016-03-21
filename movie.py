#-*- encoding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re

start_page = 'bbs.hd62.com/form-12-'

class MovieCatcher(object):
	def __init__(self):
		self.url_head = 'http://bbs.hd62.com/'
		self.parsed_urls = []
		self.download_link = []
	
	def walk_pages(self, start_page, num):
		for i in xrange(1, num+1):
			page_url = start_page + str(i) + '.html'
			print 'start walk page %s'%i
			self.walk_page(page_url)
	
	def walk_page(self, page_url):
		response = requests.get(page_url)
		if not response.status_code == 200: return
		content = response.content
		content_soup = BeautifulSoup(content, 'html.parser')
		links = content_soup.find_all('a', href=re.compile('thread-(.*).html'))
		for link in links:
			url = self.url_head + link['href']
			if url in self.parsed_urls:continue
			print 'start walk url %s'%link['href']
			self.parsed_urls.append(url)
			response = requests.get(url)
			response.encoding = 'UTF-8'
			if not response.status_code == 200:continue
			content = response.content
			self.parse_content(content)
	
	def parse_content(self, content):
		print 'start parse content'
		soup = BeautifulSoup(content, 'html.parser')
		score_tag = soup.find(text=re.compile('(.*?)from(.*?)users'))
		if not score_tag: return
		print score_tag.string.replace(u'\xa0', '')
		download_tag = soup.find('a', href=re.compile("pan.baidu.com"))
		if not download_tag: return
		link = download_tag['href']
		if link in self.download_link:return
		self.download_link.append(link)
		self.process_download_link(link)

	def process_download_link(self, link):
		response = requests.get(link)
		if not response.status_code == 200: return



def test_case():
	mc = MovieCatcher()
	start_url = 'http://bbs.hd62.com/forum-12-'
	mc.walk_pages(start_url, 1)

if __name__ == '__main__':
	test_case()
