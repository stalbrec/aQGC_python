from ROOT import TFile, TH1F, THStack, gROOT,TCanvas,gStyle,TLegend
from array import array


if(__name__=="__main__"):
    path='/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.'
    
    inputFiles=["MC.MC_aQGC_WPWPjj_hadronic.root","MC.MC_aQGC_WPWMjj_hadronic.root","MC.MC_aQGC_WMWMjj_hadronic.root","MC.MC_QCD.root"]
    # inputFiles=["MC.MC_QCD.root"]
    # tostack=["MC.MC_QCD.root"]
    tofill=["MC.MC_QCD.root"]
    sampleNames=['WPWP','WPWM','WMWM','QCD']
    
    #plot this Histogram
    hist_to_Plot=['M_jj_AK8']
    
    #from these Directories
    dir_to_Plot=['detaAk4sel','invMAk4sel_1p5_allcuts','invMAk4sel_2p0_allcuts']
    # dir_to_Plot=['detaAk4sel']


    #rebinning 20 bins 500GeV the (21 values (->lower_edges) - the last ist the upper_edge of the last bin
    #will rebin all histograms!!!
    rebin=True
    nBins=20
    xbins= array('d')
    for i in range(0,nBins+1):
        xbins.append(i*500)
    print 'nBins:', len(xbins)
    
    gROOT.SetBatch(True)
    gROOT.ProcessLine( "gErrorIgnoreLevel = 2001;")

    for dir in dir_to_Plot:
        
        for histname in hist_to_Plot:
            plottitle="invariant Mass of AK8 Jets"
            canv = TCanvas(plottitle,plottitle,600,600)
            #if(logY):
            canv.SetLogy()

            #turning off the standard Statistic-Box
            gStyle.SetOptStat(0)
            
            legend = TLegend(0.5,0.7,0.9,0.9)
            
            drawOpt='HE1'

            rf_stack=[]
            rf_sup=[]

            maxY=0

            for file in inputFiles:
                if(file in tofill):                    
                    rf_stack.append(TFile(path+file,'READ'))
                else:
                    rf_sup.append(TFile(path+file,'READ'))
            

            stack=THStack('stack',plottitle)
            hist_counter=0

            for rf in rf_stack:
                if(rebin):
                    hist_oldbin=rf.Get(dir+'/'+histname)
                    hist=hist_oldbin.Rebin(nBins,"new binning",xbins)
                else:
                    hist=rf.Get(dir+'/'+histname)

                hist.SetFillColor(867+hist_counter)
                hist.SetLineColor(867+hist_counter)
                hist.SetTitle('stack')
                stack.Add(hist)
                hist_counter=hist_counter+1

            
            stack.Draw(drawOpt)
            stack.GetXaxis().SetTitle('M_{jj-AK8} [GeV/c^{2}]')
            stack.GetYaxis().SetTitle('Events')
            # stack.Draw(drawOpt)

            drawOpt=drawOpt

            for rf in rf_sup:
                if(rebin):
                    hist_oldbin=rf.Get(dir+'/'+histname)
                    hist=hist_oldbin.Rebin(nBins,"new binning",xbins)
                else:
                    hist=rf.Get(dir+'/'+histname)
                
                hist.SetLineColor(1)
                hist.SetLineStyle(hist_counter)
                hist.SetTitle('stack_%i'%hist_counter)
                
                stack.Add(hist)
                hist_counter=hist_counter+1

            stack.Draw('nostack'+drawOpt)

            canv.Update()
            canv.Print('%s_%s.eps'%(histname,dir))

    # test=raw_input('Press Enter to continue...')
