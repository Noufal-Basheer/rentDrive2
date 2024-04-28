from cli_utils.logger.logger import p
import argparse , sys
from cli_utils import process


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RentDrive Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    add_parser = subparsers.add_parser("add", help="Add files")
    add_parser.add_argument("path", nargs="+", help="files/dirs to add \t rentdrive add <path>")
    subparsers.add_parser("status", help="Check status")
    subparsers.add_parser("commit", help="commit the files and make it ready to push ")
    subparsers.add_parser("pull", help="Pull files")
    commit_parser = subparsers.add_parser("push",help="Push the files to server")
    commit_parser.add_argument("token",help="Auth token")
    subparsers.add_parser("restore", help="Check status")
    config_parser = subparsers.add_parser("config", help="Config your account \t config -u <username> -p <password>")
    config_parser.add_argument("u",help="username")
    config_parser.add_argument("p", help="password")

    

    args = parser.parse_args()

    if args.command == "add":
        if not args.path:
            p.error("please pass arguments path")
            sys.exit(1)
        p.info("rentdrive add %s"%args.path)
        process.add(args.path)
    elif args.command == "pull":
        process.pull()
    elif args.command == "commit":
        process.commit()
    elif args.command == "push":
        if not args.token:
            p.error("Invalid token")
            sys.exit(1)
        process.push(args.token)
    elif args.command=="restore":
        process.restore()
    elif args.command=="config":
        process.config(args.u,args.p)

        
        
     
