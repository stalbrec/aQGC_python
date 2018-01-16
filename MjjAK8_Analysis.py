import RootClasses


if(__name__=="__main__"):
    dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    for op in dim8op:
        current_Set = RootClasses.Set(op)
        #current_Set.exportPlot()
        #current_Set.exportCalc()
