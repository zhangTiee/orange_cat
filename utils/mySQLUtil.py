# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:33
# @Author  : zjl

import pymysql
import logging

logger = logging.getLogger(__name__)


class MySQLUtil:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "1234"
        self.database = "information_live"
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.exception("sql执行异常>>>")

    def SqlSe(self, sql, param=None):
        try:
            self.cursor.execute(sql, param)
            logger.info(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logger.exception("sql执行异常>>>")
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommit(self, sql, param=None):
        try:
            if param is None:
                self.cursor.execute(sql)
                logger.info(sql)
            else:
                self.cursor.execute(sql, param)
                logger.info(sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.exception("sql执行异常>>>")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommitMany(self, sql, param):
        try:
            self.cursor.executemany(sql, param)
            logger.info(sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.exception("sql执行异常>>>")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def GetColumns(self, tablename):
        sql = f"describe {tablename}"
        try:
            self.cursor.execute(sql)
            logger.info(sql)
            columns = [result[0] for result in self.cursor.fetchall()]
            return columns
        except Exception as e:
            logger.exception("sql执行异常>>>")
        finally:
            self.cursor.close()
            self.conn.close()
