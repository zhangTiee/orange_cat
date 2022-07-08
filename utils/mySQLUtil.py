# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:33
# @Author  : zjl

import pymysql
import logging

logger = logging.getLogger(__name__)
from config.source import mysqldata

host = mysqldata().get("host")
user = mysqldata().get("user")
password = mysqldata().get("password")
database = mysqldata().get("database")


class MySQLUtil:
    def __init__(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursorclass = pymysql.cursors.DictCursor
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, cursorclass=self.cursorclass)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.exception("-----------------数据库连接异常-----------------")

    def SqlSe(self, sql, param=None):
        try:
            self.cursor.execute(sql, param)
            logger.warning(f"执行sql----------------->  {sql}")
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logger.exception("-----------------sql执行异常-----------------")
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommit(self, sql, param=None):
        try:
            if param is None:
                self.cursor.execute(sql)
                logger.warning(sql)
            else:
                self.cursor.execute(sql, param)
                logger.warning(f"执行sql----------------->  {sql % param}")
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.exception("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlInsert(self, table, params):
        try:
            key = ",".join(list(params.keys()))
            val = ",".join(list(params.values()))
            insert_sql = f"""
            insert into {table}({key}) values({val})"""
            logger.warning(f"执行sql----------------->  {insert_sql}")
            self.cursor.execute(insert_sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.exception("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommitMany(self, sql, param):
        try:
            self.cursor.executemany(sql, param)
            logger.warning(f"执行sql----------------->  {sql % param}")
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.exception("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def GetColumns(self, tablename):
        sql = f"describe {tablename}"
        try:
            self.cursor.execute(sql)
            logger.warning(f"执行sql----------------->  {sql}")
            columns = [result[0] for result in self.cursor.fetchall()]
            return columns
        except Exception as e:
            logger.exception("-----------------sql执行异常-----------------")
        finally:
            self.cursor.close()
            self.conn.close()
