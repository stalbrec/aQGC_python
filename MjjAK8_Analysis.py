import ParSet,subprocess,os


if(__name__=="__main__"):
    dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]

    limits=[]
    for op in dim8op:
        current_Set = ParSet.Set(op)
        current_Set.exportPlot(True)
        current_Set.calcLimits()
        print 'Limits:'
        print op,'-',current_Set.Limits

        limits.append(current_Set.Limits)
    

    filenames=["%s.eps"%op for op in dim8op]
    os.chdir("plots")
    subprocess.call(["gs","-sPAPERSIZE=a4","-sDEVICE=pdfwrite","-dNOPAUSE","-dBATCH","-dSAFER","-sOutputFile=plots.pdf"]+filenames)
    os.chdir("..")

    fout=open("new.tex","wt")
    with open("latex.txt","rt") as fin:
        for line in fin:
            fout.write(line.replace('X','(%.2f, %.2f)'%limits[dim8op.index(line[4:6])]))
