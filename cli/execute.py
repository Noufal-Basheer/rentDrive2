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
    subparsers.add_parser("push",help="Push the files to server")
    subparsers.add_parser("restore", help="Check status")
    config_parser = subparsers.add_parser("config", help="Config your account \t config -u <username> -p <password>")
    config_parser.add_argument("u",  help="username")
    config_parser.add_argument("p",  help="password")
    commit_parser = subparsers.add_parser("test",help="Push the files to server")



    

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
        process.push()
    elif args.command=="restore":
        process.restore()
    elif args.command=="config":
        process.config(args.u,args.p)
    elif args.command=="test":
        process.test()

        
        
     
