import logging
import inspect
from datetime import datetime
import os

class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
 
    def init(self, *args, **kwds):
        pass

# Inherits Singleton
class LoggerManager(Singleton):
    error_level = logging.ERROR
    debug_level = logging.DEBUG

    def __init__(self, folder_path: str):
        self.logger = logging.getLogger()
        self.level = LoggerManager.debug_level
        self.format = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s(): %(lineno)d - %(message)s"
        self.folder_path = folder_path

        self.file_name = ""
        self.log_file = ""

        file_handler = None
        console_handler = None

        self._create_dir()
        try:
            # Handlers
            file_handler = logging.FileHandler(self.log_file, "a")
            console_handler = logging.StreamHandler()
        except:
            raise IOError("Couldn't create/open file \"" + \
                          self.log_file + "\". Check permissions.")
        
        # Set logger level
        self.logger.setLevel(self.level)
        # format
        formatter = logging.Formatter(self.format)
        # Set format for handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
 
    def debug(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)
 
    def error(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.error(msg, exc_info=True)
 
    def info(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.info(msg)
 
    def warning(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)

    def _get_date_now(self):
        '''
        Get date now with format YYYYMMDD
        '''
        now = datetime.now()
        date_time = now.strftime("%Y%m%d")
        return date_time

    def _create_dir(self):
        '''
        Create the path of file if needed
        '''
        self.file_name = self._get_date_now()
        self.log_file = f"{os.path.join(self.folder_path, self.file_name)}.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

class Logger(object):
    """
    Logger object.
    """
    def __init__(self, loggername: str, folder_path: str):
        self.logger_manager = LoggerManager(folder_path) # LoggerManager instance
        self.loggername = loggername # logger name

 
    def debug(self, msg):
        self.logger_manager.debug(self.loggername, msg)
 
    def error(self, msg):
        self.logger_manager.error(self.loggername, msg)
 
    def info(self, msg):
        self.logger_manager.info(self.loggername, msg)
 
    def warning(self, msg):
        self.logger_manager.warning(self.loggername, msg)



