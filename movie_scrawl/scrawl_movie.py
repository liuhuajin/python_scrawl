#-*- coding:utf-8 -*-
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
        self.pre_link = 'bt0.com'
        self.retry_list = []
        self.mongo_db = db_op.MongoDBO() 
        self.mysql_db = db_op.MySQLDBO()
        self.cursor = self.mysql_db.db.cursor()
        self.cursor.execute('drop table if exists movie_info')
        sql = 'create table movie_info (name char(100), link char(100), tag char(30), size decimal(8,3), actors varchar(500)) default charset=utf8'
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
                link = (self.pre_link + movie.a['href']).encode('utf-8')
                spans = movie.a.find_all('span')    
                tag = spans[0].text.encode('utf-8')
                size_str = spans[1].text.encode('utf-8')
                size = self.get_size_from_str(size_str)
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

    def get_size_from_str(self, size_str):
        size = 0
        try:
            size_pattern = re.compile('(\d+\.*\d*)(.*)')
            match = size_pattern.match(size_str)
            if match:
                size = float(match.groups()[0])
                size_type = match.groups()[1]
                if 'm' in size_type or 'M' in size_type:
                    size /= 1000
        except:
            pass
        finally:
            print size
            return size

    def save_movie(self, movie_attr_list):
        for movie_attr in movie_attr_list:
            try:
                attr_format = [MySQLdb.escape_string(attr) if type(attr) == str else attr for attr in movie_attr]
                sql = " insert movie_info (name, link, tag, size, actors)\
                values\
                ('%s', '%s', '%s', '%d', '%s') "%(attr_format[0], attr_format[1], attr_format[2], attr_format[3], attr_format[4])
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
