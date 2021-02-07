import flowkit as fk
from bokeh.plotting import show


thysamples = ['Specimen_001_BM3 Rag 849 Full Stain Thy_004.fcs',
              'Specimen_001_BM3 Rag 850 Full Stain Thy_005.fcs',
              'Specimen_001_KALxBM3 846 Full Stain Thy_001.fcs',
              'Specimen_001_KALxBM3 847 Full Stain Thy_002.fcs',
              'Specimen_001_KALxBM3 848 Full Stain Thy_003.fcs',
              'Specimen_001_KQxBM3 838 Full Stain Thy_006.fcs',
              'Specimen_001_KQxBM3 839 Full Stain Thy_007.fcs',
              'Specimen_001_KQxBM3 840 Full Stain Thy_008.fcs']
print("Importing FCS files... Please wait...")

fks = fk.Session()

compsamp = {}
"""for i in compensations:
    compsamp[i] = fk.Matrix(i, "data/" + i, )"""
# comps = fk.Matrix(i, "data/" + i, )

thysample = {}
for i in thysamples:
    thysample[i] = fk.Sample("data/" + i)
userselection = [thysamples[i] for i in range(len(thysamples))]
while True:
    for i in range(len(userselection)):
        print(i, userselection[i])
    sample = int(input())
    sam = thysample[userselection[sample]]
    print(sam.channels)
    # sam.apply_compensation('data/comps.csv')
    fks.add_samples(sam)
    fks.add_sample_group("Thy")
    fks.assign_sample(userselection[sample], "Thy")
    fks.add_gate(gate=fk.gates.PolygonGate(gate_id="Singlets", parent_id=None,
                                           dimensions=[fk.Dimension('FSC-A'), fk.Dimension('FSC-H')],
                                           vertices=[fk.Vertex((0, 20000)), fk.Vertex((240000, 225000)),
                                                     fk.Vertex((240000, 150000)),
                                                     fk.Vertex((1000, 1000))]))
    # a = fks.plot_scatter(userselection[sample], fk.Dimension('FSC-A'), fk.Dimension('SSC-A'), gate_id="Singlets")
    # a = fks.plot_gate("Thy", userselection[sample], 0)#fk.Dimension('FSC-A'), fk.Dimension('SSC-A'), gate_id=0)
    # show(a)
    fks.add_gate(
        gate=fk.gates.PolygonGate(gate_id="Thymocytes", parent_id="Singlets",
                                  dimensions=[fk.Dimension('FSC-A'), fk.Dimension('SSC-A')],
                                  vertices=[fk.Vertex((27000, 19000)), fk.Vertex((190000, 40000)),
                                            fk.Vertex((170000, 7000)), fk.Vertex((19000, 9600))]))
    fks.add_transform(fk.transforms.LogicleTransform('logicle_xform', param_t=262144.0,
                                                               param_w=1.0,
                                                               param_m=4.418539922,
                                                               param_a=0.0))
    a = fks.plot_scatter(userselection[sample], fk.Dimension('Qdot 605-A', transformation_ref="logicle_xform"),
                         fk.Dimension('Pacific Blue-A', transformation_ref="logicle_xform"))#, gate_id="Thymocytes")
    show(a)
    # a = fks.plot_gate("Thy",0,'FSC-A', 'SSC-A', source='raw', gate_id=0)
    # show(a)
