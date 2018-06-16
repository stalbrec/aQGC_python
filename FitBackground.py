from array import array
import csv,collections,numpy
import ROOT as rt
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooFormulaVar,RooGenericPdf

if(__name__=='__main__'):

    gROOT.SetBatch(True)
    
    # SD_REGION='Signal'
    # REGION='SignalRegion'
    REGION='SidebandRegion'
    #File=TFile('/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/input/ZZ_S0_16p00.root','READ')
    # File=TFile('/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/backup/uhh2.AnalysisModuleRunner.Data.DATA.root','READ')
    File=TFile('/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/backup/uhh2.AnalysisModuleRunner.MC.MC_QCD.root','READ')

    # VVHist_1GeV= File.Get('qcd_invMass')
    # VBFHist_1GeV= File.Get('qcd_invMass_afterVBFsel')
    VVHist_1GeV= File.Get('VVRegion/M_jj_AK8_highbin')
    VBFHist_1GeV= File.Get('invMAk4sel_1p0/M_jj_AK8_highbin')


    VVHist_1GeV.Scale(1./VVHist_1GeV.Integral(),'width')
    VBFHist_1GeV.Scale(1./VBFHist_1GeV.Integral(),'width')
    
    # RooFit.gErrorIgnoreLevel = RooFit.kInfo
    fitbinning=array('d')
    binwidth=200
    #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
    NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
    for i in range(NBins+1):
        fitbinning.append(1050+i*binwidth)
    #print fitbinning
    
    VVHist_100GeV=VVHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)
    VBFHist_100GeV=VBFHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)


    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0000)    
    # gStyle.SetOptFit(1100)    
    gStyle.SetOptTitle(0)
    RooFit.SumW2Error(kTRUE)
    
    # VVmjj=RooRealVar('VVmjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
    # VVmjjral=RooArgList(VVmjj)
    # VVdh=RooDataHist('VVdh','VVdh',VVmjjral,RooFit.Import(VVHist_100GeV))

    # VVx=RooFormulaVar('VVx','','@0/13000',RooArgList(VVmjj))
    # VVp0=RooRealVar('VVp0','VVp0_',1.0,1000000000)
    # VVp1=RooRealVar('VVp1','VVp1_',5,-100,100)

    # VVShape=RooGenericPdf('VVShape','VV','@1/pow(@0,@2)',RooArgList(VVx,VVp0,VVp1))

    
    # VBFmjj=RooRealVar('VBFmjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
    # VBFmjjral=RooArgList(VBFmjj)
    # VBFdh=RooDataHist('VBFdh','VBFdh',VBFmjjral,RooFit.Import(VBFHist_100GeV))
    
    # VBFx=RooFormulaVar('VBFx','','@0/13000',RooArgList(VBFmjj))    
    # VBFp0=RooRealVar('VBFp0','VBFp0_',1.0,1000000000)
    # VBFp1=RooRealVar('VBFp1','VBFp1_',5,-100,100)

    # VBFShape=RooGenericPdf('VBFShape','VBF','@1/pow(@0,@2)',RooArgList(VBFx,VBFp0,VBFp1))

    # VVShape.fitTo(VVdh, RooFit.Strategy(1),RooFit.Minos(kFALSE), RooFit.Range(1050,13000),RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE),RooFit.PrintEvalErrors(-1))
    # VBFShape.fitTo(VBFdh, RooFit.Strategy(1),RooFit.Minos(kFALSE), RooFit.Range(1050,13000),RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE),RooFit.PrintEvalErrors(-1))
    
    # VVndof=VVdh.numEntries()-2
    # VBFndof=VBFdh.numEntries()-2

    twopar='[0]/TMath::Power(x/13000,[1])'
    threepar='[0]*TMath::Power((1-x)/13000,[2])/TMath::Power(x/13000,[1])'
    VV_MAXIMUM=0
    for i in range(VVHist_100GeV.GetNbinsX()):
        if(VVHist_100GeV.GetBinContent(i)>0):
            VV_MAXIMUM=VVHist_100GeV.GetBinCenter(i)

    VBF_MAXIMUM=0
    for i in range(VBFHist_100GeV.GetNbinsX()):
        if(VBFHist_100GeV.GetBinContent(i)>0):
            VBF_MAXIMUM=VBFHist_100GeV.GetBinCenter(i)
            
    
    VVcanv=TCanvas('VV','VV',700,700)
    VVcanv.SetLogy()
    VVcanv.SetLeftMargin(0.20) 
    VVcanv.cd()
    # threeparfunc=TF1('3par',threepar,1050,FIT_MAX)
    # threeparfunc.SetParameter(0,0.001)
    # threeparfunc.SetParameter(1,10)
    # threeparfunc.SetParameter(0,0)
   
    # twoparfunc=TF1('2par',twopar,1050,FIT_MAX)
    # twoparfunc.SetParameter(0,0.001)
    # twoparfunc.SetParameter(1,10)

    # VVHist_100GeV.Draw('PE1')
    # test=raw_input('press enter to continue')    
    fitfunc=twopar
    
    VVTF1=TF1('VVTF1',fitfunc,1050,VV_MAXIMUM)
    VVTF1.SetParameter(0,0.001)
    VVTF1.SetParameter(1,10)
    VVHist_100GeV.Fit('VVTF1','R')
    VVHist_100GeV.SetMarkerStyle(8)
    VVHist_100GeV.SetLineColor(1)
    VVHist_100GeV.GetYaxis().SetRangeUser(10**(-6),10)
    VVHist_100GeV.GetXaxis().SetRangeUser(0,VV_MAXIMUM+1000)
    VVHist_100GeV.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    VVHist_100GeV.GetYaxis().SetTitle('Normalized # Events')
    VVHist_100GeV.GetYaxis().SetTitleOffset(2)
    VVHist_100GeV.Draw('PE1')
    VVTF1.Draw('SAME')

    print 'chi2/ndf:',VVTF1.GetChisquare(),'/',VVTF1.GetNDF()

    latex=TLatex()
    latex.SetNDC(kTRUE)
    latex.SetTextSize(0.03)
    # latex.DrawLatex(0.52,0.953,"%.2f fb^{-1} (13 TeV)"%36.1)
    latex.DrawLatex(0.45,0.65,"#chi^{2}/ndof=%.2f/%.2f=%.2f"%(VVTF1.GetChisquare(),VVTF1.GetNDF(),VVTF1.GetChisquare()/VVTF1.GetNDF()))
    # latex.Draw("SAME")
    
    VVleg = TLegend(0.45,0.7,0.9,0.9)
    VVleg.SetBorderSize(0)
    VVleg.SetFillStyle(0)
    VVleg.AddEntry(VVHist_100GeV,'QCD-!VBF','p')
    VVleg.AddEntry(VVTF1,'QCD-!VBF Fit (p_{0}/(x/#sqrt{s})^{p_{1}}','l')
    VVleg.SetTextSize(0.03)
    VVleg.Draw('SAME')
   
    VVcanv.Print(REGION+'_VVRegion.eps')

    VBFcanv=TCanvas('VBF','VBF',700,700)
    VBFcanv.SetLogy()
    VBFcanv.SetLeftMargin(0.20) 
    VBFcanv.cd()

    VBFTF1=TF1('VBFTF1',fitfunc,1050,VBF_MAXIMUM)
    VBFTF1.SetParameter(0,1)
    VBFTF1.SetParameter(1,5)
    VBFTF1.SetLineColor(rt.kBlue)
    VBFHist_100GeV.Fit('VBFTF1','R')
    VBFHist_100GeV.SetMarkerStyle(8)
    VBFHist_100GeV.SetLineColor(1)
    VBFHist_100GeV.GetXaxis().SetRangeUser(0,VV_MAXIMUM+1000)
    VBFHist_100GeV.GetYaxis().SetRangeUser(10**(-6),10)
    VBFHist_100GeV.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    VBFHist_100GeV.GetYaxis().SetTitle('Normalized # Events')
    VBFHist_100GeV.GetYaxis().SetTitleOffset(2)
    VBFHist_100GeV.Draw('PE1')
    VBFTF1.Draw('SAME')
    VVTF1.Draw('SAME')
    print 'chi2/ndf:',VBFTF1.GetChisquare(),'/',VBFTF1.GetNDF()

    latexvbf=TLatex()
    latexvbf.SetNDC(kTRUE)
    latexvbf.SetTextSize(0.03)
    latexvbf.DrawLatex(0.45,0.65,"#chi^{2}/ndof=%.2f/%.2f=%.2f"%(VBFTF1.GetChisquare(),VBFTF1.GetNDF(),VBFTF1.GetChisquare()/VBFTF1.GetNDF()))

    
    VBFleg = TLegend(0.45,0.7,0.9,0.9)
    VBFleg.SetBorderSize(0)
    VBFleg.SetFillStyle(0)
    VBFleg.AddEntry(VBFHist_100GeV,'QCD-VBF','p')
    VBFleg.AddEntry(VBFTF1,'QCD-VBF Fit (p_{0}/(x/#sqrt{s})^{p_{1}}','l')
    VBFleg.AddEntry(VVTF1,'QCD-!VBF Fit (p_{0}/(x/#sqrt{s})^{p_{1}}','l')
    VBFleg.SetTextSize(0.03)
    VBFleg.Draw('SAME')

    VBFcanv.Print(REGION+'_VBFRegion.eps')

    
 
