from array import array
import csv,collections,numpy
import ROOT as rt
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1,TH1F ,TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex,TGraphAsymmErrors

# from ROOT import RooRealVar, RooDataHist, RooPlot, RooGaussian, RooAbsData, RooFit, RooArgList,RooFormulaVar,RooGenericPdf

if(__name__=='__main__'):

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    # gStyle.SetOptTitle(0)

    gStyle.SetTextFont(43)
    
    gStyle.SetTitleOffset(0.86,"X")
    gStyle.SetTitleOffset(1.6,"Y")
    # gStyle.SetPadLeftMargin(0.18)
    gStyle.SetPadLeftMargin(0.1)
    # gStyle.SetPadBottomMargin(0.15)
    gStyle.SetPadBottomMargin(0.12)
    gStyle.SetPadTopMargin(0.08)
    # gStyle.SetPadRightMargin(0.08)
    gStyle.SetPadRightMargin(0.1)
    gStyle.SetMarkerSize(0.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetTitleSize(0.05, "XYZ")
    gStyle.SetLabelSize(0.04, "XYZ")
    gStyle.SetNdivisions(506, "XYZ")
    gStyle.SetLegendBorderSize(0)
    
    # postfix=''
    postfix='_SignalInjection'
    # postfix='_SidebandData'


    # filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_M6_6p00'+postfix+'0_invMass_combined.root'
    # filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_T7_m21p00'+postfix+'0_invMass_combined.root'
    filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_T7_m15p40'+postfix+'0_invMass_combined.root'
    # filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_T0_m1p080_invMass_combined.root'
    # filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_M0_105p000_invMass_combined_1GeV.root'
    # filename='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/plots/fitDiagnosticsZZ_M0_105p000_invMass_combined_1GeV.root'
    File=TFile(filename,'READ')
    pointname=filename.split('/')[-1].split('_')
    canvTitle=pointname[1]+' '+pointname[2]+' '+pointname[3][:-1]
    pointname=pointname[1]+'_'+pointname[2]+'_'+pointname[3][:-1]
    for channel in ['ch1','ch2']:
        if channel=='ch1':
            name='VV'
        if channel=='ch2':
            name='VBF'
        
        signal=File.Get('shapes_fit_s/'+channel+'/total_signal')
        background=File.Get('shapes_fit_s/'+channel+'/total_background')
        data=File.Get('shapes_fit_s/'+channel+'/data')

        # signal.Scale(10)

        # TH1 h; // the histogram (you should set the number of bins, the title etc)
        # auto nPoints = graph.GetN(); // number of points in your TGraph
        # for(int i=0; i < nPoints; ++i) {
        #         double x,y;
        #         graph.GetPoint(i, x, y);
        #         h->Fill(x,y); // ?
        # }
        
        N=0
        datahist=TH1F('data','data',3451,1050,4500)        
        datahist1=TH1F('data1','data1',3450,1050,4500)
        for i in range(0,data.GetN()):
            x=rt.Double(0)
            y=rt.Double(0)
            data.GetPoint(i,x,y)
            datahist.Fill(x,y)
            datahist1.SetBinContent(i,y)
            datahist1.SetBinError(i,data.GetErrorY(i))

        Nbins=200
        binning=range(1050,4500,Nbins+1)
        d_binning=array('d')
        for b in binning:
            d_binning.append(b)
        datahist=datahist.Rebin(len(d_binning)-1,'new binning',d_binning)
        datahist1=datahist1.Rebin(len(d_binning)-1,'new binning',d_binning)

        test=datahist.Clone()
        test.Add(datahist1,-1)
        test.SetLineColor(1)
        test.SetLineWidth(2)
        datahist.SetLineColor(rt.kRed-2)
        datahist.SetLineWidth(2)
        datahist1.SetLineColor(rt.kBlue-2)
        datahist1.SetLineWidth(2)
       
        tcanv=TCanvas('test','test',600,600)
        # tcanv.SetLogy()
        datahist.Draw('H1')
        datahist1.Draw('H1SAME')
        # datahist.Draw('H1SAME')
        # test.Draw('PE1SAME')
        # test.Draw('H1')
        tcanv.Print('test.eps')


        datahist.SetMarkerStyle(8)
        datahist.SetLineColor(1)

        signal.Scale(Nbins)
        background.Scale(Nbins)
        signal.SetFillColor(rt.kRed-2)
        background.SetFillColor(rt.kBlue-2)
        signal.SetLineColor(1)
        background.SetLineColor(1)

    
        canv=TCanvas('Canvas1','Canvas1',600,600)
        canv.SetLogy()
        dummy=TH1F('','',3500,1050,4500)
        dummy.Fill(1500,signal.GetMaximum())
        dummy.Fill(2000,background.GetMaximum())
        dummy.SetLineColor(rt.kWhite)
        dummy.Draw('P')
        dummy.GetXaxis().SetTitle('M_{jj AK8}')
        dummy.GetYaxis().SetTitle('')
        dummy.Draw('PSAME')

        stack=THStack('signal+background','signal+background')
    
    
        stack.Add(background)
        stack.Add(signal)
        stack.Draw('HISTSAME')
        datahist.Draw('PE1SAME')

        gPad.RedrawAxis()
        legend = TLegend(0.5,0.7,0.8,0.92)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)
        legend.SetMargin(0.4)
        # legend.SetNColumns(2)
        # legend.SetColumnSeparation(0.3)
        legend.AddEntry(signal,'Signal','f')
        legend.AddEntry(background,'Background','f')
        legend.AddEntry(datahist,'PseudoData','lep')
        legend.Draw('SAME')

        latex=TLatex()
        latex.SetNDC(kTRUE)
        latex.SetTextSize(24)
        if('VV' in name):
            latextitle='!VBF'
        else:
            latextitle='VBF'
        latex.DrawLatex(0.45,0.953,latextitle)
        # latex.DrawLatex(0.35,0.953,canvTitle)


        canv.Print('combinedFitPlot_'+name+pointname+'.eps')
        del dummy,canv,datahist,datahist1,tcanv
    
