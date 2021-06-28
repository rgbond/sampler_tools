#!/usr/bin/python3
#
# plots halsampler output
#
# Usage errplt file col1 col3 ... coln
#     assumes the columns of data have a label in row 1
#
# x-pos-cmd x-vel-cmd x-pid-out x-pos-fb x-vel-fb
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
# 0.000000 0.000000 -0.012800 0.005709 -0.011239 
#
# The colx arguments pick off columns to plot from the file
# example:
#
# echo 'x-pos-cmd x-vel-cmd x-pid-out x-pos-fb x-vel-fb' > run.out
# halsampler -c 0 >> run.out
#
# errplt run.out x-pos-cmd x-pos-fb
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

def process_file(f, fields, scale):
    n = 0
    lines = f.readlines()
    if len(lines) < 2:
        print("Less than 2 lines in file.")
        print("File example:")
        print("x-pos-cmd x-vel-cmd x-pos.out")
        print("0.000000 0.000000 -0.012800")
        exit(1)
    labels = lines[0].strip().split()
    indicies = []
    lscale = []
    for field in fields:
        if field not in labels:
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
    for line in lines[1:]:
        lf = line.strip().split()
        if lf[0].isalpha():
            print("skipping", lf[0])
            continue
        plot_data.append([float(lf[i]) * lscale[i] for i in indicies])
    return plot_labels, np.array(plot_data).transpose()
        
class plotter(object):
    def __init__(self, nplots):
        if nplots == 1:
            fig, axs = plt.subplots()
            self.fig = [fig]
            self.axs = [axs]
        else:
            self.fig, self.axs = plt.subplots(nplots)
        self.pn = 0

    def plot_subplot(self, labels, data, file_name):
        x_values = np.arange(len(data[0]))
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
    ap.add_argument('files', nargs='+', help='Files to process')
    args = ap.parse_args()

    scale = {}
    fields = []
    for f in args.field:
        if ':' in f:
            fs = f.split(':')
            fields.append(fs[0])
            scale[fs[0]] = float(fs[1]) 
        else:
            fields.append(f)
            scale[f] = 1.0

    if args.verbose > 0:
        print("fields:", fields)
        print("scale:", scale)

    plot = plotter(len(args.files))
    for fname in args.files:
        try:
            f = open(fname, 'r')
            labels, data = process_file(f, fields, scale)
            plot.plot_subplot(labels, data, fname)
            f.close()
        except IOError as e:
            print("Can't open file", fname)
            exit(1)
    plot.show()
