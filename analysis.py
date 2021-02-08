import flowkit as fk
from bokeh.plotting import show
import pickle

class Analysis():
	"""
	The analysis class serves as the primary interface between the FlowKit library and the raw data/user inputs. 
	Nearly all functions performed should go through an Analysis object.  
	"""
	plot_his = 1
	plot_density = 2
	def __init__(self):
		"""
		init is responsible for creation of all variables/attributes within the object. 

		returns True if function is completed without error. 
		"""

		self.session = None
		self.filepath = ""
		self.samples = {} #id:filename
		self.gatingheiarchy = {}#dictionary for gating heiarchy
		return True

	def importdata(self, filepath, datafiles):
		"""
		importdata is responsible for importing all sample data files and initial population of object variables/attributes.

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
		return True


	def addgate(self, parent_x , parent_y, verticies,  gatename, parentgate = ''):
		"""
		The method addgate is responsible for creating gates, and saving them to the gatingheiarchy dictionary. The only supported gate is polygon.

		Input Parameteres:
		- parent_x
		- parent_y
		- verticies
		- gatename - string representing the name of the date (eg. CD3 High). There should be no duplicate gate names. 
		- parentgate - Defaulted to ''. String representing the parent gates of the new gate. 

		returns True if gate is added successfully and False if an error is encountered such as a duplicate gate.

		Implemented gating heiarchy handling. Actually creating the gate on FlowKit is still yet to be implemented.
		"""
		if parentgate == '': 
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
				#create flowkit gate
				return True
			else: 
				return False

	def generatefigure(self, type, log = True):
		pass

	def getgateheiarchy(self):
		"""
		The getgateheiarchy class serves as a method for users of the program to view their gating heiarchy. 
		The method is implemented to map out the structure of nested dictionaries (self.gateheiarchy) and return
		a tree in the format of a string. There are no input perameters and returns the string that will be printed. 
		Please note dictionaries are not ordered and therefore the values on the tree are not ordered either. Only the
		heiarchy will be intact. 
		"""
		stack = []
		returnstring = ""
		for i, j in {"root": self.gateheiarchy}.items():
			stack.append((0, i, j))
			while len(stack) != 0:
				lvl, key, val = stack.pop()
				returnstring += "|" + lvl * "---" + str(key) + "\n" if lvl != 0 else lvl * "---" + str(key) + "\n"
				for k, l in val.items():
					stack.append((lvl + 1, k, l))
		return returnstring


	def exportsession(self, filename = "untitled"):
		"""
		Saves all object data into a binary file with name defined by user (or defaulted to "untitled") with a .session file extension.

		Input Parameteres:
		- filename - String of file name in which all data will be saved to (excludes .session extension). Defaults to "untitled".

		returns True if saving process is sucessful or returns False if filename is empty
		"""
		if len(filename) == 0: #filename cannot be empty
			return False
		with open(filename + ".session", 'wb'):
			pickle.dump([self.session, self.filepath, self.samples, self.gateheiarchy], f)
		return True

	def restoresession(self, filename = "untitled"):
		"""
		Loads object data from a previous saved session file. 

		Input Parameteres:
		- filename - String of file name in which all data will be loaded from (excludes .session extension). Defaults to "untitled".

		returns True if loading process is sucessful or returns False if filename is empty
		"""
		if len(filename) == 0: #filename cannot be empty
			return False
		with open(filename + ".session", 'wb'):
			self.session, self.filepath, self.samples, self.gateheiarchy = pickle.load(f)
		return True