# Halsampler tools

These command line tools provide wrappers for the Linuxcnc halcmd and halsampler
utilities.  They allow the user to set hal pins, log hal pin values, log comments,
then start halsampler, saving the run in an automatically generated output file.
All log data is captured in a local sqlite database called log.db. The halsampler
data can be plotted via plot_hs.py. The logged hal data and comments can be dumped
via logdb.py

To use log_hs.py, first edit log_hs.py and change these python arrays as needed:

* to_set: hal pins or nets to set before the run starts.
* to_log: hal pins or nets to log before the run starts.
* comments: any comments you want logged in the database for this run.
* sampler_nets: The nets that the sampler hal utility is saving for halsampler.

Then run the command. It will:
* create the database if it doesn't exist,
* create a log file for halsampler to use, 
* log the info in the database, 
* log the sampler_nets information as the first line of the log file,
* start halsampler. 

At this point the user would normally run a gcode file that
triggers sampler. When the run ends, hit return and halsampler will be
terminated.

plot_hs.py takes "-f" command line arguments to specify the fields to plot.
Valid field names are logged as the first line of the log file. The
field name can be extended with a ":n" to scale that field. For example, to see
"x-vel-cmd" in inches per minute rather than inches per second, use
"-f x-vel-cmd:60". Plot_hs.py takes a list of one or more log file names. All
data is displayed on one screen to help show what changed between runs.

logdb.py has a command style interface that allows the user to dump the database,
query it, add or remove previously logged comments.

The utilities require python3 versions of matplotlib, sqlite3 and numpy.
