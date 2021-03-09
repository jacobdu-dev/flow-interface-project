from analysis import Analysis
import matplotlib.pyplot as plt
prompt = """
Usage:
gf - Generate Figure
gc - Generate Gate
rg - Retrieve Gate Heiarchy
rs - Retrieve Statistics
q - Quit Program
"""

def main():
	flow = Analysis()
	#Importing of data
	while True:
		a = str(input("Please specify relative filepath of FCS files and Compensation Matrix CSV with '/' at the end of last directory:\n"))
		if '/' not in a:
			print("Invalid filepath!")
			continue
		else:
			filepath = a
			a = str(input("Please specify all FCS files to be imported separated by ';' (eg. 'sample1.fcs;sample2.fcs' ):\n"))
			if ('fcs' not in a) and ('FCS' not in a):
				print("Invalid flow cytometry data files.")
				continue
			files = a.split(';')
			a = str(input("Please specify file name of compensation matrix:\n"))
			if 'csv' not in a:
				print("Invalid flow cytometry data files.")
				continue
			comp = a
			print("Importing Data...")
			flow.importdata(filepath, files, comp)
			break
	flowsamples = list(flow.samples.keys())
	sampleid = {i:flowsamples[i] for i in range(len(flowsamples))}
	while True:

		print(prompt)
		a = str(input("What would you like to do? (gf/gc/rg/rs) :"))
		if a == 'gf':
			while True:
				for i, smplename in sampleid.items():
					print("{} - {}".format(i, smplename))
				a = int(input("Please enter the ID of the sample you would like to generate a figure for or e to exit. ({}-{}/e) :".format(0, len(sampleid) - 1)))
				if (a < 0) or (a >= len(sampleid)):
					print("Invalid input.")
					continue
				elif a == 'e':
					break
				else:
					samplename = sampleid[a]
				channels = flow.samples[samplename].channels
				labels = {channels[i]['PnN']: i for i in channels.keys()}
				print("Valid Sample Makers:")
				for marker, i in labels.items():
					if (int(i) > 4) and (int(i) < len(channels)):
						print("{} - {}({})".format(i, marker, channels[i]['PnS']))
					else:
						print("{} - {}".format(i, marker))
				a = str(input("Please enter the markers to be shown on the x and y axis in the format 'x;y'. A histogram will be generated if only one ID is entered ({}-{};{}-{}/{}-{}/e) :".format(1, len(channels), 1, len(channels), 1, len(channels))))
				if a == 'e':
					break
				else:
					list_x_y = a.split(';')
					if len(list_x_y) > 2: 
						print("Invalid input.")
						continue
					else:
						for i in range(len(list_x_y)):
							for j in list_x_y[i]:
								if j not in "0123456789":
									print("Invalid input.")
									continue
				x_label = channels[list_x_y[0]]['PnN']
				y_label = channels[list_x_y[1]]['PnN'] if len(list_x_y) > 1 else "his"
				a = str(input("Would you like the figure to be shown on a logicle scale? (y/n/e) :"))
				if a == 'y':
					logicle = True
				elif a == 'n':
					logicle = False
				elif a == 'e':
					break
				else:
					print("Invalid input.")
					continue
				if len(flow.gates) > 0:
					valgates = {i + 1 :flow.gates[i] for i in range(len(flow.gates))}
					print("Valid Parent Gate(s): ")
					print("0 - None")
					for i, parentgates in valgates.items():
						print("{} - {}".format(i, parentgates))
					a = int(input("Please enter the ID of the parent gate. ({}-{}/e) :".format(0, len(valgates))))
					if a > len(valgates):
						print("Invalid input.")
						continue
					parent = "" if a == 0 else valgates[a]
					ax = flow.generatefigure(samplename, x_label, y_label, parent, logicle)
				else:
					ax = flow.generatefigure(samplename, x_label, y_label, logicle = logicle)
				plt.show()
				print()
				#ask if user would like to create a gate off that figure



		elif a == 'gc':
			pass
		elif a == 'rg':
			pass
		elif a == 'rs':
			pass
		elif a == 'q':
			quit()
		else:
			print("Invalid input!")
			continue




if __name__ == "__main__":
	main()