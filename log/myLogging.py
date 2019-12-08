import logging

myLogger = logging.getLogger(__name__)
myLogger.setLevel(logging.INFO)

file_handler = logging.FileHandler('log/logfile.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
myLogger.addHandler(file_handler)