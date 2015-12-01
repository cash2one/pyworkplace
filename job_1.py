#jobs_coreint
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 

class Handler(BaseHandler):
    crawl_config = {
        
       
    }
    @every(minutes=24*60)
    def on_start(self):
        self.crawl('http://jobs.coreint.org/', callback=self.index_page,age=1*24*60*60)


    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://jobs.coreint.org/\d+$', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page,age=1*24*60*60)
            

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('title').text(),
            "position": response.doc('div.job_title').text(),
            "company": response.doc('div.company_name').text(),
            "fulltime":"",
            "address": response.doc('div.location_preview').html(),
            "url": response.url,
            "scrsys": "jobs_coreint",
            "note": response.doc('div.container>div>div').text(),
            "issuedtime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
            "inserttime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,

        }
    def on_result(self, result):
        print result
        if not result or not result['title']:
            return
        sql = SQL()
        sql.replace('jobs',**result)
        
        
#-----------------------------------------------------------------------------------------------
#jobs_github
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://jobs.github.com/positions', callback=self.index_page)

    def index_page(self, response):
        str1 = response.doc('#page>div>h1').text().replace(' ','').replace('\n','')
        print str1
        pattern = re.compile("of(\d*)jobs")
        res = pattern.search(str1).groups()
        pagNo = int(res[0])/50
        
        self.crawl('https://jobs.github.com/positions?page='+ str(pagNo), callback=self.index_page2,age=1*24*60*60)


    def index_page2(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('https://jobs.github.com/positions/', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page  , age=1*24*60*60)
        for each in response.doc('a[href^="http"]').items():
            if re.match('https://jobs.github.com/companies/', each.attr.href):
                self.crawl(each.attr.href, callback=self.index_page2,   age=1*24*60*60)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('title').text(),
            "position": response.doc('#page>div>h1').text(),
            "company": response.doc('div.column.sidebar>div.module.logo>div>h2').text(),
            "fulltime":response.doc('#page>div>p').text().split('/')[0],
            "address": response.doc('#page>div>p').text().split('/')[1],
            "url": response.url,
            "scrsys": "github",
            "note": response.doc('div.column.main>p:nth-child(1)').text(),
            "issuedtime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
            "inserttime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,

        }
    def on_result(self, result):
        print result
        if not result or not result['title']:
            return
        sql = SQL()
        sql.replace('jobs',**result)

#-----------------------------------------------------------------------------------------------

#larajobs
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 


class Handler(BaseHandler):
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://larajobs.com/api/jobs',
                   callback=self.json_parser, age=1*24*60*60)

    def json_parser(self, response):
  
        return [{
            "title": x['title'],
            "position": x['slug'],
            "company": x['user']['company_name'],
            "fulltime":x['type']['label'],
            "address": (x['location_city'] == "" and ['Remote / Anywhere'] or [x['location_city']])[0] ,
            "url": 'https://larajobs.com/job/'+str(x['id'])+'/'+x['slug'],
            "scrsys": "larajobs",
            "note": x['description'],
            "issuedtime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
            "inserttime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
        } for x in response.json]
    def on_result(self, result):
        print result
        if not result or not result[0]['title']:
            return
        sql = SQL()
        for x in result:
            sql.replace('jobs',**x)
#-----------------------------------------------------------------------------------------------
#remoteok
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 
import datetime


def now(formatstr):
    if formatstr == '':formatstr='%Y-%m-%d %H:%M:%S'
    d1= datetime.datetime.now()
    return d1.strftime(formatstr)

def calctime(value):
    d1= datetime.datetime.now()
    if value.find('d')>0:
        day = int(value.replace('d',''))
        return (d1 +datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
    elif value.find('h')>0:
        hour = int(value.replace('h',''))
        return (d1 +datetime.timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return d1.strftime('%Y-%m-%d %H:%M:%S')

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://remoteok.io/', callback=self.index_page, age=1*24*60*60)



    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('https://remoteok.io/remote-jobs/(\d*)-', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page, age=1*24*60*60)



    @config(priority=2)
    

    def detail_page(self, response):
        getTime = response.doc('td.time>a').text()
        print getTime
        return {
            "title": response.doc('title').text(),
            "position": response.doc('div.description>div:nth-child(2)').text(),
            "company": response.doc('div.description>div:nth-child(1)>a').text(),
            "fulltime":'',
            "address": '',
            "url": response.url,
            "scrsys": "remoteok",
            "note": response.doc('div.description>div:nth-child(3)').text(),
            "issuedtime": calctime(getTime) ,
            "inserttime": now('%Y-%m-%d %H:%M:%S'),

        }
    def on_result(self, result):
        print result
        if not result or not result['title']:
            return
        sql = SQL()
        sql.replace('jobs',**result)


#-----------------------------------------------------------------------------------------------
#stackoverflow
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://careers.stackoverflow.com/jobs?sort=p', callback=self.index_page, age=1*24*60*60)


    @config(age=1 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://careers.stackoverflow.com/jobs/(\d*)/', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('#content>div.-row>div.main.-col9>div.listResults.-jobs.list.jobs>div.jobsfooter>div>a.prev-next.job-link.test-pagination-next').items():
            self.crawl(each.attr.href,callback=self.index_page)
        # for each in response.doc('a[href^="http"]').items():
        #     if re.match('http://careers.stackoverflow.com/jobs?', each.attr.href):
        #         self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('title').text(),
            "position": response.doc('#hed>h1>a').text(),
            "company": response.doc('#hed>a').text(),
            "fulltime":response.doc('#hed>span').text(),
            "address": response.doc('#hed>span').text(),
            "url": response.url,
            "scrsys": "stackoverflow",
            "note": response.doc('#jobdetailpage>div.main.-col9>div').text(),
            "issuedtime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
            "inserttime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,

        }
    def on_result(self, result):
        print result
        if not result or not result['title']:
            return
        sql = SQL()
        sql.replace('jobs',**result)
        
#----------------------------------------------------------
#stackoverflow
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
import re
import time 

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://careers.stackoverflow.com/jobs?sort=p', callback=self.index_page, age=1*24*60*60)


    @config(age=1 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://careers.stackoverflow.com/jobs/(\d*)/', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('#content>div.-row>div.main.-col9>div.listResults.-jobs.list.jobs>div.jobsfooter>div>a.prev-next.job-link.test-pagination-next').items():
            self.crawl(each.attr.href,callback=self.index_page)
        # for each in response.doc('a[href^="http"]').items():
        #     if re.match('http://careers.stackoverflow.com/jobs?', each.attr.href):
        #         self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('title').text(),
            "position": response.doc('#hed>h1>a').text(),
            "company": response.doc('#hed>a').text(),
            "fulltime":response.doc('#hed>span').text(),
            "address": response.doc('#hed>span').text(),
            "url": response.url,
            "scrsys": "stackoverflow",
            "note": response.doc('#jobdetailpage>div.main.-col9>div').text(),
            "issuedtime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,
            "inserttime": time.strftime('%Y-%m-%d %X',time.localtime(time.time())) ,

        }
    def on_result(self, result):
        print result
        if not result or not result['title']:
            return
        sql = SQL()
        sql.replace('jobs',**result)