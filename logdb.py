#!/usr/bin/python3
# log.db utility
#
# dump
# print file_list
# comment file "comment"
# delete key
#
# Copyright 2021 Robert Bond
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import os
import sys
import argparse
import sqlite3

import log_hs

def dump_cmd(log_db):
    log_db.dump_db()

def print_cmd(log_db, files):
    for f in files:
        l = log_db.get_log(f)
        for entry in l:
            print(entry[1], entry[2], entry[3])
        c = log_db.get_comments(f)
        for entry in c:
            print(entry[0], entry[1], entry[2])

def comment_cmd(log_db, f, s):
    log_db.add_comment(f, s)
    log_db.commit()

def delete_cmd(log_db, key):
    log_db.del_comment(key)
    log_db.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="Commands", dest="command")
    dump_parser = subparsers.add_parser("dump", aliases=["du"],
                      help = "Dump entire database")

    print_parser = subparsers.add_parser("print", aliases=["p", "pr"],
                  help = "Print data associated with a list of files")
    print_parser.add_argument("file", nargs="+", help = "File names")

    comment_parser = subparsers.add_parser("comment", aliases=["c", "co"],
                   help = "Add a comment")
    comment_parser.add_argument("file", help = "file_name")
    comment_parser.add_argument("string", help = "string to add to the db")

    delete_parser = subparsers.add_parser("delete", aliases=["de", "del"],
                  help = "Delete a comment from the database")
    delete_parser.add_argument("key", type=int, help = "Key")

    log_db = log_hs.db('log.db')

    args = parser.parse_args(sys.argv[1:])
    if args.command in {"dump", "du"}:
        dump_cmd(log_db)
    elif args.command in {"print", "p", "pr"}:
        print_cmd(log_db, args.file)
    elif args.command in {"comment", "c", "co"}:
        comment_cmd(log_db, args.file, args.string)
    elif args.command in {"delete", "de", "del"}:
        delete_cmd(log_db, args.key)
    else:
        print("Unknown command:", args.command)

    exit(0)
