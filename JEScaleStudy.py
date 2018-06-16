#!/usr/local/bin/python2.7
from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TH1F,TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooCBShape,RooVoigtian,RooBreitWigner,RooFFTConvPdf,RooLandau,RooBifurGauss,RooPolynomial,RooChebychev
import ROOT as rt
from RooFitHist import RooFitHist

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
gStyle.SetOptStat(0)
gStyle.SetOptFit(0000)    
# gStyle.SetOptFit(1100)    
gStyle.SetOptTitle(0)
RooFit.SumW2Error(kTRUE)

if(__name__=='__main__'):
   channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
   # channels=['WMZ']
   # channels=['ZZ']
    
   # csv_out=open('RegionComparison_%s.csv'%referenceHistPath.split('/')[0],'wt')
   # csvwriter=csv.DictWriter(csv_out,fieldnames=['channel','NSignal','NSideband','N','NSideband/NSignal','NSideband/N'])
   # csvwriter.writeheader()
    
   for channel in channels:
      print '##################################################################'
      print 'Channel:',channel
      Files=[]
      Hists=[]
      directions= ['NOMINAL','UP','DOWN']
      for direction in directions:
         filename='/nfs/dust/cms/user/albrechs/UHH2_Output/JEScaleStudy/%s/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%(direction,channel)
         gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
         Files.append(TFile(filename))
         # Hists.append(Files[-1].Get('tau21sel/M_jj_AK8_highbin'))
         Hists.append(Files[-1].Get('invMAk4sel_1p0/M_jj_AK8_highbin'))
         gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")
      for i in range(len(directions)):
         print '##################################################################'
         print '##################################################################'
         print directions[i]
         print '##################################################################'
         print '##################################################################'
         RooFitHist(Hists[i],channel+'_'+directions[i],'test')
      for File in Files:
         File.Close()
        # VVcanv=TCanvas('VV','VV',700,700)
        # VVcanv.SetLogy()
        # VVcanv.SetLeftMargin(0.20) 
        # VVcanv.cd()
    
        # csvwriter.writerow({'channel':channel,
        #                     'NSignal':N_Events[0],
        #                     'NSideband':N_Events[1],
        #                     'N':N,
        #                     'NSideband/NSignal':N_Events[1]/N_Events[0],
        #                     'NSideband/N':N_Events[1]/N})
        # print '##################################################################'
        # print ''
