import logging

log_level = logging.DEBUG

logging.root.setLevel(log_level)

stream = logging.StreamHandler()
stream.setLevel(log_level)

logger = logging.getLogger('gudid_parser')
logger.addHandler(stream)
