#!/usr/bin/env python3

import argparse
import os
import zipfile
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def add_command(directory_path):
    zip_filename = "archive.zip"
    hash_value = hashlib.sha256()
    with open(directory_path, 'rb') as file:
        for chunk in iter(lambda: file.read(8192), b''):
            hash_value.update(chunk)
    hash_value = hash_value.hexdigest()

    cipher = AES.new(b'Sixteen byte key', AES.MODE_CBC)
    encrypted_hash = b64encode(cipher.encrypt(pad(hash_value.encode('utf-8'), AES.block_size))).decode('utf-8')

    print("Zipping the directory...")
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, directory_path)
                zip_file.write(file_path, arcname)

    print(f"Hash value: {hash_value}")
    print(f"Encrypted Hash: {encrypted_hash}")

def status_command():
    print("Showing user registry...")
    # Add code to display user registry

def main():
    parser = argparse.ArgumentParser(description="rentdrive - A simple CLI for file manipulation")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add a directory")
    add_parser.add_argument("directory_path", help="Path to the directory")

    subparsers.add_parser("status", help="Show user registry")

    args = parser.parse_args()

    if args.command == "add":
        add_command(args.directory_path)
    elif args.command == "status":
        status_command()
    else:
        print("Error: Invalid command. Available commands: add, status")

if __name__ == "__main__":
    main()
