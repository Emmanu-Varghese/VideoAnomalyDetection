import cv2

import time

import ensem
import pyttsx

import datetime
from twilio.rest import TwilioRestClient



def anomaly_run(path):
    # initialize the first frame in the video stream
    firstFrame = None
    #########################

    # to_no = "+918547073500"
    

    # msg="Abnormaly Detected"
    # account='ACb1b0ea4fd0015b8603516337d996eb8d'
    # token='5cc96c2264969a1497153f925774ad3a'
    # client=TwilioRestClient(account,token)
    
    #########################

    count=0
    v_count=0
    if count==0:
        ensem.clear_folder()
    #creating video capture object
    #capture=cv2.VideoCapture(0)
    engine = pyttsx.init()
    #Set the resolution of capturing to 640W*480H
    #capture.set(3,640)
    #capture.set(4,480)
    frame_time_set=[]
    frame_set=[]
    start_time=time.time()
    s_frame_no=0
    e_frame_no=100
    ensemble_final_set=[]
    pack_count=0
    pack_count_c = 0
    pack_max_count=143
    mod_max_list=[[x] for x in range(0,48)]
    mod_min_list=[[x] for x in range(0,48)]
    f_c=0
    stay_count=0
    one_time_set=0

    cap = cv2.VideoCapture(path)

    ## Only when reading from video file ##
    while not cap.isOpened():
        cap = cv2.VideoCapture(path)
        cv2.waitKey(1000)
        print "Wait for the header"

    pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)

    with open('gray_max.txt', 'r') as f1:
        upper = [line.rstrip('\n') for line in f1]
    upper = map(float, upper)
    with open('gray_min.txt', 'r') as f2:
        lower = [line.rstrip('\n') for line in f2]
    lower = map(float, lower)

    with open('mod_max.txt', 'r') as f3:
        mod_upper = [line.rstrip('\n') for line in f3]
    mod_upper = map(float, mod_upper)
    with open('mod_min.txt', 'r') as f4:
        mod_lower = [line.rstrip('\n') for line in f4]
    mod_lower = map(float, mod_lower)

    while(True):
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = cap.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # resize the frame, convert it to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            # (x, y, w, h) = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if cv2.contourArea(c) < 2000:
                if pack_count_c > pack_max_count:
                        v_count+=1
                        if v_count > 20:
                            pack_count_c = 0
                            v_count=0
                continue
                        
            if pack_count_c > pack_max_count:
                    text="Person is not leaving:-Anomaly"
                    v_count=0
                    
            else:
                    text = "Busy"
                    v_count=0

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        ensemble_set=[]
        re_list=[]

        ## Real time only ##

        # count = count + 1
        # # Converting to Gray Scale
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame_time_set.append(gray)
        # frame_set.append(gray)
        # # Display the resulting frame
        # cv2.imshow('frame', gray)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        ## When reading from video file ##

        if grabbed:
            count=count+1
            # Converting to Gray Scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_time_set.append(gray)
            frame_set.append(gray)
            # Display the resulting frame
            (h, w) = gray.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            rotated = cv2.warpAffine(gray, M, (w, h))
            cv2.imshow('frame',gray)
            pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            print str(pos_frame) + " frames"
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


        if(len(frame_time_set)==5):
            frame_time=time.time()
            time_duration=frame_time-start_time

        if(len(frame_set)==5):
            pack_count+=1
            pack_count_c+=1
            print pack_count
            flag=0
            m_flag=0
            v_flag=0
            re_list=ensem.process_frames(frame_set,5,time_duration)
            g_max=re_list[0]
            g_min=re_list[1]
            frame_set=[]
            upper_thresh=0
            p_count=0
            temp_max=0
            temp_min=0
            j=0
            for i in range(0,4800):
                p_count+=1
                temp_max+=g_max[i]
                temp_min+=g_min[i]
                if p_count==100:
                    if f_c==0:
                        mod_max_list[j][0]=temp_max
                        mod_min_list[j][0]=temp_min
                    if f_c!=0:
                        mod_max_list[j].append(temp_max)
                        mod_min_list[j].append(temp_min)
                    temp_max=0
                    temp_min=0
                    p_count=0
                    j+=1
            f_c=1

            vol_count=0
            for i in range(0,4800):
                vol_count+=1
                if g_max[i] > upper[i]+500:
                    v_flag=v_flag+1
                if g_min[i] < lower[i]-500:
                    v_flag=v_flag+1
                if vol_count==100:
                    if v_flag >=40:
                        flag+=1
                    vol_count=0
                    v_flag=0
            print "violated flag cout is "
            print flag
            if flag > 5:
                if flag >15:
                    print "Abnormaly by the presence of two persons"
                if flag < 15:
                    print "Abnormaly by Single person"
                name = "abnormal_frames\\frame%d.jpg"%count
                cv2.imwrite(name, frame)
                print flag
                print "Abnormaly"
                engine.say("Abnormaly")
                #client.messages.create(from_="+13473942587",to=to_no,body=msg)
                engine.runAndWait()


        if pack_count==pack_max_count:
            print "reached max pack count"
            one_time_set=1
            temp_mod_max_list=[]
            temp_mod_min_list=[]
            for i in range(0,48):
                temp_mod_max_list.append(ensem.stat_range(mod_max_list[i]))
                temp_mod_min_list.append(ensem.stat_range(mod_min_list[i]))
            for i in range(0,48):
                if temp_mod_max_list[i] > (mod_upper[i]+(mod_upper[i]*0.25)):
                    print i
                    print "max"
                    print temp_mod_max_list[i]
                    m_flag+=1
                if temp_mod_min_list[i] < (mod_lower[i]-(mod_lower[i]*0.25)):
                    print i
                    print "min"
                    print temp_mod_min_list[i]
                    m_flag+=1
            print "flags violated "+ str(m_flag)
            if m_flag >6:
                print "Abnormaly by mod"
                engine.say("Abnormaly by mod")
                engine.runAndWait()
            print temp_mod_max_list
            mod_max_list=[[x] for x in range(0,48)]
            mod_min_list=[[x] for x in range(0,48)]
            f_c=0
            m_flag=0
            pack_count=0
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

