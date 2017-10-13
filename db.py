# -*- coding: utf-8 -*-
import MySQLdb


class DB:
    def __init__(self):
        self.coon = MySQLdb.connect(host='127.0.0.1', user="root", passwd="123456", db="weibo", charset="utf8")
        self.coon.autocommit(True)

    def ex(self, weobo_level, weibo_name, synopsis, attention, fans, wei_bo, sex):
        sql = "INSERT INTO weibo_user(weobo_level, weibo_name, synopsis, attention, fans," \
                     " wei_bo_num, sex) VALUES ({}, '{}', '{}', {}, {}, {}, '{}')".format(weobo_level, weibo_name,
                                                                                          synopsis, attention, fans,
                                                                                          wei_bo, sex)
        db = self.coon.cursor()
        try:
            db.execute(sql)
        except:
            db.rollback()
        self.close_spider()

    def close_spider(self):
            self.coon.close()


