# -*- coding: utf-8 -*-
import chardet
import scrapy
import re
import sys
from mysql import MySQL
from datetime import datetime
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider,Spider
from scrapy.linkextractors import LinkExtractor
from QQspider.items import QqspiderItem
reload(sys)
sys.setdefaultencoding('utf-8')


def find_domain(url):
    try:
        domain = re.findall(r'http://[\w.]*.com', url)[0]
        return domain
    except IndexError:
        return ""


def next_urls(url):
    try:
        value = re.findall(r'http://[\w.]*.qq.com', url)[0]
        return value
    except IndexError:
        return False


def judge_url(url):
    if re.match(r'http://', url):
        return 1
    return 0


def insert_data(data):
    db = MySQL()
    try:
        db.insert('urls_crawled', data)
    except:
        return 0
    db.commit()


def get_data(url, title):
    data = dict()
    data['title'] = title
    data["domain"] = find_domain(url)
    data["url"] = url
    data["time"] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return data


class QQSpider(Spider):
    name = "pre"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://www.qq.com/"
    ]
    news = set()

    def parse(self, response):
        if response.status:
            selector = Selector(response)
            count=0
            for a in selector.xpath('//a'):
                try:
                    url_link = a.xpath("@href").extract()
                    url_title = a.xpath("text()").extract()
                    url = url_link[0]
                    if url_title is None or url_title == []:
                        url_title.append("")
                    if judge_url(url):
                        url_title = url_title[0]
                        insert_data(get_data(url, url_title))
                    count+=1
                    if count==15:
                        break
                except IndexError as e:
                    print(e)

