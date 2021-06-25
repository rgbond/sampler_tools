#!/usr/bin/python3
# Gets stuff out of the logger database


import os
import sys
import argparse
import sqlite3

import logger


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Add a comment to log.db')
    ap.add_argument('--verbose', '-v', action='count', default=0,
                    help='print debug info')
    ap.add_argument('file', help='file to comment on')
    ap.add_argument('comment', help='comment to add')
    args = ap.parse_args()

    log_db = logger.db('log.db')

    if len(args.comment) == 0:
        print("Must list at least one comment on the command line")
        exit(1)

    log_db.add_comment(args.file, args.comment)
    log_db.commit()
