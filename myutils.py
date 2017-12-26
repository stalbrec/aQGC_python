from ROOT import gROOT, TCanvas, TF1, TFile
import myutils,shutil,os
gROOT.Reset()


def getParName(set, startx, increment, i):
    name="M_jj_AK8_%s_"%set
    parameter=10*startx+i*10*increment
    if(parameter>=0):
        name+="%ip%i"%(parameter/10,parameter%10)
    else:
        name+="m%ip%i"%(-parameter/10,-parameter%10)    
    #print name
    return name

def getHistNames(set,histname):
    # S0=[91,20,-900,900]
    # S1=[67,10,-330,330]
    # M0=[85,1,-42,42]
    # M1=[67,5,-165,165]
    # M6=[84,2,-84,82]
    # M7=[121,5,-300,300]
    # T0=[69,0.2,-6.8,6.8]
    # T1=[51,0.5,-12.5,12.5]
    # T2=[83,0.5,-20.5,20.5]
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
    for i in range(0,sets[set][0]):
        histname.append(getParName(set,sets[set][1],sets[set][2],i)) 

def getHistNamesold(histname):
    #S0=[91,20,-900,900]
    for i in range(0,91):
        histname.append(getParName("S0",-900.0,20.0,i))
    # S1=[67,10,-330,330]
    for i in range(0,67):
        histname.append(getParName("S1",-330.0,10.0,i))
    # M0=[85,1,-42,42]
    for i in range(0,85):
        histname.append(getParName("M0",-42.0,1.0,i))
    # M1=[67,5,-165,165]
    for i in range(0,67):
        histname.append(getParName("M1",-165.0,5.0,i))
    # M6=[84,2,-84,82]
    for i in range(0,85):
        histname.append(getParName("M6",-84.0,2.0,i))
    # M7=[121,5,-300,300]
    for i in range(0,121):
        histname.append(getParName("M7",-300.0,5.0,i))
    # T0=[69,0.2,-6.8,6.8]
    for i in range(0,69):
        histname.append(getParName("T0",-6.8,0.2,i))
    # T1=[51,0.5,-12.5,12.5]
    for i in range(0,51):
        histname.append(getParName("T1",-12.5,0.5,i))
    # T2=[83,0.5,-20.5,20.5]
    for i in range(0,83):
        histname.append(getParName("T2",-20.5,0.5,i)) 
