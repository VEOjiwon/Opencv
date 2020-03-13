import cv2
import numpy as np
from cv2 import aruco
import time
#from robotarium import Robotarium, transformations
import csv
import datetime
%matplotlib inline


"""
Output value
if you want add the values in csv files
change the f_var=[] (type = str)
Option : id, time, x, y, seta

실험환경구성은 마커 오차측정.hwp 파일에서 확인가능.
사용 카메라 : 로지텍 c920
"""


#csv file open

title = "c2" #csv파일 제목 설정
f_var=["id","x","y"] #csv파일에 첨부할 변수 설정, all_var에 이쓴 변수로만 구성해야함.

all_var={"id":-1,"time":-1,"x":-1,"y":-1,"seta":-1}


#csv파일명 생성 코드
my_datetime = str(datetime.datetime.now())
gen_time = my_datetime[:-7].replace(":","-")
gen_time= gen_time[:19]+" "+title+'.csv'
pwd_f = 'C:/Users/Some/Desktop/e/output/'+gen_time
f = open(pwd_f, 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

#첫줄(변수명) 입력코드
wr.writerow(f_var)



#carmera calibration value
cameraMatrix=np.array([[1445.23344,0,950.82515],[0,1444.13649,  590.20015],[0,0,1]])
distCoeffs = (0.03406,  -0.11815,  0.00062,  0.00097)


#시간측정용 코드
time_m=[]



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


#값이 얼마나 변동하는지 확인하기 위한 변수
tem_x=[[],[],[],[],[],[],[], [],[],[],[]] # x좌표
tem_y=[[],[],[],[],[],[],[], [],[],[],[]] # y좌표
tem_theta=[[],[],[],[],[],[],[], [],[],[],[]] # theta
e_xy=[[],[],[],[],[],[],[], [],[],[],[]] #xy좌표 오류구하기
e_theta=[[],[],[],[],[],[],[], [],[],[],[]] # theta 에러 구하기



#capture the frame
while True:
    #time measure start point
    start = time.time()
    
    #image read
    ret, image = cap.read()
    
    
    
    #time measure end point & append  value
    time_m.append(time.time() - start)
    
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    
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
            #픽셀로 x,y 좌표를 구하는 코드이며 이 부분은 사용되지 않았고 대신 translation vector를 이용하였음.
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
            x=tvecs[i][0][0] * 100
            y=tvecs[i][0][1] * 100
            
           

           
            # save x,y,theta and error of x,y, theta
            # 마커 인덱스별로 오류구하는 코드
            # theta는 0도로 맞추고 실험하였으므로 빼줄필요가 없다.
            # 사용 마커 : 0~9번 마커 10번이상 마커 사용시 if문 추가 필요
            if idr == 0:
                tem_x[0].append(x)
                tem_y[0].append(y)
                e_xy[0].append(x)
                e_xy[0].append(y)
                tem_theta[0].append(abs(seta))
            elif idr == 1:
                tem_x[1].append(x)
                tem_y[1].append(y)
                e_xy[1].append(abs(abs(x)-abs(-50)))
                e_xy[1].append(y)
                tem_theta[1].append(abs(seta))
            elif idr == 2:
                tem_x[2].append(x)
                tem_y[2].append(y)
                e_xy[2].append(abs(abs(x)-abs(-100)))
                e_xy[2].append(y)
                tem_theta[2].append(abs(seta))
            elif idr == 3:
                tem_x[3].append(x)
                tem_y[3].append(y)
                e_xy[3].append(x)
                e_xy[3].append(abs(abs(y)-abs(-50)))
                tem_theta[3].append(abs(seta))
            elif idr == 4:
                tem_x[4].append(x)
                tem_y[4].append(y)
                e_xy[4].append(x)
                e_xy[4].append(abs(abs(y)-abs(-100)))
                tem_theta[4].append(abs(seta))
            elif idr == 5:
                tem_x[5].append(x)
                tem_y[5].append(y)
                e_xy[5].append(abs(abs(x)-abs(-50)))
                e_xy[5].append(abs(abs(y)-abs(-100)))
                tem_theta[5].append(abs(seta))
            elif idr == 6:
                tem_x[6].append(x)
                tem_y[6].append(y)
                e_xy[6].append(abs(abs(x)-abs(-100)))
                e_xy[6].append(abs(abs(y)-abs(-100)))
                tem_theta[6].append(abs(seta))
            elif idr == 7:
                tem_x[7].append(x)
                tem_y[7].append(y)
                e_xy[7].append(abs(abs(x)-abs(-100)))
                e_xy[7].append(abs(abs(y)-abs(-50)))
                tem_theta[7].append(abs(seta))
            elif idr == 8:
                tem_x[8].append(x)
                tem_y[8].append(y)
                e_xy[8].append(abs(abs(x)-abs(-50)))
                e_xy[8].append(abs(abs(y)-abs(-50)))
                tem_theta[8].append(abs(seta))
            """
            10개 이상의 마커로 실험시 코드 추가필요...
            elif idr == 9:
                tem_x[9].append(x)
                tem_y[9].append(y)
                tem_theta[9].append(seta)
            elif idr == 10:
                tem_x[10].append(x)
                tem_y[10].append(y)
                tem_theta[10].append(seta)
            """
            
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
            
            #append file
            s=[]
            for k in f_var:
                s.append(str(all_var[k]))

            wr.writerow(s)
           

    
    cv2.imshow("webcam",image)
    
    #실험시 반복횟수 설정
    if len(tem_x[8])==100:
        break
    
    #SHIFT + Q 혹은 Q로 종료
    #break the window
    if cv2.waitKey(1) % 0xFF == ord('q'):
        break

        
f.close()
cap.release()
cv2.destroyAllWindows()


#소요시간
import itertools
print("time")
print("평균 :",numpy.mean(time_m)) #평균
print("표준편차 : ", numpy.std(time_m)) # 표준편차
print("95percentile :", np.percentile(time_m, 95))#95
print("표본개수 :", len(time_m))


# 오차측정값 보기
total_xy = list(itertools.chain.from_iterable(e_xy))
total_theta = list(itertools.chain.from_iterable(tem_theta))
print("xy")
print("평균 :",numpy.mean(total_xy)) #평균
print("표준편차 : ", numpy.std(total_xy)) # 표준편차
print("95percentile :", np.percentile(total_xy, 95))#95
print("표본개수 :", len(total_xy))
print("")
print("Theta")
print("평균 :",numpy.mean(total_theta)) #평균
print("표준편차 : ", numpy.std(total_theta)) # 표준편차
print("95percentile :", np.percentile(total_theta, 95))
print("표본개수 :", len(total_theta))

#xy normal distribution
x = np.linspace(-20, 20, 10000) 
y = (1 / (np.sqrt(2 * np.pi)*numpy.std(total_xy))) * np.exp(- (x-numpy.mean(total_xy)) ** 2 / (2*numpy.std(total_xy)**2) )
import matplotlib.pyplot as plt
%matplotlib inline

plt.figure(figsize=(10, 6))          # 플롯 사이즈 지정
plt.plot(x, y)                       
plt.xlabel("x")                      # x축 레이블 지정
plt.ylabel("y")                      # y축 레이블 지정
plt.grid()                           # 플롯에 격자 보이기
plt.title("XY Normal Distribution")     # 타이틀 표시
#plt.legend(["N(0, 1)"])              # 범례 표시
plt.show()      

#theta normal distribution
x = np.linspace(-20, 20, 10000) 
y = (1 / (np.sqrt(2 * np.pi)*numpy.std(total_theta))) * np.exp(- (x-numpy.mean(total_theta)) ** 2 / (2*numpy.std(total_theta)**2) )
%matplotlib inline

plt.figure(figsize=(10, 6))          # 플롯 사이즈 지정
plt.plot(x, y)                       
plt.xlabel("x")                      # x축 레이블 지정
plt.ylabel("y")                      # y축 레이블 지정
plt.grid()                           # 플롯에 격자 보이기
plt.title("Theta Normal Distribution")     # 타이틀 표시
#plt.legend(["N(0, 1)"])              # 범례 표시
plt.show()      


# 각 마커별 값 보기
a=e_xy
for idx,i in enumerate(a):
    if i !=[]:
        print(idx,"번의 값은")
        print("평균 :",numpy.mean(i)) #평균
        #print(numpy.var(a)) #분산
        print("표준편차 : ", numpy.std(i)) # 표준편차
        print("95percentile :", np.percentile(i, 95)) #95

# 각 머커별 실제로 나온 값들 보기
#e_xy[4] -> 4번 마커의 에러의 실제값들 볼수있음...
#e_xy대신 tem_x, tem_y, tem_theta등을 넣으면 실제값을 볼수있음.
dd={}
for i in tem_x[8]:
    if i in dd:
        dd[i]=dd[i]+1
    else:
        dd[i] = 1
print(dd)