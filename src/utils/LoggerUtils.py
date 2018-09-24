import logging
import os

def configure_log(level=logging.DEBUG, name=None, use_file=False, use_console=False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if use_file:
        filename = os.path.join('logs', name + ".log")
        file_handler = logging.FileHandler(filename, 'w', 'utf-8')

        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    if use_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('[%(asctime)s - %(name)s: %(funcName)s] >> %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger