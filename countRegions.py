#!/usr/local/bin/python2.7
from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gSystem,TF1, TFile
import ROOT as rt

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
    referenceHistPath = 'tau21sel/M_jj_AK8'
    # referenceHistPath = 'invMAk4sel_1p0/M_jj_AK8'
    IntegralMjj=DataFile.Get(referenceHistPath).Integral()
    print 'Integral_MjjAK8=',IntegralMjj

    return IntegralMjj
    

if(__name__=='__main__'):
    channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    # tau21selections=['tau21_35']
    tau21selections=['tau21sel_45','tau21sel_35']
    # tau21selections=['tau21sel_45']
    RegionPaths=[   '/nfs/dust/cms/user/albrechs/UHH2_Output/SignalRegion',
                    # '/nfs/dust/cms/user/albrechs/UHH2_Output/LOWSidebandRegion',
                    '/nfs/dust/cms/user/albrechs/UHH2_Output/HIGHSidebandRegion'
    ]
    for tau21sel in tau21selections:
        csv_out=open('%s_RegionComparison.csv'%tau21sel,'wt')
        csvwriter=csv.DictWriter(csv_out,fieldnames=['channel','NSignal','NSideband','N','NSideband/NSignal','NSideband/N'])
        csvwriter.writeheader()

        for channel in channels:
            filename='uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%channel


            N_Events=[]
            for path in RegionPaths:
                N_Events.append(CountRegion(path+'/'+tau21sel+'/'+filename))
            
                # print 'Signal/LowSideband:',N_Events[0]/N_Events[1]
            N_Signal=N_Events[0]+N_Events[1]    
            csvwriter.writerow({'channel':channel,
                                'NSignal':N_Events[0],
                                'NSideband':N_Events[1],
                                'N':N_Signal,
                                'NSideband/NSignal':N_Events[1]/N_Events[0],
                                'NSideband/N':N_Events[1]/N_Signal})

            print '##################################################################'
            print 'Channel:',channel
            print 'For N-Subjettiness-Selection (0<tau21<0.%s)'%tau21sel.split('_')[-1]
            print 'N_Signal in SignalRegion:',N_Events[0],'and in SidebandRegion:',N_Events[1],' (both N_Signal:',N_Signal,')'
            print 'N_Signal_Sideband/N_Signal:',N_Events[1]/N_Signal
            print 'N_Signal_Signal/N_Signal:',N_Events[0]/N_Signal
            print 'N_Signal_Signal/N_Signal_Sideband:',N_Events[0]/N_Events[1]
            print '##################################################################'
            print ''
