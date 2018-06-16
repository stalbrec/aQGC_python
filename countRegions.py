#!/usr/local/bin/python2.7
from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gSystem,TF1, TFile
import ROOT as rt

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
referenceHistPath = 'tau21sel/M_jj_AK8'
# referenceHistPath = 'invMAk4sel_1p0/M_jj_AK8'
   
def magnitude(x):
    return int(math.floor(math.log10(x)))

gROOT.SetBatch(True)

def CountRegion(filename):
    region=''
    for substr in path.split('/'):
        if 'Region' in substr:
            region=substr
    print 'getting NEvents for Region:',region
    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    # DataFile = TFile(path+"/uhh2.AnalysisModuleRunner.Data.DATA.root")
    DataFile = TFile(filename)
    gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")
    IntegralMjj=DataFile.Get(referenceHistPath).Integral()
    print 'Integral_MjjAK8=',IntegralMjj

    return float(int(IntegralMjj))
    

if(__name__=='__main__'):
    channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    RegionPaths=[   '/nfs/dust/cms/user/albrechs/UHH2_Output/SignalRegion',
                    '/nfs/dust/cms/user/albrechs/UHH2_Output/SidebandRegion'
    ]
    csv_out=open('RegionComparison_%s.csv'%referenceHistPath.split('/')[0],'wt')
    csvwriter=csv.DictWriter(csv_out,fieldnames=['channel','NSignal','NSideband','N','NSideband/NSignal','NSideband/N'])
    csvwriter.writeheader()
    
    for channel in channels:
        print '##################################################################'
        print 'Channel:',channel
        
        filename='uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%channel
        N_Events=[]
        for path in RegionPaths:
            print path
            N_Events.append(CountRegion(path+'/'+filename))
        N=N_Events[0]+N_Events[1]    
        csvwriter.writerow({'channel':channel,
                            'NSignal':N_Events[0],
                            'NSideband':N_Events[1],
                            'N':N,
                            'NSideband/NSignal':N_Events[1]/N_Events[0],
                            'NSideband/N':N_Events[1]/N})
        
        print 'N_Signal in SignalRegion:',N_Events[0],'and in SidebandRegion:',N_Events[1],' (both N_Signal:',N,')'
        print 'N_Signal_Signal/N_Signal:',str(N_Events[0]/N)
        print color.BOLD+color.YELLOW+'N_Signal_Sideband/N_Signal_Signal:',str(N_Events[1]/N_Events[0])+color.END
        print '##################################################################'
        print ''
