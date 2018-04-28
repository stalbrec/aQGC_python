from array import array
import sys,csv,collections,numpy,math
from ROOT import gROOT, gStyle, gPad,TCanvas, TColor, TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex,TPad,TLine
import ROOT as rt

def magnitude(x):
    return int(math.floor(math.log10(x)))

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

gStyle.SetTitleOffset(0.86,"X")
gStyle.SetTitleOffset(1.6,"Y")
# gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadLeftMargin(0.1)
# gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadTopMargin(0.08)
# gStyle.SetPadRightMargin(0.08)
gStyle.SetPadRightMargin(0.2)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetTitleSize(0.05, "XYZ")
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)


def plotter(dir,plot,xTitle,logY,channels=['VV'],includeData=False,scaleSignal=0):

    #signal channel to superimpose
    channelTex={'WPWP':'W^{+}W^{+}','WPWM':'W^{+}W^{-}','WMWM':'W^{-}W^{-}','WPZ':'W^{+}Z','WMZ':'W^{-}Z','ZZ':'ZZ'}
    plotstyle=[(1,1),(1,2),(2,1),(2,2),(4,1),(4,2)]

    cutnames=['cleaner','AK8N2sel','invMAk8sel','detaAk8sel','softdropAK8sel','tau21sel','AK4cleaner','AK4N2sel','OpSignsel','detaAk4sel','invMAk4sel_1p0']

    cuts={'cleaner':'#splitline{p_{T-AK8} > 200 GeV, |#eta_{AK8}| < 2.5}{p_{T-AK4} > 30 GeV, |#eta_{AK4}| < 5.0}',
          'AK8N2sel':'N_{AK8} #geq 2',
          'invMAk8sel':'M_{jj-AK8} > 1050 GeV',
          'detaAk8sel':'|#Delta#eta_{jj-AK8}|<1.3',
          'softdropAK8sel':'65 GeV <M_{SD}< 105 GeV',
          'tau21sel':'0 #leq #tau_{2}/#tau_{1}<0.45',
          # 'AK4cleaner':'p_{T-AK4} > 30 GeV, |#eta_{AK4}| < 5.0',
          'AK4cleaner':'',
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

    lumi=36.814
    
    region='SignalRegion'
    
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/%s/'%region
    
    scaleVV=scaleSignal!=0
    VVScale=scaleSignal
    
    # scaleVV=False
    # VVScale=10**2

    YRangeUser=False
    Ymin=10**1
    Ymax=10**4

    XRangeUser=False
    Xmin=0
    Xmax=13000


    
    
    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    SFiles=[]
    
    for i in range(len(channels)):
        SFiles.append(TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_aQGC_%sjj_hadronic.root"%channels[i]))

    ##Open Files to get BackgroundHist:
    QCDFile = TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")
    WJetsFile = TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_WJetsToQQ_HT600ToInf.root")
    ZJetsFile = TFile(path+"/uhh2.AnalysisModuleRunner.MC.MC_ZJetsToQQ_HT600ToInf.root")    

    #Open File to get DataHist:
    DataFile = TFile(path+"/uhh2.AnalysisModuleRunner.Data.DATA.root")

    gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")

    SHists=[]
    for i in range(len(channels)):            
        SHists.append(SFiles[i].Get(dir+'/'+plot))
    QCDHist=QCDFile.Get(dir+'/'+plot)
    WJetsHist=WJetsFile.Get(dir+'/'+plot)
    ZJetsHist=ZJetsFile.Get(dir+'/'+plot)

    if(includeData):
        DataHist=DataFile.Get(dir+'/'+plot)
        
    canv = TCanvas(plottitle,plottitle,600,600)

    yplot=0.6
    yratio=0.4
    ymax=1.0
    xmax=1.0
    xmin=0.0
    plotpad=TPad("plotpad","Plot",xmin,ymax-yplot,xmax,ymax)
    ratiopad=TPad("ratiopad","Ratio",xmin,ymax-yplot-yratio,xmax,ymax-yplot)

    plotpad.SetTopMargin(0.08)
    plotpad.SetBottomMargin(0.0)
    plotpad.SetLeftMargin(0.2)
    plotpad.SetRightMargin(0.2)
    plotpad.SetTicks()
    
    ratiopad.SetTopMargin(0.0)
    ratiopad.SetBottomMargin(0.25)
    ratiopad.SetLeftMargin(0.2)
    ratiopad.SetRightMargin(0.2)
    ratiopad.SetTicks()
    # ratiopad.SetGridx()

    
    plotpad.Draw()
    ratiopad.Draw()
    
    
    if(logY):
        plotpad.SetLogy()
        canv.SetLogy()

    
    #turning off the standard Statistic-Box

    legend = TLegend(0.8,0.6,1,0.9)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.02)
    legend.SetMargin(0.4)

    
    drawOptions="HE"
    # drawOptions=""

    stack=THStack(plottitle,plottitle)

    BHist=THStack(plottitle,plottitle)


    QCDColor=rt.kAzure+7
    WJetsColor=rt.kRed-4
    ZJetsColor=rt.kOrange-2

    QCDHist.SetFillColor(QCDColor)
    WJetsHist.SetFillColor(WJetsColor)
    ZJetsHist.SetFillColor(ZJetsColor)
    # QCDHist.SetLineColor(854)
    # WJetsHist.SetLineColor(629)
    # ZJetsHist.SetLineColor(799)

    QCDHist.SetLineColor(QCDColor)
    WJetsHist.SetLineColor(WJetsColor)
    ZJetsHist.SetLineColor(ZJetsColor)

    BHist.Add(ZJetsHist,"HIST")
    BHist.Add(WJetsHist,"HIST")
    BHist.Add(QCDHist,"HIST")

    legend.AddEntry(ZJetsHist,"Z+JetsToQQ","f")
    legend.AddEntry(WJetsHist,"W+JetsToQQ","f")
    legend.AddEntry(QCDHist,"QCD","f")
    
    if(YRangeUser):
        BHist.GetYaxis().SetRangeUser(Ymin,Ymax)
    if(XRangeUser):
        BHist.GetXaxis().SetRangeUser(Xmin,Xmax)

    BHist.SetTitle(plottitle)
    BHistErr=QCDHist.Clone()
    BHistErr.Add(WJetsHist)
    BHistErr.Add(ZJetsHist)
    
    BHistErr.SetFillStyle(3204)
    
    BHistErr.SetFillColor(rt.kGray+2)
    BHistErr.SetLineColor(1)
    legend.AddEntry(BHistErr,"stat. Uncertainty","f")
    
    if(includeData):
        DataHist.SetMarkerStyle(8)
        DataHist.SetLineColor(1)    
        
        DataHist.SetTitle(plottitle)
        legend.AddEntry(DataHist,"Data","lep")




    
    for i in range(len(channels)):
        if VV:
            if(i==0):
                VVsum=SHists[i].Clone()
            else:
                VVsum.Add(SHists[i])
        else:
            SHists[i].SetLineColor(plotstyle[i][0])
            SHists[i].SetLineStyle(plotstyle[i][1])
            legend.AddEntry(SHists[i],"%sjj"%channelTex[channels[i]])
            

    if VV:
        legentry='VVjj'
        if(scaleVV):
            VVsum.Scale(VVScale)
            legentry+=' *%0.f'%VVScale
        VVsum.SetLineColor(1)
        VVsum.SetLineStyle(plotstyle[0][1])
        legend.AddEntry(VVsum,legentry)

    canv.SetTitle(plottitle)


    BGMax=BHist.GetMaximum()
    SIGMax=0
    if(VV):
        SIGMax=VVsum.GetMaximum()
    else:
        for i in range(len(channels)):
            tmpmax=SHists[i].GetMaximum()
            if(tmpmax>SIGMax):
                SIGMax=tmpmax
    if(logY):
        MAX=float(10**(magnitude(max(BGMax,SIGMax))+1))
        MIN=float(10**(magnitude(max(BGMax,SIGMax))-4))
    else:
        MAX=1.1*max(BGMax,SIGMax)
        MIN=0.

    # if(BGMax>SIGMax):
    # BHist.Draw("Hist")
    # BHistErr.GetXaxis().SetTitle(xTitle)
    BHistErr.GetYaxis().SetTitle('Events')
    BHistErr.GetYaxis().SetRangeUser(MIN,MAX)
    BHistErr.GetYaxis().SetTitleSize(0.08)
    BHistErr.GetYaxis().SetLabelSize(0.06)
    BHistErr.GetXaxis().SetTitleSize(0.0)
    BHistErr.GetXaxis().SetLabelSize(0.0)

    
    plotpad.cd()
    BHistErr.GetXaxis().SetLabelSize(0.0)

    BHistErr.Draw("E2")

    BHist.Draw("HistSAME")
    if(VV):
        VVsum.Draw("SAME"+drawOptions)
    else:
        for i in range(len(channels)):
            SHists[i].Draw("SAME")

    if(includeData):
        DataHist.Draw("APE1SAME")


    ratiopad.cd()
    
    ratioHist=DataHist.Clone()
    ratioHist.SetLineColor(rt.kBlack)
    ratioHist.Sumw2()
    ratioHist.SetStats(0)
    ratioHist.Divide(BHistErr)
    ratioHist.SetMarkerStyle(21)
    ratioHist.GetYaxis().SetRangeUser(0.35,2.-0.35)
    ratioHist.GetYaxis().SetTitle("Data/MC")
    ratioHist.GetYaxis().SetTitleSize(0.11)
    ratioHist.GetYaxis().SetLabelSize(0.11)
    ratioHist.GetYaxis().SetNdivisions(506)
    ratioHist.GetXaxis().SetTitle(xTitle)
    ratioHist.GetXaxis().SetTitleSize(0.11)
    ratioHist.GetXaxis().SetLabelSize(0.11)
    # ratioHist.GetXaxis().SetNdivisions(506)
    
    ratioHist.Draw("ep")


    zeropercent=TLine(ratioHist.GetXaxis().GetXmin(),1,ratioHist.GetXaxis().GetXmax(),1)
    zeropercent.Draw()
    plus10percent=TLine(ratioHist.GetXaxis().GetXmin(),1.1,ratioHist.GetXaxis().GetXmax(),1.1)
    plus10percent.SetLineStyle(rt.kDashed)
    plus10percent.Draw()
    minus10percent=TLine(ratioHist.GetXaxis().GetXmin(),0.9,ratioHist.GetXaxis().GetXmax(),0.9)
    minus10percent.SetLineStyle(rt.kDashed)
    minus10percent.Draw()
    
    canv.cd()
    gPad.RedrawAxis()
    legend.Draw()        
    
    latex=TLatex()
    
    latex.SetNDC(kTRUE)
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.6,0.93,"%.2f fb^{-1} (13 TeV)"%lumi)
    latex.DrawLatex(0.18,0.87,"private work")
    
    lastcut='nocuts'
    for cut in cutnames:
        # print cut, dir
        if cut in dir:
            lastcut=cut
    
    # if(not (lastcut=='nocuts')):
    #     latex.SetTextSize(0.03)
    #     for l in range(cutnames.index(lastcut)+1):
    #         latex.DrawLatex(0.5,0.8-l*0.04,cuts[cutnames[l]])

    canv.Update()
    # canv.Print('Plots/%s_%s.png'%(dir,plot))
    canv.Print('Plots/%s_%s.eps'%(dir,plot))
    # canv.Print('%s_%s.eps'%(dir,plot))

if(__name__=='__main__'):
    dir='AK8_invMAk4sel_1p0'

    plot='mass'
    plotter(dir, plot)
