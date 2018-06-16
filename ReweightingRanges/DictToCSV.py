#!/usr/local/bin/python2.7
import csv,collections
from time import gmtime,strftime

def writeDict(dict,filename="range_%s"%strftime("%m_%d_%H_%M",gmtime()) ):
    anoinput={
        "S0":1,
        "S1":2,
        "M0":3,
        "M1":4,
        "M2":5,
        "M3":6,
        "M4":7,
        "M5":8,
        "M6":9,
        "M7":10,
        "T0":11,
        "T1":12,
        "T2":13,
        "T3":14,
        "T4":15,
        "T5":16,
        "T6":17,
        "T7":18,
        "T8":19,
        "T9":20}
        

    with open(filename+'.csv','w') as csvfile:
        print('opened file:',filename+'.csv')
        coloumns=['parameter','anoinput','Npoints','start','end','stepsize']
        writer = csv.DictWriter(csvfile,fieldnames=coloumns)
        writer.writeheader()
        for set in dict:
            writer.writerow({'parameter':set,
                             'anoinput':anoinput[set],
                             'Npoints':dict[set][0],
                             'start':dict[set][1],
                             'end':-dict[set][1],
                             'stepsize':dict[set][2]})
if(__name__=="__main__"):

    # sets={
    #     "S0":[91,-900.0,20.0],
    #     "S1":[67,-330.0,10.0],
    #     "M0":[85,-42.0,1.0],
    #     "M1":[67,-165.0,5.0],
    #     "M6":[85,-84.0,2.0],
    #     "M7":[121,-300.0,5.0],   
    #     "T0":[69,-6.8,0.2],
    #     "T1":[51,-12.5,0.5],
    #     "T2":[83,-20.5,0.5]}
    sets=collections.OrderedDict()

    sets['S0']=[83,-328.0,8]
    sets['S1']=[71,-1050,30]
    sets['M0']=[71,-105,3]
    sets['M1']=[71,-105,3]
    sets['M2']=[81,-200,5]
    sets['M3']=[81,-320,8]
    sets['M4']=[81,-320,8]
    sets['M5']=[81,-520,13]
    sets['M6']=[71,-210,6]
    sets['M7']=[85,-168,4]   
    sets['T0']=[91,-5.4,0.12]
    sets['T1']=[97,-1.44,0.03]
    sets['T2']=[71,-6.3,0.18]
    sets['T5']=[81,-28,0.7]
    sets['T6']=[81,-20,0.5]
    sets['T7']=[81,-56,1.4]
    sets['T8']=[81,-6,0.15]
    sets['T9']=[81,-12,0.3]
    
    channels=["ZChannels"]
    # channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    for channel in channels:
        writeDict(sets,'%sRange'%channel)
