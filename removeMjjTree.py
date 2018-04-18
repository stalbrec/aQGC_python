#!/usr/bin/python
import shutil,os
import ROOT as rt
from ROOT import *

if(__name__=='__main__'):
    regions=['SignalRegion','SidebandRegion']
    
    # samples=['MC.MC_aQGC_WPWPjj_hadronic']
    samples=['MC.MC_aQGC_WPWPjj_hadronic','MC.MC_aQGC_WPWMjj_hadronic','MC.MC_aQGC_WMWMjj_hadronic','MC.MC_aQGC_WPZjj_hadronic','MC.MC_aQGC_WMZjj_hadronic','MC.MC_aQGC_ZZjj_hadronic',
             'MC.MC_QCD',
             'Data.DATA_JetHT']
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/'
    for region in regions:
        for sample in samples:
            FileName=path+region+'/uhh2.AnalysisModuleRunner.'+sample+'.root'
            if(not os.path.isfile(FileName)):
                print 'file', FileName,'does not exist'
                continue
            newFileName=FileName[:FileName.find('.root')]+'_noscan.root'
            if('Data' in FileName):                
                newFileName=path+region+'/uhh2.AnalysisModuleRunner.Data.DATA.root'
            print 'newFileName:',newFileName
            shutil.copyfile(FileName,newFileName)
            File=TFile(newFileName,'UPDATE')
            keyList=File.GetListOfKeys()
            for key in keyList:
                if 'Mjj' in key.GetName():
                    print 'deleting',key.GetName()
                    gDirectory.Delete(key.GetName()+';1')
            gDirectory.Delete('AnalysisTree;1')
            File.Close()

