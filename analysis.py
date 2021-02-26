import flowkit as fk
from bokeh.plotting import show
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

class Analysis():
	"""
	The analysis class serves as the primary interface between the FlowKit library and the raw data/user inputs. 
	Nearly all functions performed should go through an Analysis object.  
	"""
	def __init__(self):
		"""
		init is responsible for creation of all variables/attributes within the object. 

		returns True if function is completed without error. 
		"""
		self.session = None
		self.filepath = ""
		self.channels = None
		self.samples = {} #id:filename
		self.gatingheiarchy = {}#dictionary for gating heiarchy
		self.gateindicies = {}

	def importdata(self, filepath, datafiles, compensation):
		"""
		importdata is responsible for importing all sample data files and initial population of object variables/attributes.

		Input Paramters:
		- filepaths - string of the directory containing sample data relative to current directory
		- datafiles - list of strings of filenames of fsc files to be imported
		- compensation - string of filename (in same filepath) of the compensation matrix in csv format

		returns True if function is completed without error. 
		"""
		self.session = fk.Session()#creating flowkit session
		self.filepath = filepath #no use at the moment, just in case accessing of files is needed later on
		self.samples = datafiles
		#importing all samples to session
		self.channels = fk.Sample(filepath + datafiles[0]).channels
		print(self.channels)
		#get compensation matrix
		#comp = np.genfromtxt(filepath + compensation, delimiter = ',')
		#comp = np.nan_to_num(comp)
		for i in datafiles: 
			#apply compensation
			sample = fk.Sample(filepath + i)
			if sample.channels != self.channels:
				print("Channels do not match, are these samples from the same experiment?")
			#sample.apply_compensation(comp, comp_id="spill_comp")
			self.session.add_samples(sample)
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
				#parent gate must exist, if a == False, it doesnt
				a[parentgate][gatename] = {}
				#create flowkit gate
				gate_indicies = [] # implement a function that gets sample indicies from gate
				self.gateindicies[gatename] = gate_indicies
				return True
			else: 
				return False

	def generatefigure(self, sample, x, y = "his", parent = "", logicle = True, left = 0, right = 270000):
		"""if percentile == True:
			raw = np.sort(self.session.get_sample(sample).get_raw_events())
			events_to_remove = raw.size * 0.01 #removes 0.01% of events to remove noise
			for i in range(int(events_to_remove / 2)): del raw[-1]
			for i in range(int(events_to_remove / 2)): del raw[0]"""
		#ensures channels exist
		label_indicies = {self.channels[i]['PnN']:i for i in self.channels.keys()}
		print(label_indicies)
		if x not in label_indicies.keys(): return False
		if y != "his" and y not in label_indicies.keys(): return False
		#get dataframe of events
		if logicle == True:
			sample_instance = self.session.get_sample(sample)
			sample_instance.apply_transform(fk.transforms.LogicleTransform('logicle_xform', param_t=300000, param_w=5, param_m=5, param_a=0))
			sampledata = sample_instance.get_transformed_events()
		else:
			sample_instance = self.session.get_sample(sample)
			sampledata = self.session.get_sample(sample).get_raw_events()
		x_index = label_indicies[x]
		y_index = None
		if y != "his": y_index = sample_instance.get_channel_index(y)
		#get gate events
		if parent == "":
			plotdata = sampledata[: , [int(x_index)]].flatten() if y_index is None else sampledata[: , [int(x_index), int(y_index)]]
			del sampledata
		else:
			gate_indicies = [1, 2]
			plotdata = sampledata[[[rows] for rows in gate_indicies], [int(x_index)].flatten() if y_index is None else [int(x_index), int(y_index)]]
			del sampledata
		#generate matplotlib plot
		f, ax = plt.subplots()
		if y == "his":
			ax.hist(plotdata, bins = int((right - left) / 10))
			ax.set_title("Histogram - " + x)
			ax.set_xlabel(x)
			ax.set_ylabel("Counts")
			ax.set_xlim(left=left, right=right)
			return ax
		else:
			print("starting", plotdata[:, 0].size, plotdata[:, 1].size)
			xy = np.vstack([plotdata[:, 0], plotdata[:, 1]])
			print("half")
			density = gaussian_kde(xy)(xy)
			print("generating plot")
			ax.scatter(plotdata[:, 0], plotdata[:, 1], c=density, edgecolor='')
			print("done")
			ax.set_title(x + "vs." + y)
			ax.set_xlabel(x)
			ax.set_ylabel(y)
			return ax



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