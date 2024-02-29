from extras import registry
from utils import process
from utils.logger.logger import setup_logger
import argparse
from utils.startupservices import portlistenstartupservice
p = setup_logger()

if __name__ == "__main__":
   #  parser = argparse.ArgumentParser()
   #  parser.add_argument("supass", help="superuser password")
   #  args = parser.parse_args()
   #  registry.set_registry("superuser", args.supass)
    p.info("starting process")
    portlistenstartupservice.receiver()
    process.process()
