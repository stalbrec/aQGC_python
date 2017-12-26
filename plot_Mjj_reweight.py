from ROOT import gROOT, TCanvas, TF1, TFile
import myutils,shutil,os


def processSet(set):
    histnames=[]
    myutils.getHistNames(set,histnames)
    title="invariant Mass of AK8 Jets (Scanned through %s-Operator)"%set
    c2 = TCanvas('c2',title ,200,10,700,500)
    back_hist.SetTitle(title)
    back_hist.Draw("HIST")
    #hists=[]
    for histname in histnames:
        #hists.append(signal_file.Get('/MjjHists_detaAk4sel_allcuts/%s'%histname))
    #for hist in hists:
        hist=signal_file.Get('/MjjHists_detaAk4sel_allcuts/%s'%histname)
        hist.Draw("H1][SAME")
        sum_events=0 
        for i in range(bin,hist.GetNbinsX()): 
            sum_events+=hist.GetBinContent(i)
        f=open('results/%s.txt'%set,"a")
        f.write('%s:  %f\n'%(histname,sum_events))    
    c2.SetLogy()
    c2.SetTitle(title)
    c2.Update()
    c2.Print("~/www/%s.png"%set)

if(__name__=="__main__"):
    gROOT.Reset()

    signal_file = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/testuhh2.AnalysisModuleRunner.MC.aQGC_WPWPjj_hadronic.root")
    background_file = TFile("/nfs/dust/cms/user/albrechs/UHH2_Output/uhh2.AnalysisModuleRunner.MC.MC_QCD.root")

    back_hist=background_file.Get("detaAk4sel_allcuts/M_jj_AK8")
    back_hist.SetLineColor(6)
    
    bin=0
    content=0

    crossed_start=False;
    for i in range(0,back_hist.GetNbinsX()):
        content=back_hist.GetBinContent(i)
        bin=i
        print "BinContent(",bin,"):",content
        if(content>0):
            crossed_start=True
        if(crossed_start):
            if(content <= 10):
                break

    back_hist.GetXaxis().SetRangeUser(back_hist.GetBinCenter(bin-1),7500) 

    print "printing 10 before and after found bin (",bin,"):"
    for i in range(-10,10):
        print "BinContent(",bin+i,"):",back_hist.GetBinContent(bin+i)," BinCenter:" ,back_hist.GetBinCenter(bin+i)


    shutil.rmtree('results')
    os.mkdir('results')

    sets=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    for set in sets:
        processSet(set)
