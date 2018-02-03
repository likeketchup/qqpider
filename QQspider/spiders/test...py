import pymysql
from datetime import datetime
import re
from mysql import MySQL


def find_domain(url):
    try:
        domain = re.findall(r'http://[\w.]*.qq.com/', url)[0]
        return domain
    except IndexError:
        return "Not qq.com"


def get_data(url, title):
    data = {}
    data['title'] = title
    data["domain"] = find_domain(url)
    data["url"] = url
    data["grabTime"] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return data


def insert_data(data):
    db = MySQL()
    sql = "select id from urls_crawled where url='"+data['url']+"';"
    try:
        db.insert('urls_crawled',data)
    except pymysql.Error:
        return 0
    db.commit()


insert_data(get_data("http://www.gy.qq.com/leia.htm","test"))