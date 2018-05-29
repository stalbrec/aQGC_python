#!/usr/local/bin/python2.7
import ParSet,subprocess,os,shutil,csv,glob
from time import gmtime,strftime

def LimitChannel(channel,dim8op,cuts):

    for cut in cuts:
        plot_dir='output/limit/plots/%s'%channel
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)        
            			
        csv_out=open('output/limit/%s_limits_%s.csv'%(channel,cut),'wt')
        csvwriter=csv.DictWriter(csv_out,fieldnames=['parameter','limmin','limmax','limminmax','limitCalc_succeeded'])
        csvwriter.writeheader()

        csv_summary=open('output/limit/limits.csv','r')
        r=csv.reader(csv_summary)
        header=r.next()
        header.append(channel)
        rows=[]
        rows.append(header)

        for op in dim8op:
            print '=============%s-%s============='%(op,cut)
            current_Set_AK8 = ParSet.Set(op,channel,cut,'SignalRegion/tau21sel_45/')
            current_Set_AK8.testSensitivity(True,plot_dir)
            print 'Limits:'
            print op,'-',current_Set_AK8.Limits
            print '==========================='
            print        
            csvwriter.writerow({'parameter':op,
                                'limmin':current_Set_AK8.Limits[0],
                                'limmax':current_Set_AK8.Limits[1],
                                'limminmax':'(%.2f, %.2f)'%current_Set_AK8.Limits,
                                'limitCalc_succeeded':str(current_Set_AK8.limitCalc_succeeded)})
            row=r.next()
            row.append('(%.2f, %.2f)'%current_Set_AK8.Limits)
            rows.append(row)
        csv_out.close()
        csv_summary.close()

        csv_summary_new=open('output/limit/limits.csv','wt')
        w=csv.writer(csv_summary_new,delimiter=',')
        w.writerows(rows)
        csv_summary_new.close()
        
def exportMjjPlots(channel,dim8op,cuts):
    for cut in cuts:
        plot_dir='output/plots/MjjPlots/%s/%s'%(channel,cut)
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)        
        for op in dim8op:
            current_Set_AK8 = ParSet.Set(op,channel,cut,'SignalRegion')            
            current_Set_AK8.exportPlot(True,plot_dir,True)

            current_Set_AK4 = ParSet.Set(op,channel,cut,'SignalRegion',4)
            current_Set_AK4.exportPlot(True,plot_dir,True)


def FitChannel(channel,dim8op,cuts):
    chi2={}
    bestn={}
    for cut in cuts:
        for op in dim8op:           
            plot_dir='output/plots/Fits/%s/%s/'%(cut,op)
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)

            refplot_dir='output/plots/Fits/refpoint/'
            if not os.path.exists(refplot_dir):
                os.makedirs(refplot_dir)

            print '+++++++++++Fit - %s - %s+++++++++++'%(op,cut)
            current_Set=ParSet.Set(op,channel,cut,'SignalRegion')

            # current_Set.FitSignal(plot_dir)
            # current_Set.RooFitSignal(plot_dir)

            if(op == 'T0'):
                current_Set.RooFitSig(refplot_dir)
            
    #         chi2.update({cut:current_Set.chi2_dict})
    #         bestn.update(current_Set.best_n)
            
    # for cut in cuts:
    #     print '------------------------------- %s -------------------------------:'%cut
    #     print 'best n:',bestn[cut][0],'w/ chi2/ndf:',bestn[cut][1]
    #     print chi2[cut]




if(__name__=="__main__"):
    # dim8op=["T0"]
    # channels=['VV']

    # dim8op=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    # channels=["WZ","ZZ"]

    dim8op=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    # # channels=['WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    # channels=['ssWW','VV','WPWP','WPWM','WMWM','WPZ','WMZ','ZZ']
    channels=['VV','ssWW','ZZ']

    # cuts=['detaAk8selVV','detaAk4sel','invMAk4sel_1p0','invMAk4sel_1p2','invMAk4sel_1p5_allcuts']
    # cuts=['detaAk8selVV','detaAk4sel','invMAk4sel_1p0']
    cuts=['invMAk4sel_1p0']

    backup=False
    archiv_path='/afs/desy.de/user/a/albrechs/aQGCVVjj/python/output/archiv/%s/'%strftime("%m_%d_%H_%M_%S",gmtime())
    if(backup):
        os.mkdir(archiv_path)
    backup_files=[]

    # if os.path.exists('output/limit/limits.csv'):
    #     os.remove('output/limit/limits.csv')
    csv_init=open('output/limit/limits.csv','wt')
    csvwriter=csv.writer(csv_init,delimiter=',')
    csvwriter.writerow(['parameter'])
    for op in dim8op:
        csvwriter.writerow([op])
    csv_init.close()
    for channel in channels:
        LimitChannel(channel,dim8op,cuts)
        # exportMjjPlots(channel,dim8op,cuts)
        # FitChannel(channel,dim8op,cuts)
        # filenames=["%s_%s.eps"%(channel,op) for op in dim8op]
        # os.chdir("plots")
        # subprocess.call(["gs","-sPAPERSIZE=a4","-sDEVICE=pdfwrite","-dNOPAUSE","-dBATCH","-dSAFER","-sOutputFile=plots.pdf"]+filenames)
        # os.chdir("..")

        if(backup):             
            shutil.copyfile('ReweightingRanges/%sRange.csv'%channel,'%s/%sRange.csv'%(archiv_path,channel))
    


    if(backup):
        os.chdir('output')
        backup_files=glob.glob("*.csv")
        backup_files+=glob.glob("*.tex")
        for bfile in backup_files:
            shutil.copyfile(bfile,archiv_path+bfile)
        subprocess.call(['tar','cfz','plots.tar.gz','plots/'])
        shutil.move('plots.tar.gz',archiv_path)
        os.chdir('..')
    
        # fout=open("output/%s_new.tex"%channel,"wt")
        # with open("latex.txt","rt") as fin:
        #     for line in fin:
        #         fout.write(line.replace('X','(%.2f, %.2f)'%limits[dim8op.index(line[4:6])]))
        # fout.close()
        # with open('output/%s_limits.csv'%channel,'wt') as csvfile:
        #     writer=csv.DictWriter(csvfile,fieldnames=['parameter','limmin','limmax','limminmax','limitCalc_succeeded'])
        #     writer.writeheader()
        #     for i in range(0,len(dim8op)):
        #         limit=limits[i]
        #         writer.writerow({'parameter':dim8op[i],
        #                          'limmin':limits[i][0],
        #                          'limmax':limits[i][1],
        #                          'limminmax':'(%.2f, %.2f)'%limits[i],
        #                          'limitCalc_succeeded':limts_success[i]})
        # csvfile.close()
