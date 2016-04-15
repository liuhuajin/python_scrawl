#-*- encoding:utf-8 -*-
import requests
import threadpool
import db_op
from bs4 import BeautifulSoup
import re
import MySQLdb

class MovieScrawl(object):
    def __init__(self, url, pages):
        self.start_url = url
        self.total_pages = pages
        self.retry_list = []
        self.mongo_db = db_op.MongoDBO() 
        self.mysql_db = db_op.MySQLDBO()
        self.cursor = self.mysql_db.db.cursor()
        self.cursor.execute('drop table if exists movie_info')
        sql = 'create table movie_info (name char(100), link char(100), tag char(30), size char(30), actors varchar(500))'
        self.cursor.execute(sql)
        self.mysql_db.db.commit()
    def scrawl_url(self, url):
        try:
            print 'start scrawl %s'%url
            url_response = requests.get(url, timeout=5)
            if not url_response.status_code == 200:
                self.retry_list.append(url)
            else:
                content = url_response.content
                movie_attr_list = self.parse_content(content)
                self.save_movie(movie_attr_list)
        except:
            import traceback
            traceback.print_exc()
            self.retry_list.append(url)
    
    def parse_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        movie_list = soup.find_all('div',class_='home-list-item-left')
        movie_attr_list = []
        for movie in movie_list:
            link = None
            tag = None
            size = None
            name = None
            actors = None
            try:
                link = movie.a['href'].encode('utf-8')
                spans = movie.a.find_all('span')    
                tag = spans[0].text.encode('utf-8')
                size = spans[1].text.encode('utf-8')
                name_and_actors = movie.p.text
                pattern = re.compile(u'影片名称: (.*)  - 主演：(.*)')
                match = pattern.match(name_and_actors)
                name = match.groups()[0].encode('utf-8')
                actors = match.groups()[1].encode('utf-8')
            except:
                import traceback
                traceback.print_exc()
            finally:
                movie_attr = [name, link, tag, size, actors] if link and tag and size and name and actors else []
            if movie_attr:
                movie_attr_list.append(movie_attr)
        return movie_attr_list

    def save_movie(self, movie_attr_list):
        for movie_attr in movie_attr_list:
            try:
                attr_format = [MySQLdb.escape_string(attr) for attr in movie_attr]
                sql = " insert movie_info (name, link, tag, size, actors)\
                values\
                ('%s', '%s', '%s', '%s', '%s') "%(attr_format[0], attr_format[1], attr_format[2], attr_format[3], attr_format[4])
                self.cursor.execute(sql)
                self.mysql_db.db.commit()
            except:
                import traceback
                traceback.print_exc()
                self.mysql_db.db.rollback()

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
