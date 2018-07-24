import os, shutil, subprocess, glob, csv


if(__name__=="__main__"):
    BosonChannel="VV"
    operators=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]

    NPoint=0
    snippet=''
    
    with open('ReweightingRanges/'+BosonChannel+'Range.csv','rb') as csvfile:
        setreader=csv.DictReader(csvfile)
        for row in setreader:
            NPoint+=int(row['Npoints'])
    for i in range(NPoint):
        snippet+='<InputData Lumi="1624.87" NEventsMax="-1" Type="MC" Version="MC_aQGC_ZZjj_hadronic_%i" Cacheable="False">\n'%i
        snippet+='&aQGCZZPreSelection;\n'
        snippet+='<InputTree Name="AnalysisTree" />\n'
        snippet+='</InputData>\n'
        # snippet+='\n'
        
    with open("PDFStudy/XML-Snippet.xml","wt") as fout:
        fout.write(snippet)
