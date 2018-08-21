import collections,csv

sets=collections.OrderedDict()

with open('/afs/desy.de/user/a/albrechs/aQGCVVjj/python/ReweightingRanges/VVRange.csv','rb') as csvfile:
    setreader=csv.DictReader(csvfile)
    for row in setreader:
        sets.update({row['parameter']:[
                    int(row['Npoints']),
                    float(row['start']),
                    float(row['stepsize'])
                    ]})
        
def getPointName(OpName,i):
    name=""
    parameter=100*sets[OpName][1]+i*100*sets[OpName][2]
    name+="%.2f"%(parameter/100)
    name = name.replace('.','p')
    if('-' in name):
        name = name.replace('-','m')
    return name

def getPointNameI(Index):
    N=0
    OpName=''
    for i in range(len(sets.items())):
        OpName=sets.items()[i][0]
        N=(N+sets.items()[i][1][0])
        if(N > Index):
            break
    InternIndex=Index-(N-sets[OpName][0])
    # print("The Weight with number "+str(Index)+" is part of "+OpName+" (Number "+str(InternIndex)+")")
    # print("Name of Point:"+getPointName(OpName,InternIndex))
    return (OpName,getPointName(OpName,InternIndex)[:-1])
    
def fullList(parameters,alternative_iter=[]):
    list=[]
    for parameter in parameters:
        if len(alternative_iter)!=0:
            iterations=alternative_iter
        else:
            iterations=range(sets[parameter][0])
        for i in iterations:
            list.append(getPointName(parameter,i))
    return list

def OpList(parameter,N=-1,alternative_iter=[]):
    list=[]
    if len(alternative_iter)!=0:
        iterations=alternative_iter
    else:
        if(N==-1):
            iterations=range(sets[parameter][0])
        else:
            N=N/2
            lhalf=range( ( (sets[parameter][0]-1) / 2 ) - N,( ( sets[parameter][0]-1 ) / 2 ) )
            uhalf=range( ( (sets[parameter][0]-1) / 2 )+1,( (sets[parameter][0]-1) / 2 ) + N+1)
            print(sets[parameter][0])
            print('lhalf',lhalf)
            print('uhalf',uhalf)

            iterations=lhalf+uhalf
            iterations.sort()
            # lower_half=range(0,sets[parameter][0]/2,(sets[parameter][0]-1)/N)
            # if(len(lower_half)!=N/2):
            #     lower_half.pop()
            # upper_half=[x*(-1) for x in range(-(sets[parameter][0]-1),-sets[parameter][0]/2,(sets[parameter][0]-1)/N)]
            # if(len(upper_half)!=N/2):
            #     upper_half.pop()
            # print(len(lower_half),len(upper_half))
            # iterations=lower_half+upper_half
            # iterations.sort()

    j=0
    for i in iterations:
        # if(j==(len(iterations))/2):
            # print('----------')
        j+=1    
        if( i != ((sets[parameter][0]-1)/2) ): #don't add 0
            list.append(getPointName(parameter,i))
            # print(i,getPointName(parameter,i))
    return list

def NPoints(parameter):
    return sets[parameter][0]


if(__name__=='__main__'):
    # OpList('S0',5)
    for i in range(200):
        print getPointNameI(i)
