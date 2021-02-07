import flowkit as fk
from bokeh.plotting import show

class Analysis():
	def __init__(self, filepath, datafiles):
		"""
		Init is responsible for importing all sample data files and creating 
		dictionaries and variables for tracking analysis progress

		Input Paramters:
		- filepaths - string of the directory containing sample data relative to current directory
		- datafiles - list of filenames of fsc files to be imported
		"""

		filepath = filepath
		self.samples = {}
		self.gatingheiarchy = {}