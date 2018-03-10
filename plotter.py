from array import array
import sys,csv,collections,numpy
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex
gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTitleOffset(1.4,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.08)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

if(__name__=='__main__'):
    #signal channel to superimpose
    channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    channelTex=['W^{+}W^{+}','W^{+}W^{-}','W^{-}W^{-}','W^{+}Z','W^{-}Z','ZZ']
    plotstyle=[(1,1),(1,2),(2,1),(2,2),(4,1),(4,2)]

    logY=True

    #cut
    dir='AK8_cleaner'

    #plot
    plot='mass'
    xTitle='M_{j-AK8} [GeV/c^{2}]'

    plottitle=''


    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    SFiles=[]
    
    for i in range(len(channels)):
        SFiles.append(TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic_parameterscan.root"%channels[i]))

    ##Open File to get BackgroundHist:
    BFile = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/parameterscan/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")


    gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")

    SHists=[]
    for i in range(len(channels)):            
        SHists.append(SFiles[i].Get(dir+'/'+plot))
    BHist=BFile.Get(dir+'/'+plot)

    canv = TCanvas(plottitle,plottitle,600,600)
        
    #turning off the standard Statistic-Box

    legend = TLegend(0.7,0.7,0.9,0.9)
        
    drawOptions="HE"
    if(logY):
        canv.SetLogy()
            
    stack=THStack(plottitle,plottitle)
    
    BHist.SetFillColor(867)
    BHist.SetLineColor(867)
    
    BHist.SetTitle(plottitle)
    BHist.GetXaxis().SetRangeUser(0,7500)

    legend.AddEntry(BHist,"QCD","f")

    stack=THStack('stack',plottitle)
    stack.Add(BHist)

    for i in range(len(channels)):
        SHists[i].SetLineColor(plotstyle[i][0])
        SHists[i].SetLineStyle(plotstyle[i][1])
        stack.Add(SHists[i])
        legend.AddEntry(SHists[i],"%sjj"%channelTex[i])

    canv.SetTitle(plottitle)
    stack.Draw('nostack'+drawOptions)
    stack.GetXaxis().SetRangeUser(0,9000)
    stack.GetXaxis().SetTitle(xTitle)
    stack.GetYaxis().SetTitle('Events')
    

    # canv.SetLeftMargin(0.12) 
    stack.GetYaxis().SetTitleOffset(1.5)

    stack.Draw('nostack'+drawOptions)
        
    legend.Draw()        

    
    latex=TLatex()
    latex.SetNDC(kTRUE);
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.24,0.87,"private work")


    canv.Update()
    canv.Print('%s_%s.eps'%(dir,plot))

