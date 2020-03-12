import cv2
import numpy as np
from cv2 import aruco
import time
from robotarium import Robotarium, transformations
import csv
import datetime
%matplotlib inline


"""
Output value
if you want add the values in csv files
change the f_var=[] (type = str)
Option : id, time, x, y, seta
"""


#csv file open

title = "calibration_20_tvecs"

f_var=["error","coeffs"]

my_datetime = str(datetime.datetime.now())
gen_time = my_datetime[:-7].replace(":","-")
gen_time= gen_time[:19]+" "+title+'.csv'
pwd_f = 'C:/Users/Some/Desktop/e/output/'+gen_time
f = open(pwd_f, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)


wr.writerow(f_var)




#실제 마커위치
actual = [88.38,62.5,88.38,65.5,88.38,62.5,88.38,65.5]

cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)


#original frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#kill auto focus
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)


#aruco dict
arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()


#초기값
cameraMatrix=np.array([[1465.606,0,1001.568],[0,1463.048,  546.350],[0,0,1]])
distCoeffs = ( -0.005900,  -0.109335,  -0.000557,  0.011914)

#cameraMatrix=np.array([[1465.606,0,1001.568],[0,1463.048,  546.350],[0,0,1]])
#distCoeffs =( -0.038530999999999996, -0.500998, -0.003908, 0.0017758000000000001)

#cameraMatrix=np.array([[1465.606,0,1001.568],[0,1463.048,  546.350],[0,0,1]])
#distCoeffs =(-0.038530999999999996, -0.18779800000000008, -0.003236, -0.0005570000000000002)


#cap.release()
        #cv2.destroyAllWindows()
    #break
#image read

#start combination cal.
for a in range(0,20):
    print(a)
    for j in range(0,20):
        for k in range(0,20):
            for d in range(0,20):
                #첫번째 20단위로 실행시
                
                distCoefss = (-0.060285+a*0.0054385, -0.500998+j*0.03915, -0.003908+k*0.000336,-0.004445+d*0.0003888)
                #두번째
                #distCoeffs =(-0.0396187 + (a*0.0010877), -0.195628+ (j*0.00783), -0.0035172+ (k * 0.000672), -0.00063476+(d * 0.0000777))
                
                while(True):
                    ret, image = cap.read()
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    corners, ids, rejectedImgPoints = aruco.detectMarkers(image=image, dictionary=arucoDict, cameraMatrix=cameraMatrix, distCoeff=distCoeffs, parameters = parameters)
                    rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, 0.06, cameraMatrix, distCoeffs)
                    if ids.size == 9:
                            
                       

                        temp = [(),(),(),(),(),(),(),(),()]
                        
                        for i in range(0,ids.size):
             
        
                            idr = ids[i][0]  
        
        
                            #x = (corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][0]) / 4
                            #y = (corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][1]) / 4
            
            
                            
          
        
                            #x=x/5
                            #y=y/5
                
                            x=tvecs[i][0][0] * 100
                            y=tvecs[i][0][1] * 100
                            
                            temp[idr]=(x,y)

                        out=[]
                        
                        error=[]
                        #print(temp[0])
                        for i in range(0,8):
                             error.append((((temp[8][0]-temp[i][0])**2+(temp[8][1]-temp[i][1])**2)**0.5-actual[i])**2)
                        out.append(sum(error))
                        out.append(distCoeffs)
                        #print(error)
                        #print(out)
                        wr.writerow(out)
                        break
                    else:
                        print("not detected")
                    
  



"""
if len(ids) == 9:
        #cap.release()
        #cv2.destroyAllWindows()
    break
"""
print("end")
f.close()