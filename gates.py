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
		self.verticies = verticies #verticies will be type tuple if y is 'his' else list of tuples representing points
		self.type = y if y is 'his' else 'polygon'
		self.parent = parent
		self.transformation = transformation
		self.lines = []
		if type(verticies) is not tuple:
			#self.lines will be list of (m, b) 
			for i in range(len(verticies)):
				j = i + 1 if i != (len(verticies) - 1) else 0 #if y1, x1 is last element of list, y2 and x2 are the first element of list
				m = (verticies[j][1] - verticies[i][1]) / (verticies[j][0] - verticies[i][0]) #m = (y2 - y1)/(x2 - x1)
				b = verticies[i][1] - m * verticies[i][0] #b = y - m * x
				self.lines.append((m, b))

	def get_indicies(self, sample_data):
		if self.transformation == "logicle":
			data_xform = sample_data
			gate_indicies = []
			point_list = list(map(tuple, a))
			for i in range(len(point_list)):
				x, y = point_list[i]
				if is_ingate((x, y)):
					gate_indicies.append(i)
			return gate_indicies
		else:
			return False
	def is_ingate(self, point):
		"""
		This method is responsible for determining whether or not a specific point lies within the given boundary conditions.
		Input Paramters:
		- point - A tuple representing the coordinates of a point. This point should be post-processed (xform/comp applied to match gate conditions)

		Returns True if point lies within the boundaries else False

		Approach: For each line, if point is under line with m 
		"""
		

		for m, b in self.lines:
			if m > 0:

