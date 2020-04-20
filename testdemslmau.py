import numpy as np
import cv2
import Person
import time
cnt_red = 0
cap = cv2.VideoCapture(0)
w = cap.get(3)
h = cap.get(4)
frameArea = h * w
areaTH = frameArea/250
line_up = int(3*(h/6))
line_down = int(3*(h/6))

up_limit =   int(1*(h/5))
down_limit = int(4*(h/5))

font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while(cap.isOpened()):
            
    # -- Read an image of the video source --
    ret, frame = cap.read()
    
    # -- age every person one frame --
    
        
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # -- Binarization to eliminate shadows -- (Gray)
    try:
        
        red_lower = np.array([125, 95, 145], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        
        red = cv2.inRange(hsv, red_lower, red_upper)
        red = cv2.dilate(red, kernelOp2)
        
        
       
    except:
        
        print('so luong', cnt_red)
        
        
    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    #_, contours0, hierarchy = cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours0, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            
            # -- Tracking --    
            
            # -- Need to add conditions for multipersons, outputs and screen inputs ---
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        
                        # -- The object is near one that is already detected before --
                        new = False
                       
                        # -- actualiza coordinates in object and resets age --
                        i.updateCoords(cx,cy)   
                        
                        if i.going_DOWN(line_down,line_up) == True:
                            cnt_red += 1;
                            print ("ID:",i.getId(),'Vat mau do dang di xuong',time.strftime("%c"))
                        break
                    
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        
                    if i.timedOut():
                        # -- Remove I from the persons list --
                        index = persons.index(i)
                        persons.pop(index)
                        del i     # -- Release the memory of I --
                if new == True:
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1     

            cv2.circle(frame,(cx,cy), 7, (0,0,255), -1)        
    for i in persons:
        if len(i.getTracks()) >= 2:
            cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.6,i.getRGB(),2)
     
    red_down = 'MAU DO : ' + str(cnt_red) 
    cv2.putText(frame, red_down ,(30,60),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,255),1)
    cv2.imshow('Frame', frame)   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
