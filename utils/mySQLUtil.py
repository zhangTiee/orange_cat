# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:33
# @Author  : zjl

import pymysql
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
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
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=self.cursorclass,
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.exception("-----------------数据库连接异常-----------------")

    def SqlSe(self, sql, param=None):
        try:
            logger.info(f"执行sql----------------->  {sql}")
            self.cursor.execute(sql, param)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            logger.error("-----------------sql执行异常-----------------")
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommit(self, sql, param=None):
        try:
            if param is None:
                self.cursor.execute(sql)
                logger.warning(sql)
            else:
                logger.info(f"执行sql----------------->  {sql % param}")
                self.cursor.execute(sql, param)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error("-----------------sql执行异常-----------------")
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
            logger.info(f"执行sql----------------->  {insert_sql}")
            self.cursor.execute(insert_sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlUpdate(self, table, params, param):
        try:
            set_sql = "set "
            where_sql = f"where {param} = {params[param]}"
            del params[param]
            for k, v in params.items():
                set_sql += f"{k}={v},"
            update_sql = f"""
            update {table} {set_sql[:-1]} {where_sql}"""
            logger.info(f"执行sql----------------->  {update_sql}")
            self.cursor.execute(update_sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def SqlCommitMany(self, sql, param):
        try:
            logger.info(f"执行sql----------------->  {sql % param}")
            self.cursor.executemany(sql, param)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error("-----------------sql执行异常-----------------")
            return False
        finally:
            self.cursor.close()
            self.conn.close()

    def GetColumns(self, tablename):
        sql = f"describe {tablename}"
        try:
            logger.info(f"执行sql----------------->  {sql}")
            self.cursor.execute(sql)
            columns = [result[0] for result in self.cursor.fetchall()]
            return columns
        except Exception as e:
            logger.error("-----------------sql执行异常-----------------")
        finally:
            self.cursor.close()
            self.conn.close()
