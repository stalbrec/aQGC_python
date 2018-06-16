from array import array
import csv,collections,numpy
import ROOT as rt
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooFormulaVar,RooGenericPdf

if(__name__=='__main__'):
    File=TFile('/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/input/ZZ_S0_16p00.root','READ')
    VVHist_1GeV= File.Get('qcd_invMass')
    VBFHist_1GeV= File.Get('qcd_invMass_afterVBFsel')
    
    # RooFit.gErrorIgnoreLevel = RooFit.kInfo
    fitbinning=array('d')
    binwidth=100
    #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
    NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
    for i in range(NBins+1):
        fitbinning.append(1050+i*binwidth)
    # print(fitbinning)
    
    VVHist_100GeV=VVHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)
    VBFHist_100GeV=VBFHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)

    gStyle.SetOptFit(1100)    
    gStyle.SetOptTitle(0)
    RooFit.SumW2Error(kTRUE)
    
    VVmjj=RooRealVar('VVmjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
    VVmjjral=RooArgList(VVmjj)
    VVdh=RooDataHist('VVdh','VVdh',VVmjjral,RooFit.Import(VVHist_100GeV))

    VVx=RooFormulaVar('VVx','','@0/13000',RooArgList(VVmjj))
    VVp0=RooRealVar('VVp0','VVp0_',1.0,1000000000)
    VVp1=RooRealVar('VVp1','VVp1_',5,-100,100)

    VVShape=RooGenericPdf('VVShape','VV','@1/pow(@0,@2)',RooArgList(VVx,VVp0,VVp1))

    
    # VBFmjj=RooRealVar('VBFmjj','M_{jj-AK8}',fitbinning[0],fitbinning[len(fitbinning)-1],'GeV')
    # VBFmjjral=RooArgList(VBFmjj)
    # VBFdh=RooDataHist('VBFdh','VBFdh',VBFmjjral,RooFit.Import(VBFHist_100GeV))
    
    # VBFx=RooFormulaVar('VBFx','','@0/13000',RooArgList(VBFmjj))

    VBFdh=RooDataHist('VBFdh','VBFdh',VVmjjral,RooFit.Import(VBFHist_100GeV))
    
    VBFx=RooFormulaVar('VBFx','','@0/13000',RooArgList(VVmjj))

    VBFp0=RooRealVar('VBFp0','VBFp0_',1.0,1000000000)
    VBFp1=RooRealVar('VBFp1','VBFp1_',5,-100,100)

    VBFShape=RooGenericPdf('VBFShape','VBF','@1/pow(@0,@2)',RooArgList(VBFx,VBFp0,VBFp1))


    
    # VVShape.fitTo(VVdh, RooFit.Strategy(1),RooFit.Minos(kFALSE), RooFit.Range(1050,13000),RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE),RooFit.PrintEvalErrors(-1))
    
    # VVframe=VVmjj.frame(RooFit.Title('VVFrame'))
    # VVdh.plotOn(VVframe,RooFit.Name("VVdh"),RooFit.MarkerStyle(4))
    # VVShape.plotOn(VVframe,RooFit.Name("VVShape"),RooFit.LineColor(rt.kRed))

    # VVndof=VVdh.numEntries()-2

    # VVcanv=TCanvas('VV','VV',700,700)
    # VVcanv.SetLogy()
    # VVcanv.SetLeftMargin(0.20) 
    # VVcanv.cd()

    # #chiSquare legend
    # VVchi2 = VVframe.chiSquare()
    # # VVchi2 = VVframe.chiSquare('VVShape','VVdh',2)
    # VVprobChi2 = TMath.Prob(VVchi2*VVndof, VVndof)
    # VVchi2 = round(VVchi2,2)
    # VVprobChi2 = round(VVprobChi2,2)

    # # VVShape.paramOn(VVframe, RooFit.Layout(0.5,0.9,0.9))
    

    # VVleg = TLegend(0.7,0.7,0.9,0.9)
    # VVleg.SetBorderSize(1)
    # VVleg.SetFillStyle(0)
    # VVleg.AddEntry(VVframe.FindObject("VVdh"),"QCD-VV","P")
    # VVleg.AddEntry(VVframe.FindObject("VVShape"),"VVShape","L")
    # # VVleg.AddEntry(0,'#chi^{2} ='+str(VVchi2),'')
    # # VVleg.AddEntry(0,'Prob #chi^{2} = '+str(probChi2),'')
    # VVleg.SetTextSize(0.02)
    # VVframe.addObject(VVleg)
            
    # VVframe.SetMinimum(10**(-3))
    
    # VVframe.Draw()

    # VVcanv.Print('VVRegion.eps')

    VVShape.fitTo(VVdh, RooFit.Strategy(1),RooFit.Minos(kFALSE), RooFit.Range(1050,13000),RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE),RooFit.PrintEvalErrors(-1))
    VBFShape.fitTo(VBFdh, RooFit.Strategy(1),RooFit.Minos(kFALSE), RooFit.Range(1050,13000),RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE),RooFit.PrintEvalErrors(-1))

    VBFframe=VVmjj.frame(RooFit.Title('VBFFrame'))
    # VBFframe.GetXaxis().SetRangeUser(0,5000)
    # VBFframe.GetYaxis().SetRangeUser(10**(-6),100)
    VBFdh.plotOn(VBFframe,RooFit.Name("VBFdh"),RooFit.MarkerStyle(4))
    VBFShape.plotOn(VBFframe,RooFit.Name("VBFShape"),RooFit.LineColor(rt.kBlue))
    VVShape.plotOn(VBFframe,RooFit.Name("VVShape"),RooFit.LineColor(rt.kRed),RooFit.LineStyle(rt.kDashed))

    VBFndof=VBFdh.numEntries()-2

    VBFcanv=TCanvas('VBF','VBF',700,700)
    VBFcanv.SetLogy()
    VBFcanv.SetLeftMargin(0.20) 
    VBFcanv.cd()

    #chiSquare legend
    VBFchi2 = VBFframe.chiSquare()
    # VBFchi2 = VBFframe.chiSquare('VBFShape','VBFdh',2)
    VBFprobChi2 = TMath.Prob(VBFchi2*VBFndof, VBFndof)
    VBFchi2 = round(VBFchi2,2)
    VBFprobChi2 = round(VBFprobChi2,2)

    # VBFShape.paramOn(VBFframe, RooFit.Layout(0.5,0.9,0.9))

    VBFleg = TLegend(0.7,0.7,0.9,0.9)
    VBFleg.SetBorderSize(1)
    VBFleg.SetFillStyle(0)
    VBFleg.AddEntry(VBFframe.FindObject("VBFdh"),"QCD-VBF","P")
    VBFleg.AddEntry(VBFframe.FindObject("VBFShape"),"VBFShape","L")
    VBFleg.AddEntry(VBFframe.FindObject("VVShape"),"VVShape","L")
    # VBFleg.AddEntry(0,'#chi^{2} ='+str(VBFchi2),'')
    # VBFleg.AddEntry(0,'Prob #chi^{2} = '+str(probChi2),'')
    VBFleg.SetTextSize(0.02)
    VBFframe.addObject(VBFleg)
            
    VBFframe.SetMinimum(10**(-3))
    
    VBFframe.Draw()
    VBFcanv.Print('VBFRegion.eps')

    
 
