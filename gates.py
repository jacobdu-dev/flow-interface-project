from multiprocessing.dummy import Process

class Gates():
    """
    This class is responsible for saving gate parameters and generating indicies of subset events
    given its parameters. 
    """
    def __init__(self, name, verticies, samples, x, y = 'his', parent = None, logicle=True):
        """
        Saving gate parameters. 
        """
        self.name = name
        self.x = x
        self.y = y
        self.verticies = verticies#verticies will be [a, b] if y is 'his' else list of tuples representing points
        self.type = y if y == 'his' else 'polygon'
        self.parent = parent
        self.transformation = logicle
        self.indicies = {}
        self.processes = {}
        self.calculate(samples)

    def calculate(self, samples):
        for samplename, sample in samples.items():
            p = Process(target=self.cal_gate_indicies, args=(samplename, sample, ))
            self.processes[samplename] = p
            self.processes[samplename].start()

    def get_gate_indicies(self, sample):
        return self.indicies[sample.name]

    def cal_gate_indicies(self, *args):
        samplename = args[0]
        sample = args[1]
        gate_indicies = list(self.parent.get_gate_indicies(sample)) if self.parent != None else list(sample.all_ind)
        if self.transformation:
            if self.parent != None:
                sample_data = sample.get_xform_data(self.x, row_indicies = gate_indicies) if self.type == 'his' else sample.get_xform_data(self.x, self.y, gate_indicies)
            else:
                sample_data = sample.get_xform_data(self.x) if self.type == 'his' else sample.get_xform_data(self.x, self.y)
        else:
            if self.parent != None:
                sample_data = sample.get_comp_data(self.x, row_indicies = gate_indicies) if self.type == 'his' else sample.get_comp_data(self.x, self.y, gate_indicies)
            else:
                sample_data = sample.get_comp_data(self.x) if self.type == 'his' else sample.get_comp_data(self.x, self.y)
        c = 0
        if self.type != 'his':
            point_list = list(map(tuple, sample_data))
            for i in range(len(point_list)):
                x, y = point_list[i]
                if not self.is_ingate((x, y)):
                    del gate_indicies[i - c]
                    c += 1
        else:
            sample_data = sample_data.tolist()
            for i in range(len(sample_data)):
                if sample_data[i][0] <= self.verticies[0] or sample_data[i][0] >= self.verticies[1]:
                    del gate_indicies[i - c]
                    c += 1
        self.indicies[samplename] = gate_indicies
        return True

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
