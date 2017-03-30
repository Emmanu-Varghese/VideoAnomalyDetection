import cv2

import time
import itertools

import ensem



def capture_run(path):

    #setting timeout to 30s
    # timeout=10

    #creating video capture object
    capture=cv2.VideoCapture(path)

    #Set the resolution of capturing to 640W*480H
    capture.set(3,640)
    capture.set(4,480)
    frame_set=[]
    start_time=time.time()

    ###############################

    cap = cv2.VideoCapture(path)

    while not cap.isOpened():
        cap = cv2.VideoCapture(path)
        cv2.waitKey(1000)
        print "Wait for the header"

    pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    while True:
        flag, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if flag:
            # The frame is ready and already captured
            frame_set.append(gray)
            (h, w) = gray.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            rotated = cv2.warpAffine(gray, M, (w, h))
            cv2.imshow('video',gray)
            if(len(frame_set)==5):
                frame_time=time.time()
            pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            print str(pos_frame)+" frames"
        else:
            # The next frame is not ready, so we try to read it again
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
            print "frame is not ready"
            # It is better to wait for a while for the next frame to be ready
            cv2.waitKey(1000)

        if cv2.waitKey(10) == 27:
            break
        if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
            # If the number of captured frames is equal to the total number of frames,
            # we stop
            break

    cap.release()
    cv2.destroyAllWindows()
    
    print len(frame_set)

    #Total no of frames captured is found.Rouding it to multiple of 100
    frame_nos=len(frame_set)
    frame_rem=(frame_nos%5)

    if(frame_rem)==0:
        frame_nos=frame_nos
    else:frame_nos=frame_nos-frame_rem
    print "Total no of frames "+ str(frame_nos)
    total_frame_packs=frame_nos/5
    s_frame_no=0
    e_frame_no=5

    gray_sum_l_w=[]
    gray_sum_s_w=[]
    gray_sum=[]

    f_c=0
    f_list=[[x] for x in range(0,48)]
    g_list=[[x] for x in range(0,48)]

    f_list_l=[]
    g_list_s=[]
    mod_max_list=[]
    mod_min_list=[]

    # iterate through packs

    for i in range(total_frame_packs):
        ensemble_set=[]
        m_list_l= []
        m_list_s= []
        # Creating 48 ensembles of the frame set,ensemble_set containing 48 ensembles
        ensemble_set=ensem.sampling(frame_set[s_frame_no:e_frame_no],5)

        # Creating 100 video volumes in each ensemble,vol_set containg 48 lists,
        # each list contains 100 video volumes
        vol_set=[]
        gray_sum=[]
        gray_sum_l=[]
        gray_sum_s=[]

        for i in range(0,48):
            vol_set.append(ensem.video_volume(ensemble_set[i],5))

        for i in range(0,48):
            for j in range(0,100):
                for k in range(0,5):
                    vol_set[i][j][k]=list(itertools.chain.from_iterable(vol_set[i][j][k]))
                    gray_sum.append(sum(vol_set[i][j][k]))
        s=0
        e=5
        for i in range(0,4800):
            gray_sum_l.append(max(gray_sum[s:e]))
            m_list_l.append(max(gray_sum[s:e]))
            gray_sum_s.append(min(gray_sum[s:e]))
            m_list_s.append(min(gray_sum[s:e]))
            s+=5
            e+=5

        if not gray_sum_l_w:
            for i in range(0,4800):
                gray_sum_l_w.append(gray_sum_l[i])

        if not gray_sum_s_w:
            for i in range(0,4800):
                gray_sum_s_w.append(gray_sum_s[i])
        for i in range(0,4800):
            if gray_sum_l_w[i] < gray_sum_l[i]:
                gray_sum_l_w[i] = gray_sum_l[i]
            if gray_sum_s_w[i] > gray_sum_s[i]:
                gray_sum_s_w[i]=gray_sum_s[i]

        p_count=0
        temp_max=0
        temp_min=0
        j=0
        for i in range(0,4800):
            p_count+=1
            temp_max += m_list_l[i]
            temp_min+=m_list_s[i]
            if p_count==100:
                if f_c==0:
                    f_list[j][0]=temp_max
                    g_list[j][0]=temp_min
                if f_c!=0:
                    f_list[j].append(temp_max)
                    g_list[j].append(temp_min)
                temp_max=0
                temp_min=0
                p_count=0
                j+=1

        f_c=1
        s_frame_no+=5
        e_frame_no+=5
    for i in range(0,48):
        f_list_l.append(ensem.round(f_list[i]))
        g_list_s.append(ensem.round(g_list[i]))
    for i in range(0,48):
        mod_max_list.append(ensem.most_Common(f_list_l[i]))
        mod_min_list.append(ensem.most_Common(g_list_s[i]))

    print f_list_l
    print mod_max_list
    #Writing gray values

    with open('gray_max.txt', 'w') as f1:
        for s in gray_sum_l_w:
            i=str(s)
            f1.write(i + '\n')
    f1.close()
    with open('gray_min.txt', 'w') as f2:
        for s in gray_sum_s_w:
            i=str(s)
            f2.write(i + '\n')
    f2.close()

    # #writing mod values
    with open('mod_max.txt', 'w') as f3:
        for s in mod_max_list:
            i=str(s)
            f3.write(i + '\n')
    f3.close()
    with open('mod_min.txt', 'w') as f4:
        for s in mod_min_list:
            i=str(s)
            f4.write(i + '\n')
    f4.close()

    end_time=time.time()
    elapsed = end_time - start_time
    print "Total time to execute pgm "+str(elapsed)

