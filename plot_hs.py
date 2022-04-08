#!/usr/bin/python3
#
# plots halsampler output
#
# Assumes data files have lables in row 1:
# x-pos-cmd x-vel-cmd x-pid-out x-pos-fb x-vel-fb
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
#
# Usage plot_hs [-x col0] [-f col1] ... [-f coln] file1 file2
#
# The program plots all of the fields in the data file if called with
# no "-f" arguments.
#
# The -f colx and -x colx arguments pick off columns to plot from the file
# example:
#
# plot_hs -f x-pos-cmd -f x-pos-fb run.out
#
# A "-x" argument indicates a label to be used as the x axis instead of
# the default line number. For example, the following command will plot the
# the commanded position against the position feedback:
#
# plot_hs -x x-pos-cmd -f x-pos-fb run.out
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

import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

def process_file(x_name, f, fields, scale):
    n = 0
    lines = f.readlines()
    if len(lines) < 2:
        print("Less than 2 lines in file.")
        print("File example:")
        print("x-pos-cmd x-vel-cmd x-pos.out")
        print("0.000000 0.000000 -0.012800")
        exit(1)
    labels = lines[0].strip().split()
    if x_name is None:
        x_index = None
        xi = 0.0
    else:
        if x_name in labels:
            x_index = labels.index(x_name)
            x_scale = scale[x_name]
        else:
            print(x_name, "not in file header")
            exit(1)
    if len(fields) == 0:
        fields = labels
        scale = {}
        for f in fields:
            scale[f] = 1.0
    indicies = []
    lscale = []
    for field in fields:
        if not (field in labels):
            print(field, "not in file header")
            exit(1)
    for i, l in enumerate(labels):
        if l in fields:
            indicies.append(i)
            lscale.append(scale[l])
        else:
            lscale.append(1.0)
    plot_labels = [labels[i] for i in indicies]
    plot_data = []
    x_values = []
    for line in lines[1:]:
        lf = line.strip().split()
        if lf[0].isalpha():
            print("skipping", lf[0])
            continue
        plot_data.append([float(lf[i]) * lscale[i] for i in indicies])
        if x_index is None:
            x_values.append(xi)
            xi += 1.0
        else:
            x_values.append(float(lf[x_index]) * x_scale)
    return plot_labels, x_values, np.array(plot_data).transpose()
        
def handle_scale_factor(f, scale):
    if ':' in f:
        fs = f.split(':')
        scale[fs[0]] = float(fs[1])
        return fs[0]
    else:
        scale[f] = 1.0
        return f

class plotter(object):
    def __init__(self, nplots):
        if nplots == 1:
            fig, axs = plt.subplots()
            self.fig = [fig]
            self.axs = [axs]
        else:
            self.fig, self.axs = plt.subplots(nplots)
        self.pn = 0

    def plot_subplot(self, labels, x_values, data, file_name):
        for i, l in enumerate(labels):
            self.axs[self.pn].plot(x_values, data[i], label=l)
        self.axs[self.pn].grid(b=True, which='major', axis='x')
        self.axs[self.pn].set_title(file_name)
        self.axs[self.pn].legend()
        self.pn += 1

    def show(self):
        plt.show()

if __name__ == "__main__": 
    ap = argparse.ArgumentParser(description='Get log data')
    ap.add_argument('--verbose', '-v', action='count', default=0,
                    help='Print debug info')
    ap.add_argument('--field', '-f', action='append',
                    help='Field name, optional :scale')
    ap.add_argument('--x', '-x', help='Select X axis for plot')
    ap.add_argument('files', nargs='+', help='Files to process')
    args = ap.parse_args()

    scale = {}
    if args.x is None:
        x_name = None
    else:
        x_name = handle_scale_factor(args.x, scale)
    fields = []
    if not args.field is None:
        for f in args.field:
            f = handle_scale_factor(f, scale)
            fields.append(f)
    if args.verbose > 0:
        print("fields:", fields)
        print("scale:", scale)

    plot = plotter(len(args.files))
    for fname in args.files:
        try:
            f = open(fname, 'r')
            labels, x_values, data = process_file(x_name, f, fields, scale)
            plot.plot_subplot(labels, x_values, data, fname)
            f.close()
        except IOError as e:
            print("Can't open file", fname)
            exit(1)
    plot.show()
