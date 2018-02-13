#!/usr/local/bin/python2.7
import ParSet,subprocess,os,shutil,csv
from time import gmtime,strftime

if(__name__=="__main__"):
    # channels=["WPWP","WPWM","WMWM","WPZ","WMZ","ZZ"]
    channels=["WPWP"]
    dim8op=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    for channel in channels:
        latex_in=open('latex.txt','rt')


        # limits=[]
        # limits_success=[]
        for cut in ['detaAk4sel','invMAk4sel_allcuts']:
            latex_out=open('output/%s_new_%s.tex'%(channel,cut),'wt')
            
            csv_out=open('output/%s_limits_%s.csv'%(channel,cut),'wt')
            csvwriter=csv.DictWriter(csv_out,fieldnames=['parameter','limmin','limmax','limminmax','limitCalc_succeeded'])
            csvwriter.writeheader()
            
            for op in dim8op:
                current_Set = ParSet.Set(op,channel,cut)
                print '=============%s-%s============='%(op,cut)
                current_Set.exportPlot(True)
                current_Set.calcLimits()
                print 'Limits:'
                print op,'-',current_Set.Limits
                
                # limits.append(current_Set.Limits)
                # limits_success.append(str(current_Set.limitCalc_succeeded))
                print '==========================='
                print
        

                for line in latex_in:
                    if op in line:
                        latex_out.write(line.replace('X','(%.2f, %.2f)'%current_Set.Limits))
                csvwriter.writerow({'parameter':op,
                                 'limmin':current_Set.Limits[0],
                                 'limmax':current_Set.Limits[1],
                                 'limminmax':'(%.2f, %.2f)'%current_Set.Limits,
                                 'limitCalc_succeeded':str(current_Set.limitCalc_succeeded)})
            latex_out.close()
            csv_out.close()
        latex_in.close()

        # filenames=["%s_%s.eps"%(channel,op) for op in dim8op]
        # os.chdir("plots")
        # subprocess.call(["gs","-sPAPERSIZE=a4","-sDEVICE=pdfwrite","-dNOPAUSE","-dBATCH","-dSAFER","-sOutputFile=plots.pdf"]+filenames)
        # os.chdir("..")

        
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
        

        archiv_path='/afs/desy.de/user/a/albrechs/aQGCVVjj/python/output/archiv/%s/'%strftime("%m_%d_%H_%M",gmtime())
        os.mkdir(archiv_path)
        shutil.copyfile('output/%s_new.tex'%channel,archiv_path+'%s_new.tex'%channel)
        shutil.copyfile('output/%s_limits.csv'%channel,archiv_path+'%s_limits.csv'%channel)
        shutil.copyfile('ReweightingRanges/%sRange.csv'%channel,archiv_path+'%sRange.csv'%channel)
        os.chdir('output')
        subprocess.call(['tar','cfz','plots.tar.gz','plots/'])
        shutil.move('plots.tar.gz',archiv_path)
        os.chdir('..')
