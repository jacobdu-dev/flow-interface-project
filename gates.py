import numpy as np

class Gates():
    """
    This class is responsible for saving gate parameters and generating indicies of subset events
    given its parameters. 
    """
    def __init__(self, name, verticies, x, y = 'his', parent = None, logicle=True):
        """
        Saving gate parameters. 
        """
        self.name = name
        self.x = x
        self.y = y
        self.verticies = verticies #verticies will be [a, b] if y is 'his' else list of tuples representing points
        self.type = y if y == 'his' else 'polygon'
        self.parent = parent
        self.transformation = logicle

    def get_indicies(self, sample):
        if self.transformation:
            if self.parent is not None:
                sample_data = sample.get_xform_data(self.x, row_indicies = self.parent.get_indicies(sample)) if self.type == 'his' else sample.get_xform_data(self.x, self.y, self.parent.get_indicies(sample))
            else:
                sample_data = sample.get_xform_data(self.x) if self.type == 'his' else sample.get_xform_data(self.x, self.y)
        else:
            if self.parent is not None:
                sample_data = sample.get_raw_data(self.x, row_indicies = self.parent.get_indicies(sample)) if self.type == 'his' else sample.get_raw_data(self.x, self.y, self.parent.get_indicies(sample))
            else:
                sample_data = sample.get_raw_data(self.x) if self.type == 'his' else sample.get_raw_data(self.x, self.y)
        if self.type != 'his':
            gate_indicies = []
            print(sample_data)
            point_list = list(map(tuple, sample_data))
            print(len(point_list))
            for i in range(len(point_list)):
                x, y = point_list[i]
                if self.is_ingate((x, y)):
                    gate_indicies.append(i)
            return gate_indicies
        else:
            sample_data = sample_data.tolist()
            gate_indicies = []
            for i in range(len(sample_data)):
                if sample_data[i] >= self.verticies[0] and sample_data[i] <= self.verticies[1]:
                    gate_indicies.append(i)
            return gate_indicies

    def is_ingate(self, point):
        """
        This method is responsible for determining whether or not a specific point lies within the given boundary conditions.
        Input Paramters:
        - point - A tuple representing the coordinates of a point. This point should be post-processed (xform/comp applied to match gate conditions)

        Returns True if point lies within the boundaries else False
        """
        # check if point is a vertex
        x, y = point
        if (x,y) in self.verticies:
            return True
        # check if point is on a boundary
        else:
            for i in range(len(self.verticies)):
                p1 = None
                p2 = None
                if i==0:
                    p1 = self.verticies[0]
                    p2 = self.verticies[1]
                else:
                    p1 = self.verticies[i-1]
                    p2 = self.verticies[i]
                if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
                    return True
        n = len(self.verticies)
        p1x,p1y = self.verticies[0]
        for i in range(n+1):
            p2x,p2y = self.verticies[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            return True
        return False
