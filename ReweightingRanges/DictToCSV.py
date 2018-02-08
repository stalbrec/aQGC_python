#!/usr/local/bin/python2.7
import csv,collections
from time import gmtime,strftime

def writeDict(dict,filename="range_%s"%strftime("%m_%d_%H_%M",gmtime()) ):
    anoinput=collections.OrderedDict()
    anoinput['S0']=1
    anoinput['S1']=2
    anoinput['M0']=3
    anoinput['M1']=4
    anoinput['M6']=9
    anoinput['M7']=10
    anoinput['T0']=11
    anoinput['T1']=12
    anoinput['T2']=13
    with open(filename+'.csv','w') as csvfile:
        print 'opened file:',filename+'.csv'
        coloumns=['parameter','anoinput','Npoints','start','end','stepsize']
        writer = csv.DictWriter(csvfile,fieldnames=coloumns)
        writer.writeheader()
        for k in anoinput:
            writer.writerow({'parameter':k,
                            'anoinput':anoinput[k],
                            'Npoints':dict[k][0],
                            'start':dict[k][1],
                            'end':-dict[k][1],
                            'stepsize':dict[k][2]})
if(__name__=="__main__"):
    sets={
        "S0":[91,-900.0,20.0],
        "S1":[67,-330.0,10.0],
        "M0":[85,-42.0,1.0],
        "M1":[67,-165.0,5.0],
        "M6":[85,-84.0,2.0],
        "M7":[121,-300.0,5.0],   
        "T0":[69,-6.8,0.2],
        "T1":[51,-12.5,0.5],
        "T2":[83,-20.5,0.5]}
    channels=["WPWM","WMWM","WPZ","WMZ","ZZ"]
    for channel in channels:
        writeDict(sets,'%sRange'%channel)
