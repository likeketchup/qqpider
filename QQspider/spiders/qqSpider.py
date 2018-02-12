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
    name = "qq"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://www.qq.com/"
    ]
    news = set()
    rules = (Rule(LinkExtractor(allow=r'http://news.qq.com/a/2018.+'), callback='parse_item',follow=True),)

    def parse_item(self, response):
        if response.status:
            try:
                selector = Selector(response)
                item = QqspiderItem()
                info = selector.xpath(r'//div[@class="a_Info"]')
                try:
                    item['catalog'] = info.xpath(r'//span[@class="a_catalog"]/text()').extract()[0]
                except IndexError:
                    item['catalog'] = info.xpath(r'//span[@class="a_catalog"]/a/text()').extract()[0]
                try:
                    item['source'] = info.xpath(r'//span[@class="a_source"]/text()').extract()[0]
                except IndexError:
                    item['source'] = info.xpath(r'//span[@class="a_source"]/a/text()').extract()[0]
                item['source'] = info.xpath(r'//span[@class="a_source"]/a/text()').extract()[0]
                item['urls'] = response.url
                item['title'] = selector.xpath(r'//h1/text()').extract()[0]
                item['time'] = info.xpath(r'//span[@class="a_time"]/text()').extract()[0]
                item['first_paragraph'] = selector.xpath(r'//*[@id="Cnt-Main-Article-QQ"]//p[@class="text"]/text()').extract()[1]
                item['image_urls'] = selector.xpath(r'//p[@align="center"]/img/@src').extract()[0]
                return item
            except IndexError:
                print(response.url)


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
