import subprocess,sys
from ..utils.logger.logger import setup_logger
p =setup_logger()
def enable_port4444():
    PORT=4444
    
    try:
        (res1)=subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(PORT), '-j', 'ACCEPT'], check=True)
        (res2)=subprocess.run(['sudo', 'iptables-save'], check=True, stdout=subprocess.DEVNULL)
        p.info(f"setting up the port")
        p.info(f"res1 {res1}  res2 : {res2} ")
        return True
    except subprocess.CalledProcessError as e:
        p.info(f"exception occured {str(e)}")
        sys.exit(1)
        

