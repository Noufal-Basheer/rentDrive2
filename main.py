from utils import process, registry
from utils.logger.logger import setup_logger
import argparse

p = setup_logger()

if __name__ == "__main__":
   #  parser = argparse.ArgumentParser()
   #  parser.add_argument("supass", help="superuser password")
   #  args = parser.parse_args()
   #  registry.set_registry("superuser", args.supass)
    p.info("starting process")
    process.process()
