import logging
import sys

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)
