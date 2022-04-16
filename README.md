# Halsampler tools

These command line tools provide wrappers for the Linuxcnc halcmd and halsampler
utilities.  They allow the user to set hal pins, log hal pin values, log comments,
then start halsampler, saving the run in an automatically generated output file.
All log data is captured in a local sqlite database called log.db. The halsampler
data can be plotted via plot_hs.py. The logged hal data and comments can be dumped
via logdb.py

The commands are:
* log_hs.py: log data and run halsampler
* plot_hs.py: plot the data returned from halsampler
* logdb.py: examine and manipulate the data in the database

To use log_hs.py, first edit log_hs.py and change these python arrays as needed:

* to_set: hal pins or nets to set before the run starts.
* to_log: hal pins or nets to log before the run starts.
* comments: any comments you want logged in the database for this run.
* sampler_nets: The nets that the sampler hal utility is saving for halsampler.

Then run the log_hs.py command. It will:
* create the database if it doesn't exist,
* create a log file for halsampler to use, 
* log the info in the database, 
* log the sampler_nets information as the first line of the log file,
* start halsampler. 

At this point the user would normally run a gcode file that
triggers sampler. When the run ends, hit return and halsampler will be
terminated.

plot_hs.py takes optional "-f field" command line arguments to specify the
fields to plot.  Valid field names appear in the first line of the log file.
This command generated screenshot.png:
* plot_hs.py -f x-vel-cmd -f x-vel-fb 001.out 002.out

Field name modifiers:
* ':n' Multiply field values by n
* '^d' Delay field by d ticks

For example, use "-f x-vel-cmd:60" to see velocity in inches per minute
rather than inches per second.

plot_hs.py can have a "-x field" argument to specify the field value to use
as the x axis in the plot.

plot_hs.py will plot all of the fields in the data files if called with no
"-f" arguments.

logdb.py has a command style interface that allows the user to dump the database,
query it, add or remove previously logged comments. Sample commands:
* logdb.py dump
* logdb.py print 001.out 002.out
* logdb.py comment 001.out "a little better"
* logdb.py delete 22


To install, just save the three python files in a directory somewhere. I use
linuxcnc/nc_files/tuning so that the gcode files are "next door".

The utilities require python3 versions of matplotlib, sqlite3 and numpy.
