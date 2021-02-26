import analysis as an
import matplotlib.pyplot as plt

filepath = "E:\\Flow\\flow-interface-project\\Testing\\data\\"
files = ['Specimen_001_BM3 Rag 849 Full Stain Thy_004.fcs']
comp = "compensation_matrix.csv"
session = an.Analysis()
session.importdata(filepath, files, comp)
ax = session.generatefigure('Specimen_001_BM3 Rag 849 Full Stain Thy_004.fcs', 'FSC-A', 'FSC-H', logicle = False)
plt.show()