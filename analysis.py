import flowkit as fk
from bokeh.plotting import show

class Analysis():
	plot_his = 1
	plot_density = 2
	def __init__(self, filepath, datafiles):
		"""
		init is responsible for importing all sample data files and creating 
		dictionaries and variables for tracking analysis progress. Init will also create
		a flowkit session. 

		Input Paramters:
		- filepaths - string of the directory containing sample data relative to current directory
		- datafiles - list of strings of filenames of fsc files to be imported

		returns True if function is completed without error. 
		"""

		self.session = fk.session()#creating flowkit session
		self.filepath = filepath #no use at the moment, just in case accessing of files is needed later on
		self.samples = {i:datafiles[i] for i in range(len(datafiles))} #id:filename
		#importing all samples to session
		for i in datafiles: self.session.add_samples(fk.Sample(filepath + i))
		#creating dictionary for gating heiarchy and gates
		self.gates = {}
		self.gatingheiarchy = {}
		return True

	def addgate(self, gatename, parentgate = None):
		"""
		The method addgate is responsible for creating gates, and saving them to the gatingheiarchy dictionary.

		Input Parameteres:
		- gatename - string representing the name of the date (eg. CD3 High). There should be no duplicate gate names. 
		- parentgate - Defaulted to None. String representing the parent gates of the new gate. 

		returns True if gate is added successfully and False if an error is encountered such as a duplicate gate.

		Implemented gating heiarchy handling. Actually creating the gate on FlowKit is still yet to be implemented.
		"""
		if parentgate == None: 
			#we need to first parse through 
			self.gatingheiarchy[gatename] = {}
		else:
			#a stack implementation of a recursive function that would find the parent gate in dictionaries
			stack = []
			stack.append(self.gatingheiarchy)
			a = False
			while len(stack) != 0:
				process = stack.pop()
				#Base case: the nested/entire dictionary is empty
				if len(list(process.keys())) != 0:
					if parentgate in list(process.keys()):
						#we found the nested dictionary containing the parent gate
						a = process
						break
					else:
						for i in list(process.keys()):
							stack.append(process[i])
			if a != False:
				a[parentgate][gatename] = {}
				return True
			else: 
				return False

	def generatefigure(self, type, log = True):
		pass

	def getgateheiarchy(self):
		pass
