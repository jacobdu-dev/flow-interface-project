import numpy as np
class Sample():
	def __init__(self, channels, labels, raw, comp, xform):
		self.channels = channels
		self.label_indicies = {i: j - 1 for i, j in labels.items()}
		self.raw_data = raw
		self.comp_data = comp
		self.xform_data = xform
	def get_raw_data(self, x_label= None, y_label = None, row_indicies = None):
		if x_label is None and y_label is None: 
			return self.raw_data if row_indicies is None else self.raw_data[[[rows] for rows in row_indicies], :]
		if y_label is None: 
			return self.raw_data[:, [int(self.label_indicies[x_label])]] if row_indicies is None else self.raw_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label])]]
		return self.raw_data[:, [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]] if row_indicies is None else self.raw_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]]
	def get_comp_data(self, x_label= None, y_label = None, row_indicies = None):
		if x_label is None and y_label is None: 
			return self.comp_data if row_indicies is None else self.comp_data[[[rows] for rows in row_indicies], :]
		if y_label is None: 
			return self.comp_data[:, [int(self.label_indicies[x_label])]] if row_indicies is None else self.comp_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label])]]
		return self.comp_data[:, [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]] if row_indicies is None else self.comp_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]]
	def get_xform_data(self, x_label= None, y_label = None, row_indicies = None):
		if x_label is None and y_label is None: 
			return self.xform_data if row_indicies is None else self.xform_data[[[rows] for rows in row_indicies], :]
		if y_label is None: 
			return self.xform_data[:, [int(self.label_indicies[x_label])]] if row_indicies is None else self.xform_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label])]]
		return self.xform_data[:, [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]] if row_indicies is None else self.xform_data[[[rows] for rows in row_indicies], [int(self.label_indicies[x_label]), int(self.label_indicies[y_label])]]
