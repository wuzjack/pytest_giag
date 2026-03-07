import logging
import os.path
import time

from configs import globalparam


log_path = globalparam.log_path
class Log:
    def __init__(self):
        self.logname = os.path.join(log_path,'{0}.log'.format(time.strftime('%Y-%m-%d-%H-%M-%S')))

    def __printconsole(self,level,message):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.logname,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)

        logger.removeHandler(ch)
        logger.removeHandler(fh)

    def info(self,message):
        self.__printconsole('info',message)
    def debug(self,message):
        self.__printconsole('debug',message)
    def warning(self,message):
        self.__printconsole('warning',message)
    def error(self,message):
        self.__printconsole('error',message)

log = Log()