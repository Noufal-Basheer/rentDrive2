from cli_utils.logger.logger import setup_logger
p =setup_logger()

def add(path):
    p.info("adding...")
    for paths in path:
        p.info(f"{paths}")


def status():
    p.info("status")
    

def pull():
    p.info("pull")