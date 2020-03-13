import cv2
import numpy as np
from cv2 import aruco
import time
#from robotarium import Robotarium, transformations
import csv
import datetime
%matplotlib inline


"""
마커를 인식해서 id, 기록시간, x, y, theta를 csv파일에 기록해주는 코드입니다.
csv파일과 관련된 옵션은 파일제목, 입력하고싶은 변수 설정, 저장경로 등을 설정해줄수 있습니다.
파일제목은 '생성시간 + 주어진 파일제목' 으로 생성됩니다.
자세한건 코드상의 주석을 참고하시기 바랍니다.


실험환경구성은 마커 오차측정.hwp 파일에서 확인가능.
사용 카메라 : 로지텍 c920
"""


#csv file open

title = "exp1" #csv파일 제목 설정
f_var=["id","time","x","y","seta"] #csv파일에 첨부할 변수 설정, all_var에 있는 변수로만 구성해야함.

all_var={"id":-1,"time":-1,"x":-1,"y":-1,"seta":-1}


#csv파일명 생성 코드
my_datetime = str(datetime.datetime.now())
gen_time = my_datetime[:-7].replace(":","-")
gen_time= gen_time[:19]+" "+title+'.csv'
pwd_f = 'C:/Users/Some/Desktop/e/output/'+gen_time #경로설정
f = open(pwd_f, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

#첫줄(변수명) 입력코드
wr.writerow(f_var)


#carmera calibration value
cameraMatrix=np.array([[1445.23344,0,950.82515],[0,1444.13649,  590.20015],[0,0,1]])
distCoeffs = (0.03406,  -0.11815,  0.00062,  0.00097)


cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)


#set original frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)


#kill auto focus
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)


#aruco dict 생성
arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50) # 4 X 4 마커
parameters = aruco.DetectorParameters_create() # 파라미터 생성


# for r vector cal.
rotM = np.zeros(shape=(3,3))


#capture the frame
while True:
    #time measure start point
    start = time.time()
    
    #image read
    ret, image = cap.read()
    
    
    #Aruco Marker detection
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image=image, dictionary=arucoDict, cameraMatrix=cameraMatrix, distCoeff=distCoeffs, parameters = parameters)
   

    #Draw the Makres image
    image = aruco.drawDetectedMarkers(image, corners, ids, borderColor=(0, 255, 0))
   
    #estimate posestion
    #second parameter is the length of the marker's size (unit is meters)
    #it affect translation and rotation vectors
    rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, 0.1, cameraMatrix, distCoeffs) 
 
    
    
    if ids is not None:
        for i in range(0,ids.size):
             #draw the each axis on screen
            aruco.drawAxis(image, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.1 )
            """
            #픽셀로 x,y 좌표를 구하는 코드이며 이 부분은 사용되지 않았고 대신 translation vector를 이용하였습니다.
            #기록의 이유로 코드는 남겨놓습니다.
            #calculate center coordinates
            #x = (corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][0]) / 4
            #y = (corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][1]) / 4
            
            #pixel scaling 카메라 ~ 마커사이거리 188cm 
            #1k
            #x=x/5
            #y=y/5
            
            #4k
            #x=x/4
            #y=y/4
            
            #카메라 수선의 발(중심)으로부터 거리 구하는 식 -> multicarmera를 위한 변수
            #d = ((640-x)**2+(360-y)**2)**0.5
            """
            
            #calculate seta
            cv2.Rodrigues(rvecs[i], rotM, jacobian = 0)
            ypr = cv2.RQDecomp3x3(rotM)
            seta = ypr[0][2]
            
            
            #idr is marker's id
            idr = ids[i][0]
            
            
            #usinig tvecs
            x=tvecs[i][0][0] * 100 #m -> cm 단위변화를 위해 *100
            y=tvecs[i][0][1] * 100
            
           
            #csv파일에 기록할 시간 받아오는 코드
            my_datetime = datetime.datetime.now()
            new_datetime = str(my_datetime + datetime.timedelta(milliseconds=1))
            new_datetime = new_datetime[14:-4]
            
            #update dict for csv
            all_var["id"] = idr
            all_var["time"] = new_datetime
            all_var["x"] = x
            all_var["y"] = y
            all_var["seta"] = seta
            
            print(idr, x,y,seta)
            
            #append file
            s=[]
            for k in f_var:
                s.append(str(all_var[k]))

            wr.writerow(s)
           

  
    cv2.imshow("webcam",image)
 
    #break the window
    if cv2.waitKey(1) % 0xFF == ord('q'):
        break

        
f.close()
cap.release()
cv2.destroyAllWindows()
