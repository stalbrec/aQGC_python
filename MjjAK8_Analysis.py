#!/usr/local/bin/python2.7
import ParSet,subprocess,os,shutil,csv,glob
from time import gmtime,strftime

def LimitChannel(channel):
    # latex_in=open('latex.txt','rt')
    dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    # dim8op=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]

    for cut in ['detaAk8selVV','detaAk4sel','invMAk4sel_1p0','invMAk4sel_1p2','invMAk4sel_1p5_allcuts']:
    # for cut in ['detaAk4sel','invMAk4sel_1p5_allcuts','invMAk4sel_2p0_allcuts']:
    # for cut in ['detaAk8selVV']:
    # for cut in ['invMAk4sel_1p5_allcuts']:
        # latex_out=open('output/%s_new_%s.tex'%(channel,cut),'wt')
        plot_dir='output/plots/%s'%cut
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)        
            			
        csv_out=open('output/%s_limits_%s.csv'%(channel,cut),'wt')
        csvwriter=csv.DictWriter(csv_out,fieldnames=['parameter','limmin','limmax','limminmax','limitCalc_succeeded'])
        csvwriter.writeheader()
        
        for op in dim8op:
            print '=============%s-%s============='%(op,cut)
            current_Set_AK8 = ParSet.Set(op,channel,cut)

            current_Set_AK8.calcLimits(True)
            
            current_Set_AK8.exportPlot(True,plot_dir,True)

            print 'Limits:'
            print op,'-',current_Set_AK8.Limits

            current_Set_AK4 = ParSet.Set(op,channel,cut,4)

            current_Set_AK4.exportPlot(True,'output/plots/%s'%cut,True)
            
        
            # limits.append(current_Set.Limits)
            # limits_success.append(str(current_Set.limitCalc_succeeded))
            print '==========================='
            print
        

            # for line in latex_in:
            #     if op in line:
            #         latex_out.write(line.replace('X','(%.2f, %.2f)'%current_Set.Limits))
            csvwriter.writerow({'parameter':op,
                                'limmin':current_Set_AK8.Limits[0],
                                'limmax':current_Set_AK8.Limits[1],
                                'limminmax':'(%.2f, %.2f)'%current_Set_AK8.Limits,
                                'limitCalc_succeeded':str(current_Set_AK8.limitCalc_succeeded)})
        # latex_out.close()
        csv_out.close()
    # latex_in.close()

def FitChannel(channel):
    # dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    dim8op=["T0"]
    # dim8op=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    chi2={}
    bestn={}
    for cut in ['detaAk8selVV','detaAk4sel','invMAk4sel_1p0','invMAk4sel_1p2','invMAk4sel_1p5_allcuts']:
    # for cut in ['invMAk4sel_1p5_allcuts']:
    # for cut in ['detaAk8selVV']:
        for op in dim8op:


            
            # plot_dir='output/plots/Fits/%s/%s/'%(cut,op)
            # if not os.path.exists(plot_dir):
            #     os.makedirs(plot_dir)

            refplot_dir='output/plots/Fits/refpoint/'
            if not os.path.exists(refplot_dir):
                os.makedirs(refplot_dir)

            print '+++++++++++Fit - %s - %s+++++++++++'%(op,cut)
            current_Set=ParSet.Set(op,channel,cut)

            # current_Set.FitSignal(plot_dir)
            # current_Set.RooFitSignal(plot_dir)
            current_Set.RooFitRef(refplot_dir)

    #         chi2.update({cut:current_Set.chi2_dict})
    #         bestn.update(current_Set.best_n)
            
    # for cut in ['detaAk8selVV','detaAk4sel','invMAk4sel_1p0','invMAk4sel_1p2','invMAk4sel_1p5_allcuts']:
    #     print '------------------------------- %s -------------------------------:'%cut
    #     print 'best n:',bestn[cut][0],'w/ chi2/ndf:',bestn[cut][1]
    #     print chi2[cut]
if(__name__=="__main__"):
    # channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    # channels=["WPWP","WPWM","WMWM"]
    channels=["WPWM"]
    # channels=["WPZ"]

    archiv_path='/afs/desy.de/user/a/albrechs/aQGCVVjj/python/output/archiv/%s/'%strftime("%m_%d_%H_%M_%S",gmtime())
    os.mkdir(archiv_path)
        
    backup_files=[]

    for channel in channels:
        # LimitChannel(channel)
        FitChannel(channel)
        # filenames=["%s_%s.eps"%(channel,op) for op in dim8op]
        # os.chdir("plots")
        # subprocess.call(["gs","-sPAPERSIZE=a4","-sDEVICE=pdfwrite","-dNOPAUSE","-dBATCH","-dSAFER","-sOutputFile=plots.pdf"]+filenames)
        # os.chdir("..")

        shutil.copyfile('ReweightingRanges/%sRange.csv'%channel,'%s/%sRange.csv'%(archiv_path,channel))
    
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
        

