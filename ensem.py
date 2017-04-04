
import itertools

import os
from collections import Counter


def process_frames(p,q,t):
    average_ensemble_sum=[]
    for i in range(0,48):
        average_ensemble_sum.append(0)
    ensemble_set=[]
    # Creating 48 ensembles of the frame set,ensemble_set containing 48 ensembles
    ensemble_set=sampling(p,q)

    # Creating 100 video volumes in each ensemble,vol_set containg 48 lists,
    # each list contains 100 video volumes
    vol_set=[]
    gray_sum=[]
    gray_sum_l=[]
    gray_sum_s=[]
    for i in range(0,48):
        vol_set.append(video_volume(ensemble_set[i],q))

    for i in range(0,48):
            for j in range(0,100):
                for k in range(0,q):
                    vol_set[i][j][k]=list(itertools.chain.from_iterable(vol_set[i][j][k]))
                    gray_sum.append(sum(vol_set[i][j][k]))
    s=0
    e=q
    for i in range(0,4800):
        gray_sum_l.append(max(gray_sum[s:e]))
        gray_sum_s.append(min(gray_sum[s:e]))
        s+=q
        e+=q
    re_list=[]
    re_list.append(gray_sum_l)
    re_list.append(gray_sum_s)
    return re_list

#Sampling function this will create 48 samples of incoming video sequence 640*480
def sampling(p,q):
    total_frames=q
    ensemble_row=6
    ensemble_col=8
    frame_ensemble=[]
    ensemble_set=[]

    args1=[0,80,total_frames,p]
    args2=[80,160,total_frames,p]
    args3=[160,240,total_frames,p]
    args4=[240,320,total_frames,p]
    args5=[320,400,total_frames,p]
    args6=[400,480,total_frames,p]
    args_list=[args1,args2,args3,args4,args5,args6]

    # parallising part
    # ensemble_set = f.map(core_ensembling,args_list)
    # ensemble_set=list(itertools.chain.from_iterable(ensemble_set))
    # parallising part

    set1=core_ensembling(args1)
    set2=core_ensembling(args2)
    set3=core_ensembling(args3)
    set4=core_ensembling(args4)
    set5=core_ensembling(args5)
    set6=core_ensembling(args6)

    ensemble_set = list(itertools.chain(set1,set2,set3,set4,set5,set6))

    return ensemble_set

# video_volume function will create 100 video voulme of a ensemble.An ensemble is divided in to 100 video volumes
# 80*80 ensemble is divided into 100 8*8 video volumes
def video_volume(ensemble,q):
        volume_set=[]
        total_frames=q
        volume_row=10
        volume_col=10

        args1=[0,8,0,8,volume_row,volume_col,ensemble,q]
        args2=[8,16,0,8,volume_row,volume_col,ensemble,q]
        args3=[16,24,0,8,volume_row,volume_col,ensemble,q]
        args4=[24,32,0,8,volume_row,volume_col,ensemble,q]
        args5=[32,40,0,8,volume_row,volume_col,ensemble,q]
        args6=[40,48,0,8,volume_row,volume_col,ensemble,q]
        args7=[48,56,0,8,volume_row,volume_col,ensemble,q]
        args8=[56,64,0,8,volume_row,volume_col,ensemble,q]
        args9=[64,72,0,8,volume_row,volume_col,ensemble,q]
        args10=[72,80,0,8,volume_row,volume_col,ensemble,q]
        # args_list=[args1,args2,args3,args4,args5,args6,args7,args8,args9,args10]
        #
        # volume_set = g.map(core_volume,args_list)
        # volume_set=list(itertools.chain.from_iterable(volume_set))

        set1=core_volume(args1)
        set2=core_volume(args2)
        set3=core_volume(args3)
        set4=core_volume(args4)
        set5=core_volume(args5)
        set6=core_volume(args6)
        set7=core_volume(args7)
        set8=core_volume(args8)
        set9=core_volume(args9)
        set10=core_volume(args10)


        volume_set = list(itertools.chain(set1,set2,set3,set4,set5,set6,set7,set8,set9,set10))

        return volume_set

#used in sampling function to do repetative task
def core_ensembling(args):
    ensemble_set=[]
    row_no=args[0]
    max_row=args[1]
    total_frames=args[2]
    p=args[3]
    c1=0
    c2=80
    for j in range(0,8):
        ensemble=[]
        for k in range(0,total_frames):
            frame_ensemble=[]
            for l in range(row_no,max_row):
                frame_ensemble.append(p[k][l][c1:c2])
            ensemble.append(frame_ensemble)
        c1=c1+80
        c2=c2+80
        ensemble_set.append(ensemble)
    return ensemble_set

#used in video_volume function to do repetative task
def core_volume(args):
    v_set=[]
    row_no=args[0]
    max_row=args[1]
    c1=args[2]
    c2=args[3]
    volume_row=args[4]
    volume_col=args[5]
    ensemble=args[6]
    total_frames=args[7]
    for j in range(0,volume_col):
        single_volume=[]
        for k in range(0,total_frames):
            frame_volume=[]
            for l in range(row_no,max_row):
                frame_volume.append(ensemble[k][l][c1:c2])
            single_volume.append(frame_volume)
        v_set.append(single_volume)
        c1=c1+8
        c2=c2+8
    return v_set

def clear_folder():
    dirPath = 'C:\\FlaskVideo\\static\\abnormal_frames'
    fileList = os.listdir(dirPath)
    for fileName in fileList:
     os.remove(dirPath+"/"+fileName)

def mod_function(alist):
    mod_list=[[x] for x in range(0,4800)]
    temp_list=[]
    f_c=0
    for i in range(0,4800):
        count = Counter(alist[i])
        temp_list=count.most_common()
        l=len(temp_list)
        if l<2:
            mod_list[i]=temp_list[0][0]
        if l>1:
            for p in range(0,l):
                mod_list[i].append(temp_list[p][0])
    return mod_list

def stat_range(alist):
    ulist=sorted(alist)
    p=sum(alist)/len(alist)
    return p
def round(alist):
    rounding_factor=1000
    blist=[]
    temp_var=0
    l=len(alist)
    for i in range(0,l):
        rem=alist[i]%rounding_factor
        if rem==0:
            blist.append(alist[i])
        if rem!=0:
            alist[i]=alist[i]-rem
            blist.append(alist[i])
    return blist
def most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]