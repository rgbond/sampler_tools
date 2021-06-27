#!/usr/bin/python3
# Read logged data from log.db

import os
import sys
import argparse
import sqlite3

import log_hs


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Get log data')
    ap.add_argument('--verbose', '-v', action='count', default=0,
                    help='print debug info')
    ap.add_argument('--log', '-l', action='store_true',
                    help='print logged data')
    ap.add_argument('--comments', '-c', action='store_true',
                    help='print comments')
    ap.add_argument('--dump', '-d', action='store_true', 
                    help='dump entire database')
    ap.add_argument('files', nargs='*', help='list of files to process')
    args = ap.parse_args()

    log_db = log_hs.db('log.db')

    if args.dump:
        log_db.dump_db()
        exit(0)

    if len(args.files) == 0:
        print("Must list at least one filename")
        exit(1)
    if not args.log and not args.comments:
        print("Must specify --log or --comments")
        exit(1)

    for f in args.files:
        if args.log:
            l = log_db.get_log(f)
            if len(l) == 0:
                print("Nothing logged for", f)
            else:
                for entry in l:
                    print(entry[0], entry[1], entry[2], entry[3])
        if args.comments:
            c = log_db.get_comments(f)
            if len(c) == 0:
                print("No comments for", f)
            else:
                for entry in c:
                    print(entry[0], entry[1], entry[2])

