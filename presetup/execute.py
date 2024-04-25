import subprocess,sys
from utils import process
from logger.logger import p

if __name__ == "__main__":
   p.info(f"--------------- starting execution of presetup ---------------------")
   if subprocess.run(['id', '-u'], stdout=subprocess.PIPE).stdout.strip() != b'0':
      p.info("This script must be run with root privilages")
      sys.exit(1)
   p.info("starting process")
   process.process()
