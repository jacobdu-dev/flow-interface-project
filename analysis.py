import flowkit as fk
from bokeh.plotting import show

class Analysis():
	plot_his = 1
	plot_density = 2
	def __init__(self, filepath, datafiles):
		"""
		Init is responsible for importing all sample data files and creating 
		dictionaries and variables for tracking analysis progress. Init will also create
		a flowkit session. 

		Input Paramters:
		- filepaths - string of the directory containing sample data relative to current directory
		- datafiles - list of strings of filenames of fsc files to be imported
		"""
		self.session = fk.session()#creating flowkit session
		self.filepath = filepath #no use at the moment, just in case accessing of files is needed later on
		self.samples = {i:datafiles[i] for i in range(len(datafiles))} #id:filename
		#importing all samples to session
		for i in datafiles: self.session.add_samples(fk.Sample(filepath + i))
		#creating dictionary for gating heiarchy 
		self.gatingheiarchy = {}

	def addgate(self):
		pass

	def generatefigure(self, type):
		pass

	def getgateheiarchy(self):
		pass
