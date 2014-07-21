
import threading

import queVars

import sys

#import matplotlib
#matplotlib.use("WxAgg")

try:
	from profilestats import profile


	@profile
	def profrun():
		run()
except:
	print "Cannot profile interpreter"

	def profrun():
		run()

instructions = \
"Command line Swithes:\n\
Format:	PYTHON MAIN.PY [SWITCHES]\n\
\n\
Runtime Only Switches (Cannot be changed when program is running):\n\
  'Thermist'/'Thermistor'  - Puts the program into thermistor mode, for \n\
		interfacing with the thermistor board\n\
  'noRedir'	- Prints text output to the command line rather then\n\
		the text output window in the GUI.\n\
  'graphdata'/'graphdat'	- graph thermistor calues in realtime. *Probably \n\
		does not work with IIC devices\n\
	\
\n\
Convenience Switches :\n\
(Affect functions which can be changed through the GUI as well):\n\
\n\
  'NoViz'	- Disable the data visualization (visuzlization \n\
		can be re-enabled through the GUI after opening)\n\
  'AutoOpen'	- Opens the first serial available FTDI device \n\
		imediately at start\n\
  'LogDat'	- Starts logging imediately on run. Implies 'AutoOpen'\n\
\n\
  All commands are *not* case sensitive, and do no have to be preceded with a '-'.\n\
  \
  \
  \
"


def run():
	'''
	cleaned = ""
	if len(sys.argv) > 1:
		import re
		cleaned = re.sub("\W", "", re.sub("\W", "", ("%s" % sys.argv[1:]).lower()))


	if cleaned.find("noredir") > -1:
		print "Redirecting Test Output to command line"
		queVars.cnf.noRedir = True

	if cleaned.find("noscale") > -1:
		print "Not scaling data for display"
		queVars.cnf.scaled = False

	if cleaned.find("help") > -1:
		print instructions
		sys.exit()

	if cleaned.find("logDat") > -1:
		print "Logging from Start"

		queVars.cnf.openOnStart = True
		queVars.cnf.logEn = True

	if cleaned.find("noviz") > -1:
		print "No Vizualization"
		queVars.cnf.visualization = False

	if cleaned.find("autoopen") > -1:
		print "Opening first available serial port"
		queVars.cnf.openOnStart = True

	if cleaned.find("thermist") > -1:
		print "Reading from Thermistors"
		queVars.cnf.thermistors = True

		queVars.cnf.regenArayVars((32,64))

		import thermistSerIO as serIO


	else:
		print "Starting viz and processing thread"
		import IICserIO as serIO
		import dataProcessing

		queVars.cnf.datProcThread = threading.Thread(target = dataProcessing.mainLoop, name = "datProcThread")

		queVars.cnf.datProcThread.start()

		print "Starting Process"

	'''

	import GUI		# Have to import after queVars config variables are set

	#queVars.cnf.serThread = threading.Thread(target = serIO.mainLoop, name = "serThread")

	#queVars.cnf.serThread.start()

	mainWin = GUI.MyApp(0)

	'''
	if cleaned.find("graphdat") > -1:
		print "Realtime Data Display"
		import anim
		anim.setupWindow(mainWin, queVars.cnf.tmpRawAr)

	mainWin = MainFrame.MyApp(0)
	'''

	#print instructions
	mainWin.MainLoop()


if __name__ == "__main__":


	import cProfile
	import pstats

	cProfile.run('run()', 'fooprof')
	
	print "Exiting"
	p = pstats.Stats('fooprof')
	#p.strip_dirs().sort_stats(-1).print_stats()
	#p.sort_stats('name')
	#p.print_stats()
	p.sort_stats('cumulative').print_stats(20)
	p.sort_stats('time').print_stats(20)
	
	