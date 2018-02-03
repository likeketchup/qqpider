# -*- coding:utf-8 -*-
import scrapy
import re
from mysql import MySQL
from datetime import datetime


def find_domain(url):
    try:
        domain = re.findall(r'http://[\w.]*.qq.com/', url)[0]
        return domain
    except IndexError:
        return "Not qq.com"


def judge_url(url):
    if re.match(r'http://\w*', url):
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
    data["grabTime"] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return data


class QQSpider(scrapy.Spider):
    name = "qq"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://www.qq.com/"
    ]

    def parse(self, response):
        if response.status:
            for sel in response.xpath('//a[@href]'):
                url_link = sel.xpath("@href")[0].extract()
                url_title = sel.xpath("text()").extract()
                url = url_link.encode("utf-8")
                if url_title is None or url_title == []:
                    url_title.append("No Title")
                if judge_url(url_link):
                    insert_data(get_data(url, url_title[0]))
