#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import sys
import chardet
OperationalError = pymysql.OperationalError

class MySQL:
    host = 'localhost'
    port = 3306
    user = 'root'
    passwd = '!TM_ketchup_99'
    db = 'qq_mainpage'

    def __init__(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            self.cur = self.conn.cursor()
            self.cur.execute('set names \'utf8\';')
        except pymysql.Error, e:
            print(e)

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return 1
        except pymysql.Error, e:
            print(e)
            return 0

    def insert(self, table_name, data):
        cates = data.keys()
        prefix = "".join(['INSERT INTO ', table_name])
        fields = ",".join([i for i in cates])
        values = ",".join("%s" for i in range(len(cates)))
        sql = "".join([prefix, "(", fields, ") VALUES(", values, ");"])
        params = (data[cate] for cate in cates)
        try:
            self.cur.execute(sql, tuple(params))
        except pymysql.Error, e:
            print sql, e

    def update(self, table_name, data):
        _sql = ""
        return self.cur.execute(_sql)

    def delete(self,tbname,condition):
        _sql=""
        return self.cur.execute(_sql)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()
