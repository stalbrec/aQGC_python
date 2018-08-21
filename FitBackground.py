from array import array
import csv,collections,numpy
import ROOT as rt
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TH1F, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex,TMath
from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooFormulaVar,RooGenericPdf

def FitRegion(REGION='SignalRegion'):
    gROOT.SetBatch(True)
    # cavn0=TCanvas('test','test',600,600)
    # SD_REGION='Signal'
    # REGION='SignalRegion'
    # REGION='SidebandRegion'
    #filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/input/ZZ_S0_16p00.root'
    # filename='/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/backup/uhh2.AnalysisModuleRunner.Data.DATA.root'

    if('Signal' in REGION):
        filename='/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/uhh2.AnalysisModuleRunner.MC.MC_QCD.root'
    else:
        filename='/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/uhh2.AnalysisModuleRunner.Data.DATA.root'
        # filename='/nfs/dust/cms/user/albrechs/UHH2_Output/'+REGION+'/uhh2.AnalysisModuleRunner.MC.MC_QCD.root'

    File=TFile(filename)
    
    # VVHist_1GeV= File.Get('qcd_invMass')
    # VBFHist_1GeV= File.Get('qcd_invMass_afterVBFsel')
    VVHist_1GeV= File.Get('VVRegion/M_jj_AK8_highbin')
    VBFHist_1GeV= File.Get('invMAk4sel_1p0/M_jj_AK8_highbin')

    # VVHist_1GeV.Draw('PE1')
    # raw_input('press enter to continue')

    VVHist_1GeV.Scale(1./VVHist_1GeV.Integral(),'width')
    VBFHist_1GeV.Scale(1./VBFHist_1GeV.Integral(),'width')

    # VVHist_1GeV.Draw('PE1')
    # raw_input('press enter to continue')
    equidistant=False
    
    fitbinning=array('d')
    if(equidistant):
        binwidth=400
        yTitle='Normalized # Events / (%.1f GeV)'%binwidth
        #NBins=(14000/binwidth) - ( (1040/binwidth) + 1 )
        NBins=(14000/binwidth) - ( (1040/binwidth)+1 )
        NBins=int(NBins)
        for i in range(NBins+1):
            fitbinning.append(1050+i*binwidth)
        # # print(fitbinning)
    else:
        yTitle='Normalized # Events'

        #not plotting bin before Mjj>1050GeV Cut
        nonequidistant_binning=[1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
        # nonequidistant_binning=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
        NBins=len(nonequidistant_binning)-1
        for b in nonequidistant_binning:
            fitbinning.append(b)

    VVHist_100GeV=VVHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)
    VBFHist_100GeV=VBFHist_1GeV.Rebin(NBins,"fit parameter",fitbinning)
    # VVHist_100GeV.Scale(1./VVHist_100GeV.Integral(),'width')
    # VBFHist_100GeV.Scale(1./VBFHist_100GeV.Integral(),'width')

    # VVHist_100GeV.Draw('PE1')
    # raw_input('press enter to continue')

    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0000)    
    # gStyle.SetOptFit(1100)    
    gStyle.SetOptTitle(0)
    RooFit.SumW2Error(kTRUE)


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

    # fitOptions='R'
    # fitOptions='R'
    fitOptions='RSWLM'
    twopar='[0]/TMath::Power(x/13000,[1])'
    threeparlog='[0]/TMath::Power(x/13000,[1])+([2]*TMath::Log10(x/13000))'
    threepar='[0]*TMath::Power((1-(x/13000)),[2])/TMath::Power(x/13000,[1])'
    # threepar='[0]*TMath::Power((1-x)/13000,[1])+(x/13000)*[2]'
    fourpar='[0]*TMath::Power((1-(x/13000),[1])/TMath::Power(x/13000,[2]+[3]*TMath::Log10(x/13000))'
    if('Signal' in REGION): 
        NPar=2
    else:
        NPar=3
    if(NPar==2):
        fitfunc=twopar
        functionTeX='p_{0}/(x/#sqrt{s})^{p_{1}}'
    elif(NPar==3):
        # functionTeX='#frac{p_{0}}{(x/#sqrt{s})^{p_{1}}}+p_{2}*log_{10}(x/#sqrt{s})'
        # fitfunc=threeparlog
        functionTeX='#frac{p_{0}*((1-(x/#sqrt{s}))^{p_{2}}}{(x/#sqrt{s})^{p_{1}}}'
        fitfunc=threepar
    elif(NPar==4):
        fitfunc=fourpar
        functionTeX='#frac{p_{0}*((1-x)/#sqrt{s})^{p_{1}}}{(x/#sqrt{s})^{p_{2}+p_{3}*log_{10}(x/#sqrt{s})}}'
   
    # for i in range(VVHist_100GeV.GetNbinsX()):
    #     print i,':',VVHist_100GeV.GetBinCenter(i),'-',VVHist_100GeV.GetBinContent(i)
    # VVHist_100GeV.SetBinContent(19,0)
    # VVHist_100GeV.SetBinError(19,0)
        
    VVTF1=TF1('VVTF1',fitfunc,1058,VV_MAXIMUM)
    # VVTF1.SetParLimits(0,-10**(-6),10**(-6))
    # VVTF1.SetParLimits(1,0,8)
    # VVTF1.SetParLimits(2,-100,0)
    # VVTF1.SetParameter(0,1.70473**(-7))
    VVTF1.SetParameter(0,1.70473*10**(-7))
    VVTF1.SetParameter(1,5.76351)
    # VVTF1.SetParameter(2,0)
  
    VVHist_100GeV.SetMarkerStyle(8)
    VVHist_100GeV.SetLineColor(1)
    VVHist_100GeV.GetYaxis().SetRangeUser(10**(-6),10)
    VVHist_100GeV.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    VVHist_100GeV.GetYaxis().SetTitle(yTitle)
    VVHist_100GeV.GetYaxis().SetTitleOffset(2)

    VVHist_100GeV.Draw('PE1')   
    VVHist_100GeV.GetXaxis().SetRangeUser(1058,VV_MAXIMUM+1000)
    VVHist_100GeV.Draw('PE1SAME')   
    #raw_input('press enter to continue')
    VVHist_100GeV.Sumw2()
    VVHist_100GeV.Fit('VVTF1',fitOptions)
    # VVHist_100GeV.Fit('VVTF1','R')
    VVTF1.Draw('SAME')
    # VVTF1UP=TF1('VVTF1UP',fitfunc,1050,VV_MAXIMUM)
    # VVTF1UP.SetParameter(0,VVTF1.GetParameter(0)+VVTF1.GetParError(0))
    # VVTF1UP.SetParameter(1,VVTF1.GetParameter(1)+VVTF1.GetParError(1))
    # VVTF1UP.SetLineStyle(rt.kDashed)
    
    # VVTF1DOWN=TF1('VVTF1DOWN',fitfunc,1050,VV_MAXIMUM)
    # VVTF1DOWN.SetParameter(0,VVTF1.GetParameter(0)-VVTF1.GetParError(0))
    # VVTF1DOWN.SetParameter(1,VVTF1.GetParameter(1)-VVTF1.GetParError(1))
    # VVTF1DOWN.SetLineStyle(rt.kDashed)

    # VVTF1UP.Draw('SAME')
    # VVTF1DOWN.Draw('SAME')
    
    print('chi2/ndf:',VVTF1.GetChisquare(),'/',VVTF1.GetNDF())

    latex=TLatex()
    latex.SetNDC(kTRUE)
    latex.SetTextSize(0.03)
    # latex.DrawLatex(0.52,0.953,"%.2f fb^{-1} (13 TeV)"%36.1)
    latex.DrawLatex(0.45,0.65,"#chi^{2}/ndof=%.2f/%.2f=%.2f"%(VVTF1.GetChisquare(),VVTF1.GetNDF(),VVTF1.GetChisquare()/VVTF1.GetNDF()))
    latex.Draw("SAME")
    
    VVleg = TLegend(0.45,0.7,0.9,0.9)
    VVleg.SetBorderSize(0)
    VVleg.SetFillStyle(0)
    if('Data' in filename): 
        VVleg.AddEntry(VVHist_100GeV,'Data-!VBF','p')
        VVleg.AddEntry(VVTF1,'Data-!VBF Fit %s'%functionTeX,'l')
    else:
        VVleg.AddEntry(VVHist_100GeV,'QCD-!VBF','p')
        VVleg.AddEntry(VVTF1,'QCD-!VBF Fit %s'%functionTeX,'l')
    VVleg.SetTextSize(0.03)
    VVleg.Draw('SAME')
   
    VVcanv.Print(REGION+'_VVRegion.eps')

    VBFcanv=TCanvas('VBF','VBF',700,700)
    VBFcanv.SetLogy()
    VBFcanv.SetLeftMargin(0.20) 
    VBFcanv.cd()

    VBFTF1=TF1('VBFTF1',fitfunc,1058,VBF_MAXIMUM)

    if(NPar>2):
        VBFTF1.SetParameter(0,2.85852*10**(-8))
        VBFTF1.SetParameter(1,6.49129)
        VBFTF1.SetParameter(2,-1)
        
    VBFTF1.SetLineColor(rt.kBlue)
    VBFTF1.SetLineWidth(2)
    # VBFTF1.SetLineStyle(2)
    VBFHist_100GeV.SetMarkerStyle(8)
    VBFHist_100GeV.SetLineColor(1)
    VBFHist_100GeV.GetYaxis().SetRangeUser(10**(-6),10)
    VBFHist_100GeV.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
    VBFHist_100GeV.GetYaxis().SetTitle(yTitle)
    VBFHist_100GeV.GetYaxis().SetTitleOffset(2)
    VBFHist_100GeV.Draw('PE1')
    VBFHist_100GeV.GetXaxis().SetRangeUser(1058,VV_MAXIMUM+1000)
    VBFHist_100GeV.Draw('PE1SAME')
    # raw_input('press enter to continue')
    # VBFHist_100GeV.Sumw2()
    VBFHist_100GeV.Fit('VBFTF1',fitOptions)
    VBFTF1.Draw('SAME')
    # VVTF1.SetLineStyle(2)
    VVTF1.Draw('SAME')

    # VVTF1UP.Draw('SAME')
    # VVTF1DOWN.Draw('SAME')

    # VBFTF1UP=TF1('VBFTF1UP',fitfunc,1050,VBF_MAXIMUM)
    # VBFTF1UP.SetParameter(0,VBFTF1.GetParameter(0)+VBFTF1.GetParError(0))
    # VBFTF1UP.SetParameter(1,VBFTF1.GetParameter(1)+VBFTF1.GetParError(1))
    # VBFTF1UP.SetLineColor(rt.kBlue)
    # VBFTF1UP.SetLineStyle(rt.kDashed)
    
    # VBFTF1DOWN=TF1('VBFTF1DOWN',fitfunc,1050,VBF_MAXIMUM)
    # VBFTF1DOWN.SetParameter(0,VBFTF1.GetParameter(0)-VBFTF1.GetParError(0))
    # VBFTF1DOWN.SetParameter(1,VBFTF1.GetParameter(1)-VBFTF1.GetParError(1))
    # VBFTF1DOWN.SetLineColor(rt.kBlue)
    # VBFTF1DOWN.SetLineStyle(rt.kDashed)

    # VBFTF1UP.Draw('SAME')
    # VBFTF1DOWN.Draw('SAME')

    print('chi2/ndf:',VBFTF1.GetChisquare(),'/',VBFTF1.GetNDF())

    latexvbf=TLatex()
    latexvbf.SetNDC(kTRUE)
    latexvbf.SetTextSize(0.03)
    latexvbf.DrawLatex(0.45,0.65,"#chi^{2}/ndof=%.2f/%.2f=%.2f"%(VBFTF1.GetChisquare(),VBFTF1.GetNDF(),VBFTF1.GetChisquare()/VBFTF1.GetNDF()))

    
    VBFleg = TLegend(0.45,0.7,0.9,0.9)
    VBFleg.SetBorderSize(0)
    VBFleg.SetFillStyle(0)
    if('Data' in filename): 
        VBFleg.AddEntry(VBFHist_100GeV,'Data-VBF','p')
        VBFleg.AddEntry(VBFTF1,'Data-VBF Fit %s'%functionTeX,'l')
        VBFleg.AddEntry(TH1F(),'','')
        VBFleg.AddEntry(VVTF1,'Data-!VBF Fit %s'%functionTeX,'l')
    else:
        VBFleg.AddEntry(VBFHist_100GeV,'QCD-VBF','p')
        VBFleg.AddEntry(VBFTF1,'QCD-VBF Fit %s'%functionTeX,'l')
        if(NPar==3):
            VBFleg.AddEntry(TH1F(),'','')
        VBFleg.AddEntry(VVTF1,'QCD-!VBF Fit %s'%functionTeX,'l')
    VBFleg.SetTextSize(0.03)
    VBFleg.Draw('SAME')

    VBFcanv.Print(REGION+'_VBFRegion.eps')

 
if(__name__=='__main__'):
    # regions=['SignalRegion','SidebandRegion']
    regions=['SidebandRegion']
    for region in regions:
        FitRegion(region)
