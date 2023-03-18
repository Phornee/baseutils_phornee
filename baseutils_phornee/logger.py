""" Logger management """
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import time
from enum import Enum


class LoggerMode(Enum):
    """ Enum class for logger modes """
    NONE = 0
    FILE = 1
    STD = 2
    BOTH = 3


class UTCFormatter(logging.Formatter):
    """ Class for formatter """
    converter = time.gmtime


class Logger():
    """ Logger class with builtin handler configuration"""
    def __init__(self, package_name: str,
                 log_file_name: str,
                 mode: LoggerMode = LoggerMode.FILE,
                 level=logging.INFO,
                 utc: bool = False):
        self.log_file_name = log_file_name

        self.homevar = os.path.join(str(Path.home()), 'var', 'log', package_name)
        self.package_name = package_name

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.setup_logger(mode, level, utc)

    def get_log_path(self) -> str:
        """ Returns the log path based on the homevar folder and the log file name specified"""
        return os.path.join(self.homevar, f"{self.log_file_name}.log")

    def setup_logger(self, mode: LoggerMode, level, utc: bool):
        """ Setup the selected mode, that means which builtin handlers will be added to the logger """
        self.logger = logging.getLogger(f'{self.package_name}_{self.log_file_name}_log')

        if not os.path.exists(self.homevar):
            os.mkdir(self.homevar)

        if utc:
            formatter = UTCFormatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')
        else:
            formatter = logging.Formatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')

        # Create rotating file handler
        if mode in [LoggerMode.FILE, mode.BOTH]:
            file_handler = RotatingFileHandler(self.get_log_path(), maxBytes=10000, backupCount=10)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Create stdout stream handler
        if mode in [LoggerMode.STD, mode.BOTH]:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        # Create empty log file if it doesn´t previously exist
        if not os.path.exists(self.get_log_path()):
            with open(self.get_log_path(), 'w', encoding='UTF-8'):
                pass

        # Same level in both handlers
        self.logger.setLevel(level)

    def get_log(self) -> str:
        """ Get log file content """
        with open(self.get_log_path(), 'r', encoding='UTF-8') as file:
            return file.read()

    def info(self, message: str):
        """ Outputs a info log """
        self.logger.info(message)

    def debug(self, message: str):
        """ Outputs a debug log """
        self.logger.debug(message)

    def warning(self, message: str):
        """ Outputs a warning log """
        self.logger.warning(message)

    def error(self, message: str):
        """ Outputs an error log """
        self.logger.error(message)
