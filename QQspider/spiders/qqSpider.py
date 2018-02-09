# -*- coding: utf-8 -*-
import scrapy
import re
import sys
from mysql import MySQL
from datetime import datetime
from scrapy.selector import Selector
from scrapy.spider import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from QQspider.items import QqspiderItem


def find_domain(url):
    try:
        domain = re.findall(r'http://[\w.]*.com', url)[0]
        return domain
    except IndexError:
        return ""


def next_urls(url):
    try:
        value = re.findall(r'http://[\w.]*.qq.com',url)[0]
        return value
    except IndexError:
        return False


def judge_url(url):
    if re.match(r'http://', url):
        return 1
    return 0


def insert_data(data):
    db = MySQL()
    sql = "select id from urls_crawled where url='"+data['url']+"';"
    try:
        db.insert('urls_crawled', data)
    except:
        return 0
    db.commit()


def get_data(url, title):
    data = {}
    data['title'] = title
    data["domain"] = find_domain(url)
    data["url"] = url
    data["time"] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return data


class QQSpider(CrawlSpider):
    name = "three"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://www.qq.com/"
    ]
    news = set()
    rules = (Rule(LinkExtractor(allow=r'http://news.qq.com/a/2018.+'), callback='parse_item',follow=True),)

    def parse_item(self, response):
        if response.status:
            selector = Selector(response)
            item = QqspiderItem()
            item['urls'] = response.url
            item['title'] = selector.xpath('/html/body/div[2]/div[3]/div[1]/d'
                                           'iv/div[1]/div[1]/div[1]/h1/text()').extract()[0]
            item['catalog'] = selector.xpath('/html/body/div[2]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]'
                                             '/span[1]/a/text()').extract()[0]
            item['source'] = selector.xpath('/html/body/div[2]/div[3]/div[1]/div/div[1]/div[1]/div['
                                           '1]/div/div[1]/span[2]/a').extract()[0]
            item['time'] = selector.xpath('/html/body/div[2]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/spa'
                                          'n[4]').extract()[0]
            item['first_graph'] = /html/body/div[2]/div[4]/div[1]/div/div[1]/div[1]/div[2]/div/p[2]
            item['img'] =''//*[@id="Cnt-Main-Article-QQ"]/p[2]
            return item

#            for i in urls:
#                yield (scrapy.Request(url,callback=parse_domain))

"""
selector = Selector(response)
            for a in selector.xpath('//a'):
                try:
                    url_link = a.xpath("@href").extract()
                    url_title = a.xpath("text()").extract()
                    url = url_link[0]
                    if url_title is None or url_title == []:
                        url_title.append("")
                    if judge_url(url):
                        insert_data(get_data(url, url_title[0].encode('utf8', 'ingore')))
                except IndexError as e:
                    print(e)
"""
