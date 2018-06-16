from array import array
import os, sys, csv, collections, numpy, math
from ROOT import gROOT, gSystem, gStyle, gPad, TCanvas, TColor, TH1F,TF1, TFile, TLegend, THStack, TGraph, TMath, kTRUE, kFALSE,TLatex, TPad, TLine
import ROOT as rt

def magnitude(x):
    return int(math.floor(math.log10(x)))

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)

# gStyle.SetTextFont(43)
gStyle.SetTitleOffset(0.86,"X")
gStyle.SetTitleOffset(1.2,"Y")
# gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadLeftMargin(0.11)
# gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.05)
# gStyle.SetPadRightMargin(0.08)
gStyle.SetPadRightMargin(0.1)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(2)
gStyle.SetTitleSize(0.04, "XYZ")
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)


def cutflow(Region='SignalRegion',removeEvents=False,logY=True,normalise=True,singlePlots=False,drawOptions='HIST', weightedORraw ='weighted'):
    # removeEvents=True
    PreSelectionName='PreSelection'
    # Region='HIGHSidebandRegion'
    PlotBGStack=False
    StackBG=False
    # singlePlots=False
    # normalise=True
    # logY=True
    # drawOptions='HIST TEXT90'
    
    channel='ZZ'
    
    channelTex={'WPWP':'W^{+}W^{+}','WPWM':'W^{+}W^{-}','WMWM':'W^{-}W^{-}','WPZ':'W^{+}Z','WMZ':'W^{-}Z','ZZ':'ZZ'}
    plotstyle=[(1,1),(1,2),(2,1),(2,2),(4,1),(4,2)]
    
    PreSelectionCuts=[
      ('nocuts','All'),
      ('common','CommonModules'),
      # ('corrections','JetCorrections'),
      # ('cleaner','JetCleaner'),
      ('AK4pfidfilter','AK4 PFID-Filter'),
      ('AK8pfidfilter','AK8 PFID-Filter'),
      ('AK8N2sel','N_{AK8} #geq 2'),
      ('invMAk8sel','M_{jj-AK8} > 1050 GeV'),
      ('detaAk8sel','|#Delta#eta_{jj-AK8}|<1.3')
    ]

    SelectionCuts=[#('preselection','PreSelection-check'),
      ('softdropAK8sel','65 GeV <M_{SD}< 105 GeV'),
      ('tau21sel','0 #leq #tau_{2}/#tau_{1}<0.35'),
      ('deltaR48','#Delta R(AK4,leading AK8) > 1.3'),
      # ('VVRegion','VVRegion'),
      ('AK4N2sel','N_{AK4} #geq 2'),
      ('OpSignsel','#eta_{1-AK4} #eta_{2-AK4} < 0'),
      ('detaAk4sel','|#Delta#eta_{jj-AK4}| > 3.0'),
      ('invMAk4sel_1p0','M_{jj-AK4} > 1.0 TeV')]

    Cuts=PreSelectionCuts+SelectionCuts
    # Cuts=SelectionCuts
    
    QCDColor=rt.kAzure+7
    WJetsColor=rt.kRed-4
    ZJetsColor=rt.kOrange-2
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/'
    
    datasets=[#(filename, Name for Legend, Linestyle, Color)
        ('MC.MC_aQGC_%sjj_hadronic.root'%channel,channelTex[channel],1,28)#,
        # ('MC.MC_QCD.root','QCD',1,QCDColor),
        # ('MC.MC_WJetsToQQ_HT600ToInf.root','W+JetsToQQ',1,WJetsColor),
        # ('MC.MC_ZJetsToQQ_HT600ToInf.root','Z+JetsToQQ',1,ZJetsColor),
        # ('Data.DATA.root','Data',1,1)
    ]    

    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")
    PreSelectionFiles=[]
    SelectionFiles=[]


    if removeEvents:
        PreSelectionName=PreSelectionName+'RmEvent'
        Region=Region+'RmEvent'
        
    for dataset in datasets:
        PreSelectionFiles.append(TFile(path+PreSelectionName+"/uhh2.AnalysisModuleRunner.%s"%dataset[0]))
        # SelectionFiles.append(TFile(path+Region+'/backup/'+"/uhh2.AnalysisModuleRunner.%s"%dataset[0]))
        SelectionFiles.append(TFile(path+Region+"/uhh2.AnalysisModuleRunner.%s"%dataset[0]))
    gROOT.ProcessLine( "gErrorIgnoreLevel = 0;")


    yTitle='NEvents_%s'%weightedORraw
    if(normalise):
        yTitle=yTitle+'/N_%s'%Cuts[0][1]

        
    canv = TCanvas('cutflow_canvas','cutflow_canvas',1000,500)
    if(not singlePlots):
        legend = TLegend(0.7,0.7,0.9,0.95)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.02)
        legend.SetMargin(0.4)
    
    NCuts=len(Cuts)
    # NMETFilter=0
    # if 'common' in Cuts[:][0]:        
    #     NMETFilter=PreSelectionFiles[0].Get('cf_metfilters').GetNbinsX()
    #     for i in range(1,PreSelectionFiles[0].Get('cf_metfilters').GetNbinsX()):
    #         Cuts.insert(Cuts.index(('common','CommonModules')),(PreSelectionFiles[0].Get('cf_metfilters').GetXaxis().GetBinLabel(i),PreSelectionFiles[0].Get('cf_metfilters').GetXaxis().GetBinLabel(i)))
    #     NCuts=NCuts+NMETFilter
    print('Plotting Cutflow of',NCuts,'Cuts.')
    # for dataset in datasets:
    BGStack=THStack('MCBackground','MCBackground')

    TotalMinimum=10**10
    NBG=0
    for l in range(len(datasets)):
        print('checking', datasets[l][1])
        if normalise:
            if((len(Cuts)==len(PreSelectionCuts)) or (len(Cuts)==(len(PreSelectionCuts)+len(SelectionCuts))) ):
                Norm=PreSelectionFiles[l].Get(Cuts[0][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
            else:
                Norm=SelectionFiles[l].Get(Cuts[0][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
        else:
            Norm=1
        if(len(Cuts)>len(PreSelectionCuts)):
            CurrentMinimum=SelectionFiles[l].Get(SelectionCuts[-1][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)/Norm
        else:
            CurrentMinimum=PreSelectionFiles[l].Get(PreSelectionCuts[-1][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)/Norm
        print(CurrentMinimum,TotalMinimum)

        if(CurrentMinimum<TotalMinimum):
            print('setting ' , datasets[l][1], 'as new minimum')
            TotalMinimum=CurrentMinimum
        if(datasets[l][1]=='QCD' or datasets[l][1]=='W+JetsToQQ' or datasets[l][1]=='Z+JetsToQQ'):
            # NBG= NBG + PreSelectionFiles[l].Get(Cuts[0][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
            NBG=NBG+Norm
    cutflows=[]
    for i in range(len(datasets)):
        if(singlePlots):
            legend = TLegend(0.75,0.6,1,0.9)
            legend.SetFillStyle(0)
            legend.SetTextSize(0.02)
            legend.SetMargin(0.4)

        print('Drawing',datasets[i][1])
        currentCutflow=TH1F(datasets[i][1],datasets[i][1],NCuts,0,NCuts)
        cutflows.append(currentCutflow)
        #filling the current cutflow (with NEvents_weighted or NEvents_raw)
        if(normalise):
            if(StackBG and (datasets[i][1]=='QCD' or datasets[i][1]=='W+JetsToQQ' or datasets[i][1]=='Z+JetsToQQ')):
                NAll=NBG
            else:
                if((len(Cuts)==len(PreSelectionCuts)) or (len(Cuts)==(len(PreSelectionCuts)+len(SelectionCuts))) ):
                    NAll=PreSelectionFiles[i].Get(PreSelectionCuts[0][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
                else:
                    NAll=SelectionFiles[i].Get(SelectionCuts[0][0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)

        else:
            NAll=1
        for j in range(NCuts):
            cut=Cuts[j]
            if((len(Cuts)==len(PreSelectionCuts)) or (len(Cuts)==(len(PreSelectionCuts)+len(SelectionCuts))) and j<len(PreSelectionCuts)):
                NEvents=PreSelectionFiles[i].Get(cut[0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
            else:
                NEvents=SelectionFiles[i].Get(cut[0]+'/NEvents_%s'%weightedORraw).GetBinContent(1)
                # NEvents=NAll
            currentCutflow.GetXaxis().SetBinLabel(j+1,cut[1])
            currentCutflow.Fill(j+0.5,NEvents/NAll)
        #cosmectics for and draw current cutflow
        currentCutflow.SetLineColor(datasets[i][3])
        currentCutflow.SetMarkerSize(1.4)
        currentCutflow.GetYaxis().SetTitle(yTitle)
        HistMax=currentCutflow.GetMaximum()
        if(logY):
            if(singlePlots):
                MAX=float(10**(magnitude(HistMax)+3))
                MIN=float(10**(magnitude(currentCutflow.GetMinimum())-1))
            else:
                MAX=float(10**(magnitude(HistMax)+2))
                MIN=float(10**(magnitude(TotalMinimum)-1))

            MIN+=float(10**(magnitude(MIN)))
        else:
            MAX=1.1*HistMax
            MIN=0.
        currentCutflow.GetYaxis().SetRangeUser(MIN,MAX)
        print('RangeUser=(',MIN,',',MAX,')')
        print('drawOptions:',drawOptions)
        if(datasets[i][1]=='Data'):
            # legend.AddEntry(currentCutflow,datasets[i][1],'lep')
            # currentCutflow.SetMarkerStyle(8)
            # currentCutflow.Draw(drawOptions+'HP')
            legend.AddEntry(currentCutflow,datasets[i][1],'l')
            currentCutflow.Draw(drawOptions)
            if(not singlePlots and ('SAME' not in drawOptions)):
                drawOptions=drawOptions+'SAME'
        elif(StackBG and (datasets[i][1]=='QCD' or datasets[i][1]=='W+JetsToQQ' or datasets[i][1]=='Z+JetsToQQ')):
            legend.AddEntry(currentCutflow,datasets[i][1],'f')
            currentCutflow.SetFillColor(datasets[i][3])
            BGStack.Add(currentCutflow,drawOptions)
            # currentCutflow.Draw(drawOptions)
            PlotBGStack=True
        else:
            legend.AddEntry(currentCutflow,datasets[i][1],'l')
            currentCutflow.Draw(drawOptions)
            if(not singlePlots and ('SAME' not in drawOptions)):
                drawOptions=drawOptions+'SAME'
                
        if(singlePlots):
            legend.Draw()
            if(logY):
                canv.SetLogy()
            # canv.SetGrid()
            canv.SetTicks()
            gPad.RedrawAxis()
            canv.Print('cutflows/'+Region+'_cutflow_%s_%s.eps'%(datasets[i][1],weightedORraw))
    if(not singlePlots):
        if(PlotBGStack):
            BGStack.Draw(drawOptions)
        legend.Draw()
        if(logY):
            canv.SetLogy()
        # canv.SetGrid()
        canv.SetTicks()
        gPad.RedrawAxis()
        canv.Print('cutflows/'+Region+'_cutflow_%s.eps'%weightedORraw)

if(__name__=='__main__'):
    # Regions=['SignalRegion','HIGHSidebandRegion']
    # removeEvents=[True,False]
    Regions=['SignalRegion']
    removeEvents=[False]
    #cutflow(Region='SignalRegion',removeEvents=False,logY=True,normalise=True,singlePlots=False,drawOptions='HIST', weightedORraw ='weighted'):
    
    for Region in Regions:
        for removeEvent in removeEvents:
            cutflow(Region,removeEvent,True,True,False,'HIST','weighted')
            # cutflow(Region,removeEvent,True,True,False,'HIST','raw')
            cutflow(Region,removeEvent,True,False,True,'HIST TEXT90','weighted')
            cutflow(Region,removeEvent,True,False,True,'HIST TEXT90','raw')
