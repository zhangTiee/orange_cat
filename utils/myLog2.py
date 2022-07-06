# -*- coding: UTF-8 -*-
import logging
import os
import time


class MyLog:
    def __init__(self):
        """
        日志配置
        """
        logger = logging.getLogger("logger")
        logger.setLevel(logging.DEBUG)
        # 1.文件输出
        # 没有设置输出级别，将用logger的输出级别(并且输出级别在设置的时候级别不能比Logger的低!!!)，设置了就使用自己的输出级别
        if os.path.exists(os.getcwd() + "\\log") is False:
            os.mkdir(os.getcwd() + "\\log")
        filename = f"log\log_{time.strftime('%Y%m%d')}.log"
        # 2.标准输出
        if len(logger.handlers) == 0:
            streamHandler = logging.StreamHandler()
            fileHandler = logging.FileHandler(filename=filename, mode='a')
            # 控制台及日志打印格式器
            logformat = logging.Formatter(fmt="%(asctime)s - %(levelname)-6s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            # 给处理器设置格式
            streamHandler.setFormatter(logformat)
            fileHandler.setFormatter(logformat)
            # 设置生效
            logger.addHandler(streamHandler)
            # logger.addHandler(fileHandler)
        self.logger = logger

    def debugLog(self, message):
        """
        :param message: 信息描述
        :return:
        """
        logger = self.logger
        logger.debug(message)

    def infoLog(self, message):
        """
        :param message: 信息描述
        :return:
        """
        logger = self.logger
        logger.info(message)

    def warningLog(self, message):
        """
        :param message: 信息描述
        :return:
        """
        logger = self.logger
        logger.warning(message)

    def errorLog(self, message):
        """

        :param message: 信息描述
        :return:
        """
        logger = self.logger
        logger.error(message)

    def criticalLog(self, message):
        """
        :param message: 信息描述
        :return:
        """
        logger = self.logger
        logger.critical(message)
