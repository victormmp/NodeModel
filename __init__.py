import logging
from src.LinkService import *
from src.NetNode import *
from src.GlobalParameters import  *


# CONFIGURES LOG OPTIONS

# create logger with 'spam_application'
logger = logging.getLogger('NetModel')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs/logs.log')
fh.setLevel(logging.DEBUG)
# create console handler with a debug log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
