import numpy as np

class Gates():
	"""
	This class is responsible for saving gate parameters and generating indicies of subset events
	given its parameters. 
	"""
	def __init__(self, name, verticies, x, y = 'his', parent = "", logicle=True):
		"""
		Saving gate parameters. 
		"""
		self.name = name
		self.x = x
		self.y = y
		self.verticies = verticies
		self.type = y if y is 'his' else 'polygon'
		self.parent = parent
		self.transformation = transformation

	def get_indicies(self, sample_data, xform_data = None):
		if self.transformation == "logicle":
			return False
		else:
			return False