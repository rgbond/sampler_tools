#!/usr/bin/python3
#
# Sets up a simple db to hold tuning parameters and log file names
# Maintains parameters for tuning runs
# Runs halcmds
# Starts and stops sampler runs
#

import os
import sys
import subprocess
import argparse
import glob
import sqlite3

# Change these as needed for each run:
to_set = {
    "pid.x.Pgain": 40.0,
    "pid.x.Igain": 0.0,
    "pid.x.Dgain": 0.0,
}

to_log = [
    "pid.x.Pgain",
    "pid.x.Dgain",
    "pid.x.Igain",
    "pid.x.FF0",
    "pid.x.FF1",
    "pid.x.FF2",
    "pid.x.maxerror",
    "ini.0.max_acceleration",
    "ini.0.max_velocity",
    "ini.traj_max_acceleration",
    "ini.traj_max_velocity",
    "hm2_7i95.0.stepgen.00.maxaccel",
    "hm2_7i95.0.stepgen.00.maxvel",
    "hm2_7i95.0.stepgen.00.control-type",
    "hm2_7i95.0.stepgen.00.position-scale",
]

comments = [
    "run_x_300_F15_nobl.ngc",
]

sampler_nets = [
    "x-pos-cmd",
    "x-vel-cmd",
    "x-pos.out",
    "x-pos-fb",
    "x-vel-fb",
]

tables_sql = [
    '''
        CREATE TABLE log(
            k INTEGER primary KEY,
            file_name VARCHAR,
            param_name VARCHAR,
            param_value REAL
        )
    ''',
    '''
        CREATE TABLE comments(
            k INTEGER primary KEY,
            file_name VARCHAR,
            comment VARCHAR
        )
    '''
]

drops_sql = [
    'DROP TABLE IF EXISTS log',
    'DROP TABLE IF EXISTS comments',
]

add_log_sql = 'INSERT INTO log(file_name, param_name, param_value) VALUES(?,?,?)'
add_comment_sql = 'INSERT INTO comments(file_name, comment) VALUES(?,?)'
dump_log_sql = 'SELECT * FROM log';
dump_comments_sql = 'SELECT * FROM comments';
get_log_sql = 'SELECT * FROM log where file_name = ?';
get_comments_sql = 'SELECT * FROM comments where file_name = ?';

class db(object):
    def __init__(self, db_path, setup=False, verbose=False):
        if not os.path.isfile(db_path):
            setup = True
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()
        self.verbose = verbose
        if setup:
            self.mk_db(db_path)

    def commit(self):
        self.db.commit()

    def mk_db(self, db_path):
        for drop_sql in drops_sql:
            self.c.execute(drop_sql)
        for tbl_sql in tables_sql:
            self.c.execute(tbl_sql)
        self.db.commit()

    def add_log(self, fn, pn, pv):
        self.c.execute(add_log_sql, (fn, pn, pv))

    def add_comment(self, fn, comment):
        self.c.execute(add_comment_sql, (fn, comment))

    def dump_db(self):
        self.c.execute(dump_log_sql)
        for r in self.c.fetchall():
            print(r[1], r[2], r[3])
        self.c.execute(dump_comments_sql)
        for r in self.c.fetchall():
            print(r[1], r[2])

    def get_log(self, f):
        self.c.execute(get_log_sql, (f,))
        return self.c.fetchall()

    def get_comments(self, f):
        self.c.execute(get_comments_sql, (f,))
        return self.c.fetchall()

def set_pin(v, f):
    subprocess.run(["halcmd", "setp", v, str(f)])

def get_pin(v):
    result = subprocess.run(["halcmd", "getp", v],
                            capture_output=True, text=True)
    return result.stdout

class sampler():
    def start_sampler(self, f):
        self.p = subprocess.Popen(["halsampler"], stdout=f)

    def abort_sampler(self):
        self.p.terminate()
        self.p.wait()

def db_regress():
    my_db = db('test_db', True)
    my_db.add_log("001.out", "x.pid.Pgain", 10.0)
    my_db.add_log("001.out", "x.pid.Igain", 0.1)
    my_db.add_log("002.out", "x.pid.Pgain", 20.0)
    my_db.add_log("002.out", "x.pid.Igain", 0.2)
    my_db.add_comment("002.out", "this is a comment")
    my_db.commit()

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Log tuning runs')
    ap.add_argument('--verbose', '-v', action='count', default=0)
    ap.add_argument('--test', '-t', action='count', default=0)
    args = ap.parse_args()

    if args.test > 0:
        db_regress()
        exit(0)

    # Generate the next log file name
    file_list = glob.glob('[0-9]*.out')
    if len(file_list) == 0:
        log_file_name = "001.out"
    else:
        file_list.sort()
        last = int(file_list[-1].split('.')[0]) 
        log_file_name = "{:03d}.out".format(last + 1)
    if args.verbose > 0:
        print("log_file_name:", log_file_name)

    # Do hal cmds and log results in log.db
    log_db = db('log.db')

    for v in to_set:
        set_pin(v, to_set[v])

    for v in to_log:
        f = get_pin(v)
        log_db.add_log(log_file_name, v, f)

    for c in comments:
        log_db.add_comment(log_file_name, c)

    log_db.commit()

    # Populate the log file header
    log_file = open(log_file_name, "w")
    hdr = " ".join(sampler_nets)
    log_file.write(hdr + '\n')
    log_file.flush()

    # Cygwin hack until I spend time on ACLs
    os.chmod(log_file_name, 0o644)

    s = sampler()
    input("hit return to start sampler")
    s.start_sampler(log_file)

    input("hit return to abort sampler")
    s.abort_sampler()
