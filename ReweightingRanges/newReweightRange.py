import os, shutil, subprocess, glob, csv

def getPointName(set,point):
    name="F%s_"%set
    #point=10*startx+i*10*increment
    if(point>=0):
        name+="%ip%02i"%(point/100,(point%100))
    else:
        name+="m%ip%02i"%(-point/100,(-point%100))    
    return name

if(__name__=="__main__"):
    # BosonChannel="WPWP"
    # operators=["S0","S1","M0","M1","M6","M7","T0","T1","T2"]
    BosonChannel="VV"
    operators=["S0","S1","M0","M1","M2","M3","M4","M5","M6","M7","T0","T1","T2","T5","T6","T7","T8","T9"]

    # sets={
    #     "S0":[1,91,-900.0,20.0],
    #     "S1":[2,67,-330.0,10.0],
    #     "M0":[3,85,-42.0,1.0],
    #     "M1":[4,67,-165.0,5.0],
    #     "M6":[9,85,-84.0,2.0],
    #     "M7":[10,121,-300.0,5.0],
    #     "T0":[11,69,-6.8,0.2],
    #     "T1":[12,51,-12.5,0.5],
    #     "T2":[13,83,-20.5,0.5]
    #     }

    #for WPWP
    # sets={
    #     "S0":[1,113,-448.0,8.0],
    #     "S1":[2,101,-1500.0,30.0],
    #     "M0":[3,107,-159.0,3.0],
    #     "M1":[4,107,-159.0,3.0],
    #     "M6":[9,107,-318.0,6.0],
    #     "M7":[10,115,-228.0,4.0],
    #     "T0":[11,121,-7.2,0.12],
    #     "T1":[12,127,-1.89,0.03],
    #     "T2":[13,101,-9.0,0.18]
    #     }

    sets={}
    with open(BosonChannel+'Range.csv','rb') as csvfile:
        snippet=''
        setreader=csv.DictReader(csvfile)
        for row in setreader:
            sets.update({row['parameter']:[
                    int(row['anoinput']),
                    int(row['Npoints']),
                    float(row['start']),
                    float(row['stepsize'])
                    ]})

            snippet+='//%s=[%i,%.2f,%.2f,%.2f]\n'%(row['parameter'],int(row['Npoints']),float(row['stepsize']),float(row['start']),float(row['end']))
            snippet+='for(unsigned int i=0; i<%i; i++){\n'%int(row['Npoints'])
            snippet+='reweight_names.push_back(getParName("%s",%.2ff,%.2ff,i));\n'%(row['parameter'],float(row['start']),float(row['stepsize']))
            snippet+='}\n'
        
        print 'snippet for Mjj:'
        print snippet




    print sets
    with open(BosonChannel+"Range.dat","wt") as fout:
        fout.write("change helicity False\n")
        fout.write("change rwgt_dir rwgt\n")
        fout.write("\n\n")
        sum_points=0

        for op in operators:
            for i in range(0,sets[op][1]):
                point=100*sets[op][2]+i*100*sets[op][3]
                fout.write("#******************** F%s ********************\n"%op)
                fout.write("launch --rwgt_name=%s\n"%getPointName(op,point))
                if(sets[op][0]!=11):
                    fout.write("        set anoinputs 11 0.000000e+00\n")
                fout.write("        set anoinputs %i %8.6fe-12\n"%(sets[op][0],point/100))
                fout.write("\n\n")
                sum_points+=1
        print "Total number of reweighting points:", sum_points
