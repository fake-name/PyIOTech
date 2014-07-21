
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



def run():

	
	import GUI		# Have to import after queVars config variables are set
	
	#queVars.cnf.serThread = threading.Thread(target = serIO.mainLoop, name = "serThread")

	#queVars.cnf.serThread.start()

	mainWin = GUI.MyApp(0)

	#print instructions
	mainWin.MainLoop()


if __name__ == "__main__":

	profrun()
	'''
	import cProfile
	import pstats

	cProfile.run('run()', 'fooprof')
	
	print "Exiting"
	p = pstats.Stats('fooprof')
	p.strip_dirs().sort_stats(-1).print_stats()
	p.sort_stats('name')
	p.print_stats()
	p.sort_stats('cumulative').print_stats(10)
	p.sort_stats('time').print_stats(10)
	p.dump_stats("runStat.txt")
	'''
	