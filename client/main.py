import rentdriveProcess
from client_utils.logger.logger import setup_logger
p = setup_logger()

if __name__ == "__main__":
    p.info('This is an info message from main')
    rentdriveProcess.process()
    