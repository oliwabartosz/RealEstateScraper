"""
Here is a config file for logger.
You can set options such as:
- logging parameters.
"""
from typing import Union
import logging


class Logger:
    """
    Sets the logger.

    Attributes:
    :filename: set a filename in which logs will be saved.
    :area: set an area, which is the name of specific logger.

    :return: function logging.getLogger
    """

    @staticmethod
    def setup(name: str, file_name: str, log_filemode: Union[str, str] = 'w'):
        log_file = file_name
        log_format = "%(asctime)s - %(name)-12s: %(levelname)-8s %(message)s"
        log_level = logging.INFO

        logger = logging.getLogger(name)

        # File output line
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file, mode=log_filemode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console output line
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        log_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
        logger.propagate = 0

        return logger


# LOGGERS
logger_scrapper = Logger.setup(name='scrapper', file_name='./data/logs/scrapper.log')
logger_input = Logger.setup(name='input', file_name='./data/logs/input.log')
logger_warnings = Logger.setup(name='warnings', file_name='./data/logs/warnings.log')
