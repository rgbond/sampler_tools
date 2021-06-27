#!/usr/bin/python3
#
# Deletes a log or comment record
#

import argparse
import log_hs

if __name__ == "__main__": 
    ap = argparse.ArgumentParser(description='Delete db record')
    ap.add_argument('--verbose', '-v', action='count', default=0,
                    help='Print debug info')
    ap.add_argument('--log', '-l', action='store',
                    help='log key value to delete')
    ap.add_argument('--comment', '-c', action='store',
                    help='comment key value to delete')
    args = ap.parse_args()

    log_db = log_hs.db("log.db")

    if args.log:
        log_db.del_log(args.log)
        log_db.commit()
    if args.comment:
        log_db.del_comment(args.comment)
        log_db.commit()
