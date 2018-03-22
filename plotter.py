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
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)


def plotter(dir,plot,xTitle,logY,channels=['VV']):

    #signal channel to superimpose
    channelTex={'WPWP':'W^{+}W^{+}','WPWM':'W^{+}W^{-}','WMWM':'W^{-}W^{-}','WPZ':'W^{+}Z','WMZ':'W^{-}Z','ZZ':'ZZ'}
    plotstyle=[(1,1),(1,2),(2,1),(2,2),(4,1),(4,2)]

    cutnames=['cleaner','AK8N2sel','invMAk8sel','detaAk8sel','softdropAK8sel','tau21sel','AK4cleaner','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']

    cuts={'cleaner':'p_{T-AK8} > 200 GeV, |#eta_{AK8}| < 2.5',
          'AK8N2sel':'N_{AK8} #geq 2',
          'invMAk8sel':'M_{jj-AK8} > 1050 GeV',
          'detaAk8sel':'|#Delta#eta_{jj-AK8}|<1.3',
          'softdropAK8sel':'65 GeV <M_{SD}< 105 GeV',
          'tau21sel':'0 #leq #tau_{2}/#tau_{1}<0.45',
          'AK4cleaner':'p_{T-AK4} > 30 GeV, |#eta_{AK4}| < 5.0',
          'AK4N2sel':'N_{AK4} #geq 2',
          'OpSignsel':'#eta_{1-AK4} #eta_{2-AK4} < 0',
          'detaAk4sel':'|#Delta#eta_{jj-AK4}| > 3.0',
          'invMAk4sel_1p0':'M_{jj-AK4} > 1.0 TeV'}
    # logY=True
    VV=('VV' in channels)
    seperate=(not VV)
    if VV:
        channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]

    #cut
    # dir='AK8_cleaner'
    
    # xTitle='M_{j-AK8} [GeV/c^{2}]'

    plottitle=''

    scaleVV=True
    VVScale=10**2

    YRangeUser=False
    Ymin=10**2
    Ymax=10**5

    XRangeUser=False
    Xmin=0
    Xmax=13000

    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    SFiles=[]
    
    for i in range(len(channels)):
        SFiles.append(TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/parameterscan/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root"%channels[i]))

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
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)
    
    drawOptions="HE"

    if(logY):
        canv.SetLogy()

    stack=THStack(plottitle,plottitle)
    
    BHist.SetFillColor(867)
    BHist.SetLineColor(867)
    
    BHist.SetTitle(plottitle)

    if(YRangeUser):
        BHist.GetYaxis().SetRangeUser(Ymin,Ymax)
    if(XRangeUser):
        BHist.GetXaxis().SetRangeUser(Xmin,Xmax)

    legend.AddEntry(BHist,"QCD","f")

    stack=THStack('stack',plottitle)
    stack.Add(BHist)

    for i in range(len(channels)):
        if VV:
            if(i==0):
                VVsum=SHists[i].Clone()
            else:
                VVsum.Add(SHists[i])
        else:
            # if seperate:
            SHists[i].SetLineColor(plotstyle[i][0])
            SHists[i].SetLineStyle(plotstyle[i][1])
            stack.Add(SHists[i])
            legend.AddEntry(SHists[i],"%sjj"%channelTex[channels[i]])
            

    if VV:
        legentry='VVjj'
        if(scaleVV):
            VVsum.Scale(VVScale)
            legentry+=' *%0.f'%VVScale
        VVsum.SetLineColor(1)
        VVsum.SetLineStyle(plotstyle[0][1])
        stack.Add(VVsum)
        legend.AddEntry(VVsum,legentry)

    canv.SetTitle(plottitle)
    # canv.SetLeftMargin(0.12) 

    stack.Draw('nostack'+drawOptions)
    stack.GetXaxis().SetTitle(xTitle)
    stack.GetYaxis().SetTitle('Events')
    stack.GetYaxis().SetTitleOffset(1.5)
    stack.Draw('nostack'+drawOptions)
    
    legend.Draw()        
    
    latex=TLatex()
    latex.SetNDC(kTRUE);
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.24,0.87,"private work")

    lastcut='nocuts'
    for cut in cutnames:
        # print cut, dir
        if cut in dir:
            lastcut=cut
    
    if(not (lastcut=='nocuts')):
        latex.SetTextSize(0.03)
        for l in range(cutnames.index(lastcut)+1):
            latex.DrawLatex(0.24,0.8-l*0.04,cuts[cutnames[l]])

    canv.Update()
    canv.Print('%s_%s.eps'%(dir,plot))

if(__name__=='__main__'):
    dir='AK8_invMAk4sel_1p0'

    #plot
    plot='mass'
    plotter(dir, plot)
