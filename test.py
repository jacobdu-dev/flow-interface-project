import analysis as an
import matplotlib.pyplot as plt
import time

filepath = "Testing\\data\\"
files = ['Specimen_001_BM3 Rag 849 Full Stain Thy_004.fcs',
		 'Specimen_001_BM3 Rag 850 Full Stain Thy_005.fcs',
		 'Specimen_001_KALxBM3 846 Full Stain Thy_001.fcs',
		 'Specimen_001_KALxBM3 847 Full Stain Thy_002.fcs',
		 'Specimen_001_KALxBM3 848 Full Stain Thy_003.fcs',
		 'Specimen_001_KQxBM3 838 Full Stain Thy_006.fcs',
		 'Specimen_001_KQxBM3 839 Full Stain Thy_007.fcs',
		 'Specimen_001_KQxBM3 840 Full Stain Thy_008.fcs']
comp = "compensation_matrix.csv"
session = an.Analysis()
session.importdata(filepath, files, comp)
session.addgate([(0, 6800), (206000,210000), (258000, 208000), (18000, 3200)], 'Singlet', 'FSC-A', 'FSC-H', logicle = False)
session.addgate([(19000,9000), (34000,25000), (222000, 40000), (225000, 27000), (177000, 8200)], 'Singlet', 'FSC-A', 'SSC-A', 'Singlet', logicle = False)
ax = session.generatefigure('Specimen_001_KQxBM3 838 Full Stain Thy_006.fcs', 'Qdot 605-A', 'Pacific Blue-A', logicle = True)
ax = session.generatefigure('Specimen_001_KQxBM3 838 Full Stain Thy_006.fcs', 'FSC-A', 'SSC-A', logicle = False)
plt.show()
while True: time.sleep(5)