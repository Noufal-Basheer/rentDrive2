from cli_utils.logger.logger import setup_logger
import argparse , sys
from cli_utils import process
p= setup_logger()

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RentDrive Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    add_parser = subparsers.add_parser("add", help="Add files")
    add_parser.add_argument("paths", nargs="+", help="Paths to add")
    subparsers.add_parser("status", help="Check status")
    subparsers.add_parser("pull", help="Pull files")

    args = parser.parse_args()

    if args.command == "add":
        if not args.path:
            p.error("please pass arguments path")
            sys.exit(1)
        p.info("rentdrive add %s"%args.path)
        process.add(args.paths)
    elif args.command == "pull":
        process.pull()
        
     
