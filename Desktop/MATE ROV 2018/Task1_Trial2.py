#https://github.com/HUANGManutea/shapeDetection/blob/master/shapeDetect.py
#IMP_IDEA
#https://www.youtube.com/watch?v=IXyO2O-I2bs

#THIS IS THE NEW VERSION
import cv2
import numpy as np
import math
cap=cv2.VideoCapture(0)
# If use an image, then not infinite loop and also use imread instead of Frame


def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)
    
scale=2

#HSV better than RGB, Each value in HSV are format, but in RGB these are dependent. V- Color Value, S - Satuation like intensity and H - hue -This dictates the color
# This function are responsible for filtering colour
lower_red=np.array([150,150,0])
upper_red=np.array([180,255,255])

# You can apply filters which literally just blurs the images, thus ignoring any distrurbances
lower_blue=np.array([100,150,0])
upper_blue=np.array([140,255,255])

lower_yellow=np.array([20, 100, 100])
upper_yellow=np.array([30, 255, 255])

def changeFrameColour(lower_value,upper_value):
    mask=cv2.inRange(hsv,lower_value,upper_value)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    median_value=cv2.medianBlur(res,15)
    return median_value
    
def areaCalculate(median_value):
    edges=cv2.Canny(median_value,100,200)
    canny2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for plc,contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if area>300:
           # print("YESYESYES")
            return 1
        else:
            return 2

def shapeIdentifier(median_value,name_tri,name_rectangle):
        edges=cv2.Canny(median_value,100,200) # CHANGE THE 'FRAME' TO 'RES' FOR THE ORIGINAL CODE
        canny2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #
        for i in range(0,len(contours)):
    
            #approximate the contour with accuracy proportional to
            #the contour perimeter
            approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)
    
            #Skip small or non-convex objects
            if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                continue
    
            #triangle
            if(len(approx) == 3):
                x,y,w,h = cv2.boundingRect(contours[i])
                cv2.putText(frame,name_tri,(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            elif(len(approx)>=4 and len(approx)<=6):
                #nb vertices of a polygonal curve
                vtc = len(approx)
                #get cos of all corners
                cos = []
                for j in range(2,vtc+1):
                    cos.append(angle(approx[j%vtc],approx[j-2],approx[j-1]))
                #sort ascending cos
                cos.sort()
                #get lowest and highest
                mincos = cos[0]
                maxcos = cos[-1]
    
                #Use the degrees obtained above and the number of vertices
                #to determine the shape of the contour
                x,y,w,h = cv2.boundingRect(contours[i])
                if(vtc==4):
                    cv2.putText(frame,name_rectangle,(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                    #cv2.line(frame,'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    #            elif(vtc==5):
    #                cv2.putText(median,'PENTA',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
    #            elif(vtc==6):
    #                cv2.putText(median,'HEXA',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
            else:
                #detect and label circle
                area = cv2.contourArea(contours[i])
                x,y,w,h = cv2.boundingRect(contours[i])
                radius = w/2
    #            if(abs(1 - (float(w)/h))<=2 and abs(1-(area/(math.pi*radius*radius)))<=0.2):
    #                cv2.putText(median,'CIRC',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA) 
     

while True:
    _,frame=cap.read() #'_' is a value returned to this function, but we don't care about that value
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    median_red=changeFrameColour(lower_red,upper_red)
    area_red=areaCalculate(median_red)
    
    median_blue=changeFrameColour(lower_blue,upper_blue)
    area_blue=areaCalculate(median_blue)
    
    median_yellow=changeFrameColour(lower_yellow,upper_yellow)
    area_yellow=areaCalculate(median_yellow)
    
    #Using elif instead of multiple If's as the program should detect only one colour at a time
    if(area_red==1): #MAKE THE CONDITION THAT ONLY DETECT ONE COLOUR  AT TIME , X==1 AND Y!=1 AND Z!=1
        cv2.imshow('median',median_red)
        median_value=median_red
        shapeIdentifier(median_value,'TRI_R','RECT_R')
    elif(area_blue==1):
        cv2.imshow('median',median_blue)
        median_value=median_blue
        shapeIdentifier(median_value,'TRI_B','RECT_B')
    elif(area_yellow==1):
        cv2.imshow('median',median_yellow)
        median_value=median_yellow
        shapeIdentifier(median_value,'TRI_Y','RECT_Y')
    else:
        print('NO TAIL DETECTED')

    #edges=cv2.Canny(median_value,100,200)
    #print()
    #print(median_yellow)
#    if(area_red==1 or area_blue==1 or area_yellow==1):
#        print("we")
#        shapeIdentifier(median_value,'TRI_Y','RECT_Y')
        
#    kernel=np.ones((15,15),np.float32)/(15*15)
#    smooth=cv2.filter2D(res,-1,kernel)
    
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('smooth',smooth)
    #cv2.imshow('egdes',edges)
    
    k=cv2.waitKey(5) & 0xFF
    if k==27:
        break
    
cv2.destroyAllWindows()
cap.release()
