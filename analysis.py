import flowkit as fk
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
from gates import Gates
from sample import Sample
from timeit import timeit


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
        self.filepath = ""
        #self.channels = None
        self.samples = {}  # name:{type:instance of Sample class}
        self.gating_heiarchy = {}  # dictionary for gating heiarchy
        self.gates = {} #{gatename:instance of the gates class}

    def importdata(self, filepath, datafiles, compensation):
        """
        importdata is responsible for importing all sample data files and initial population of object variables/attributes.

        Input Paramters:
        - filepaths - string of the directory containing sample data relative to current directory
        - datafiles - list of strings of filenames of fsc files to be imported
        - compensation - string of filename (in same filepath) of the compensation matrix in csv format

        returns True if function is completed without error. 
        """
        self.filepath = filepath  # no use at the moment, just in case accessing of files is needed later on
        # importing all samples to session
        # get compensation matrix
        comp = np.genfromtxt(filepath + compensation, delimiter=',')
        comp = np.nan_to_num(comp)  # elminate NaN values in compensation matrix
        for i in datafiles:
            # apply compensation
            sample = fk.Sample(filepath + i)
            sample.apply_compensation(comp, comp_id="spill_comp")
            sample.apply_transform(
                fk.transforms.LogicleTransform('logicle', param_t=262144, param_w=0.5, param_m=5, param_a=0))
            sample_label_indicies = {sample.channels[i]['PnN']: int(i) for i in sample.channels.keys()}
            self.samples[i] = Sample(i, sample.channels, sample_label_indicies, sample.get_raw_events(), sample.get_comp_events(), sample.get_transformed_events())
            del sample
        return True

    def addgate(self, verticies, gatename, parent_x, parent_y = 'his', parentgate='', logicle=True):
        """
        The method addgate is responsible for creating gates, and saving them to the gatingheiarchy dictionary. The only supported gate is polygon.

        Input Parameteres:
        - parent_x
        - parent_y
        - verticies
        - gatename - string representing the name of the date (eg. CD3 High). There should be no duplicate gate names.
        - parentgate - Defaulted to ''. String representing the parent gates of the new gate.
        - logicle - True if parent gate figure was generated with logicle else False.

        returns True if gate is added successfully and False if an error is encountered such as a duplicate gate.

        Implemented gating heiarchy handling. Actually creating the gate on FlowKit is still yet to be implemented.
        """
        if parentgate == '':
            # we need to first parse through
            self.gating_heiarchy[gatename] = {}
            self.gates[gatename] = Gates(gatename, verticies, self.samples, parent_x, parent_y, None, logicle)
        else:
            # a stack implementation of a recursive function that would find the parent gate in dictionaries
            stack = []
            stack.append(self.gating_heiarchy)
            a = False
            while len(stack) != 0:
                process = stack.pop()
                # Base case: the nested/entire dictionary is empty
                if len(list(process.keys())) != 0:
                    if parentgate in list(process.keys()):
                        # we found the nested dictionary containing the parent gate
                        a = process
                        break
                    else:
                        for i in list(process.keys()):
                            stack.append(process[i])
            if type(a) is dict:
                while len(self.gates[parentgate].processes) != 0:
                    for sample_name in list(self.gates[parentgate].processes.keys()):
                        p = self.gates[parentgate].processes[sample_name]
                        p.join()
                        del self.gates[parentgate].processes[sample_name]
                # parent gate must exist, if a == False, it doesnt
                a[parentgate][gatename] = {}
                parent = self.gates[parentgate] if parentgate != '' else None
                print(parent, parentgate)
                self.gates[gatename] = Gates(gatename, verticies, self.samples, parent_x, parent_y, parent, logicle)
                return True
            else:
                return False, "Parent gate does not exist"

    def generatefigure(self, sample_name, x, y="his", parent="", logicle=True, left=0, right=262144):
        """
        The method addgate is responsible for generating figures through mpl. 

        Input Parameteres:
        - sample_name - string of filename of sample
        - x - String of marker represented on the x axis.
        - y - String of marker represented on the y axis or "his" for a histogram. Defaults to "his"
        - parent - string representing the name of the parent gate. Defaults to ""
        - parentgate - Defaulted to ''. String representing the parent gates of the new gate.
        - logicle - True to apply logicle transformation else False. Defaults to True. Ideally use logicle transformation on all figures except for FSC, SSC and Time
        - left - min x and y values to be displayed. Defaults to 0, ignored if logicle transformation is applied.
        - left - min x and y values to be displayed. Defaults to 262144 (generally the max intensity value read by flow machines), ignored if logicle transformation is applied.

        returns MPL axes object if succesful and False if an error is encountered.

        Parent gate functionality still needs to be implemented.
        """
        #Get sample object
        sample = self.samples[sample_name]
        # Requested markers on figure must exist in the experiment
        if x not in sample.label_indicies.keys(): return False
        if y != "his" and y not in sample.label_indicies.keys(): return False
        # get events
        if parent != "":
            while sample_name in self.gates[parent].processes:
                p = self.gates[parent].processes[sample_name]
                p.join()
                del self.gates[parent].processes[sample_name]
            gate_indicies = self.gates[parent].indicies[sample_name]
            if logicle:
                plt_data = sample.get_xform_data(x, row_indicies=gate_indicies) if y == "his" else sample.get_xform_data(x, y, gate_indicies)
            else:
                plt_data = sample.get_comp_data(x, row_indicies=gate_indicies) if y == "his" else sample.get_comp_data(x, y, gate_indicies)
        else:
            if logicle:
                plt_data = sample.get_xform_data(x) if y == "his" else sample.get_xform_data(x, y)
            else:
                plt_data = sample.get_comp_data(x) if y == "his" else sample.get_comp_data(x, y)
        # to eliminate errors when generating figures, we will replace NaNs with 0
        counts = int(plt_data.size) if y == 'his' else int(plt_data.size / 2)
        plt_data = np.nan_to_num(plt_data)
        plt_data = plt_data[plt_data[:, 0]>=0, :]
        if y != "his": plt_data = plt_data[plt_data[:, 1] >= 0, :]
        # generate matplotlib plot
        f, ax = plt.subplots()
        if y == "his":
            ax.hist(plt_data, bins=150)
            ax.set_title("Histogram - " + x + " - " + str(counts) + " events")
            ax.set_xlabel(x)
            ax.set_ylabel("Counts")
            if not logicle: ax.set_xlim(left, right)
            return f, ax
        else:
            # sorting the data point by density
            ax.hist2d(plt_data[:, 0], plt_data[:, 1], bins=500, cmap = "jet", norm=colors.LogNorm())
            ax.set_title(x + " vs. " + y + " - " + str(counts) + " events")
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            if not logicle:  # Without logicle transformation, we may have outliers that scew the min and max values of the figure
                ax.set_xlim(left, right)
                ax.set_ylim(left, right)
            else:
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
            return f, ax

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
        for i, j in {"root": self.gating_heiarchy}.items():
            stack.append((0, i, j))
            while len(stack) != 0:
                lvl, key, val = stack.pop()
                returnstring += "|" + lvl * "---" + str(key) + "\n" if lvl != 0 else lvl * "---" + str(key) + "\n"
                for k, l in val.items():
                    stack.append((lvl + 1, k, l))
        return returnstring
    def export_statistics(self, filename, precision = 3):
        sample_names = list(self.samples.keys())
        export_data = {i + types:[] for i, j in self.gates.items() for types in [' Counts', ' Relative Parent Freq.']}
        gate_names = [i for i, j in self.gates.items()]
        export_data['Sample_Name'] = sample_names
        for samp_name in sample_names:
            for gate_name in gate_names:
                parent_events = len(self.samples[samp_name].all_ind) if self.gates[gate_name].parent is None else len(self.gates[gate_name].parent.indicies[samp_name])
                #get counts
                while samp_name in self.gates[gate_name].processes:
                    p = self.gates[gate_name].processes[samp_name]
                    p.join()
                    del self.gates[gate_name].processes[samp_name]
                print(len(self.gates[gate_name].indicies[samp_name]))
                sub_gate_events = len(self.gates[gate_name].indicies[samp_name])
                export_data[gate_name + " Counts"].append(sub_gate_events)
                #get relative parent freq
                rel_freq = (sub_gate_events / parent_events) * 100
                export_data[gate_name + " Relative Parent Freq."].append(round(rel_freq, precision))
        df = pd.DataFrame(export_data)
        df.set_index('Sample_Name', inplace = True)
        df.to_csv(filename)
        return True



#EXCLUDE SESSION SAVING FROM PROJECT
    def exportsession(self, filename="untitled"):
        """
        Saves all object data into a binary file with name defined by user (or defaulted to "untitled") with a .session file extension.

        Input Parameteres:
        - filename - String of file name in which all data will be saved to (excludes .session extension). Defaults to "untitled".

        returns True if saving process is sucessful or returns False if filename is empty
        """
        if len(filename) == 0:  # filename cannot be empty
            return False
        with open(filename + ".session", 'wb'):
            pickle.dump([self.filepath, self.samples, self.gateheiarchy], f)
        return True

    def restoresession(self, filename="untitled"):
        """
        Loads object data from a previous saved session file. 

        Input Parameteres:
        - filename - String of file name in which all data will be loaded from (excludes .session extension). Defaults to "untitled".

        returns True if loading process is sucessful or returns False if filename is empty
        """
        if len(filename) == 0:  # filename cannot be empty
            return False
        with open(filename + ".session", 'wb'):
            self.filepath, self.samples, self.gateheiarchy = pickle.load(f)
        return True
