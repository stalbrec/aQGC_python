#!/usr/local/bin/python2.7
from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gSystem,TF1, TFile
import ROOT as rt
referenceHistPath = 'tau21sel/M_jj_AK8'
# referenceHistPath = 'invMAk4sel_1p0/M_jj_AK8'
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
    # referenceHistPath = 'invMAk4sel_1p0/M_jj_AK8'
    IntegralMjj=DataFile.Get(referenceHistPath).Integral()
    print 'Integral_MjjAK8=',IntegralMjj

    return IntegralMjj
    
def getPurity(channel,region):
    
    UHHPath='/nfs/dust/cms/user/albrechs/UHH2_Output/%s'%region
    signal_filename=UHHPath+'/'+'uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%channel
    background_filenames=[UHHPath+'/'+'uhh2.AnalysisModuleRunner.MC.MC_QCD.root',
                          UHHPath+'/'+'uhh2.AnalysisModuleRunner.MC.MC_TT.root',
                          UHHPath+'/'+'uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_HT600ToInf.root',
                          UHHPath+'/'+'uhh2.AnalysisModuleRunner.MC.MC_ZJetsToQQ_HT600ToInf.root']

    Signal_File=TFile(signal_filename)
    N_Signal=Signal_File.Get(referenceHistPath).Integral()
    Signal_File.Close()
    N_Background=0
    for filename in background_filenames:
        Background_File=TFile(filename)
        N_Background=N_Background+Background_File.Get(referenceHistPath).Integral()
        Background_File.Close()
    return [N_Signal,N_Background,N_Signal/N_Background]
    
if(__name__=='__main__'):
    channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    regions=['SignalRegion','SidebandRegion']
    
    csv_out=open('RegionComparison_soverb_%s.csv'%referenceHistPath.split('/')[0],'wt')
    csvwriter=csv.DictWriter(csv_out,fieldnames=['channel','region','S','B','S/B'])
    csvwriter.writeheader()
    # for region in regions:
    #     print 'Region:',regio
    #     for channel in channels:       
    #         print '###########################################'
    #         print 'channel:',channel
    for channel in channels:        
        print '###########################################'
        print 'channel:',channel
        for region in regions:
            print 'Region:',region

            Purity=getPurity(channel,region)
            print color.BOLD+color.YELLOW+'S/B:'+str(Purity[2])+color.END
            csvwriter.writerow({'channel':channel,
                                'region':region,
                                'S':Purity[0],
                                'B':Purity[1],
                                'S/B':Purity[2]})
        print '###########################################'
                    
