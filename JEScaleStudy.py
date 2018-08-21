#!/usr/local/bin/python2.7
from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TH1F,TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList, RooArgSet, RooCBShape,RooVoigtian,RooBreitWigner,RooFFTConvPdf,RooLandau,RooBifurGauss,RooPolynomial,RooChebychev, RooExtendPdf
import ROOT as rt

def BifurFitHist(inputhist,title='title',sigL=-1,sigR=-1):
   fitbinning=array('d')
   binwidth=200
   NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
   for i in range(NBins+1):
      fitbinning.append(1050+i*binwidth)

   hist=inputhist.Rebin(NBins,"fit parameter",fitbinning) 
   meanstart=hist.GetBinCenter(hist.GetMaximumBin())
   sigmastart=hist.GetRMS()
   print('meanstart:',meanstart,'sigmastart:',sigmastart)

   gStyle.SetOptFit(1100)

   gStyle.SetOptTitle(0)
   RooFit.SumW2Error(kTRUE)
   
   mjj=RooRealVar('mjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
   mjjral=RooArgList(mjj)
   dh=RooDataHist('dh','dh',mjjral,RooFit.Import(hist))
  
   #BifurGauss
   if(sigL==-1):
      BifurGausslsigma= RooRealVar('#sigma_{left}','mass resolution',sigmastart,0,2*sigmastart)
   else:
      BifurGausslsigma= RooRealVar('#sigma_{left}','mass resolution',sigL)
   if(sigR==-1):
      BifurGaussrsigma= RooRealVar('#sigma_{right}','mass resolution',sigmastart,0,2*sigmastart)
   else:
      BifurGaussrsigma= RooRealVar('#sigma_{right}','mass resolution',sigR)

   BifurGaussmean=RooRealVar('#mu_{BifurGauss}','mean BifurGauss',meanstart,0,2*meanstart)
   BifurGauss=RooBifurGauss('BifurGauss','BifurGauss',mjj,BifurGaussmean,BifurGausslsigma,BifurGaussrsigma)
   fname='Bifur-Gaus'
   nBiFur=RooRealVar("N","number of signal events",500,0.,10000);
   shape=RooExtendPdf("BifurGauss_N","BifurGauss_N",BifurGauss,nBiFur);

   plottitle='%s Fit of %s'%(fname,title)
   # shape=BifurGauss
   shape.fitTo(dh,RooFit.SumW2Error(True))
   
   frame=mjj.frame(RooFit.Title(plottitle))
   frame.GetYaxis().SetTitleOffset(2)
      
   dh.plotOn(frame,RooFit.MarkerStyle(4))
   shape.plotOn(frame,RooFit.LineColor(2))
      
   ndof=dh.numEntries()-3
      
   #chiSquare legend
   chi2 = frame.chiSquare()
   probChi2 = TMath.Prob(chi2*ndof, ndof)
   chi2 = round(chi2,2)
   probChi2 = round(probChi2,2)
   leg = TLegend(0.5,0.5,0.9,0.65)
   leg.SetBorderSize(0)
   leg.SetFillStyle(0)
   shape.paramOn(frame, RooFit.Layout(0.5,0.9,0.9))
   leg.AddEntry(0,'#chi^{2} ='+str(chi2),'')
   leg.AddEntry(0,'Prob #chi^{2} = '+str(probChi2),'')
   leg.SetTextSize(0.04)
   frame.addObject(leg)
      
   canv=TCanvas(plottitle,plottitle,700,700)
   canv.SetLogy()
   canv.SetLeftMargin(0.20) 
   canv.cd()
      
   frame.SetMinimum(10**(-1))
      
   frame.Draw()
   plot_dir='JES_Study'
   if not os.path.exists(plot_dir):
      os.makedirs(plot_dir)        
   canv.Print(plot_dir+'/%s__%s.eps'%(title,fname))
   del canv
   return(BifurGaussmean.getVal(),BifurGausslsigma.getVal(),BifurGaussrsigma.getVal())
          
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
   # channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
   # channels=['WMZ']
   channels=['ZZ']
    
   # csv_out=open('RegionComparison_%s.csv'%referenceHistPath.split('/')[0],'wt')
   # csvwriter=csv.DictWriter(csv_out,fieldnames=['channel','NSignal','NSideband','N','NSideband/NSignal','NSideband/N'])
   # csvwriter.writeheader()
    
   for channel in channels:
      print('##################################################################')
      print('Channel:',channel)
      Files=[]
      Hists=[]
      directions= ['NOMINAL','UP','DOWN']
      for direction in directions:
         # filename='/nfs/dust/cms/user/albrechs/UHH2_Output/JEScaleStudy/%s/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%(direction,channel)
         filename='/nfs/dust/cms/user/albrechs/UHH2_Output/JEScaleStudy/%s/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root'%(direction,channel)
         gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
         Files.append(TFile(filename))
         # Hists.append(Files[-1].Get('tau21sel/M_jj_AK8_highbin'))
         Hists.append(Files[-1].Get('invMAk4sel_1p0/M_jj_AK8_highbin'))
         gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")
      means=[]
      for i in range(len(directions)):
         print('##################################################################')
         print('##################################################################')
         print(directions[i])
         print('##################################################################')
         print('##################################################################')
         if('NOMINAL' in directions[i]):
            nominalWidths=BifurFitHist(Hists[i],channel+'_'+directions[i])
            means.append(nominalWidths[0])
         else:
            means.append(BifurFitHist(Hists[i],channel+'_'+directions[i]+'_fixed_Sigmas',nominalWidths[1],nominalWidths[2])[0])
            means.append(BifurFitHist(Hists[i],channel+'_'+directions[i])[0])
      
      # for i in range(len(directions)):
      #    print directions[i], ' : ',means[i]
      #    print tf1[i]

            # for File in Files:
      #    File.Close()
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
        # print('##################################################################')
        # print('')
