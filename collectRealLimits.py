#!/usr/local/bin/python2.7
import ROOT as rt
import csv, glob, os

if(__name__=='__main__'):
    #parameter,lmean,l1down,l1up,umean,u1down,u1up
    #T0,-0.17734370960084056,-0.1966518508002894,-0.1593247554784427,0.17734370960084056,0.1966518508002894,0.1593247554784427
    # limits_path='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/backup/03_27_09_34_44'
    channels=['VV']
    # parameters=['S1','M1','T7']

    limits_path='/nfs/dust/cms/user/albrechs/CMSSW_8_1_0/src/DijetCombineLimitCode/Limits'    
    # channels=['VV','ssWW','ZZ']
    parameters=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]
    
    for channel in channels:
        csv_out=open('%s_limits.csv'%channel,'wt')
        csv_writer=csv.DictWriter(csv_out,fieldnames=['parameter','lmean','l1down','l1up','umean','u1down','u1up'])
        csv_writer.writeheader()
        
        for parameter in parameters:
            if(not os.path.isfile(limits_path+'/%s_%s_limits.csv'%(channel,parameter))):
                continue
            csv_in=open(limits_path+'/%s_%s_limits.csv'%(channel,parameter),'rb')
            reader = csv.DictReader(csv_in)
            for row in reader:
                csv_writer.writerow({'parameter':row['parameter'],
                        'lmean':row['lmean'],
                        'l1down':row['l1down'],
                        'l1up':row['l1up'],
                        # 'l1down':inter_1down[0][0]-inter_mean[0][0],
                        # 'l1up':inter_1up[0][0]-inter_mean[0][0],
                        'umean':row['umean'],
                        'u1down':row['u1down'],
                        'u1up':row['u1up']
                        # 'u1down':inter_1down[1][0]-inter_mean[1][0],
                        # 'u1up':inter_1up[1][0]-inter_mean[1][0]
                        })
            csv_in.close()
        csv_out.close()
