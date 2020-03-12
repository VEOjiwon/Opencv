import numpy as np
import cv2
from cv2 import aruco
import sys

cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)
cap2 = cv2.VideoCapture(cv2.CAP_DSHOW+1)

cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap2.set(cv2.CAP_PROP_AUTOFOCUS, 0)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


cameraMatrix=np.array([[1445.23344,0,950.82515],[0,1444.13649,  590.20015],[0,0,1]])
distCoeffs = (0.03406,  -0.11815,  0.00062,  0.00097)


arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

rotM = np.zeros(shape=(3,3))


while(True):
    
    ret,image = cap.read()
    ret2,image2 = cap2.read()
    
    
    #Aruco Marker detection
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image, arucoDict, parameters = parameters)
    corners2, ids2, rejectedImgPoints2 = aruco.detectMarkers(image2, arucoDict, parameters = parameters)
    
    #Draw the Makres image
    image = aruco.drawDetectedMarkers(image, corners, ids, borderColor=(0, 255, 0))
    image2 = aruco.drawDetectedMarkers(image2, corners2, ids2, borderColor=(0, 255, 0))
    
    rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, 0.1, cameraMatrix, distCoeffs)
    rvecs2, tvecs2, _objPoints2 = aruco.estimatePoseSingleMarkers(corners2, 0.1, cameraMatrix, distCoeffs)
    
  
    
    #find common markers
    common = []
    try:
        for index,value in enumerate(ids):
            for index2,value2 in enumerate(ids2):
                
                if value[0]==value2[0]:
                    common.append((index,index2,value[0]))
                    ids[index][0] = -1
                    ids2[index2][0] = -2
                    
    except:
        pass

    al = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[], 14:[],15:[],16:[],17:[],18:[],19:[],20:[]}
    
    #Object is detected by camera-0
    if ids is not None:
        for i in range(0,ids.size):
             #draw the each axis on screen
            if ids[i][0] >=0:  
                aruco.drawAxis(image, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.1 )
            
                #calculate seta
                cv2.Rodrigues(rvecs[i], rotM, jacobian = 0)
                ypr = cv2.RQDecomp3x3(rotM)
            
                #idr is robot's id
                idr = ids[i][0]
                x=tvecs[i][0][0] * 100
                y=tvecs[i][0][1] * 100

                seta = ypr[0][2]
                
                al[idr].append([x,y,seta])
                #print("dected camera 0 ",idr,x,y,seta)
            
    
    #Object is detected by camera-1
    if ids2 is not None:
        for i in range(0,ids2.size):
            #print(ids2)
            #draw the each axis on screen
            if ids2[i][0] >=0:
                aruco.drawAxis(image2, cameraMatrix, distCoeffs, rvecs2[i], tvecs2[i], 0.1 )
            
                #calculate seta
                cv2.Rodrigues(rvecs2[i], rotM, jacobian = 0)
                ypr = cv2.RQDecomp3x3(rotM)
            
                #idr is robot's id
                idr = ids2[i][0]

                #좌표계 통일
                x=tvecs2[i][0][0] * 100 -3.5
                y=tvecs2[i][0][1] * 100 -67
                seta = ypr[0][2]    
                
                al[idr].append([x,y,seta])
                
                #print("dected camera 1 ",idr,x,y,seta)
    
    #Object is detected by both cameras
    
    if common is not None and ids is not None and ids2 is not None:
        
        for i in common:
            """
            #공통분모 처리 부분
            #0번카메라 접근
            #ids[i[0]]
            #1번 카메라 접근
            #ids2[i[1]]
            x0, y0은 0번 카메라의 distortion값을 구하기 위한 픽셀값 변수
            x20, y20은 1번 카메라의 distortion값을 구하기 위한 픽셀값 변수
            x,y,x2,y2는 각 카메라 tvecs로부터 계산된 좌표값

            
            #common -> [(array1_idx, array2_idx, marker index),(array1_idx, array2_idx, marker index)... ]
            """
            
            
                
            #1번카메라 기준
            aruco.drawAxis(image, cameraMatrix, distCoeffs, rvecs[i[0]], tvecs[i[0]], 0.1 )
        
            #calculate seta
            cv2.Rodrigues(rvecs[i[0]], rotM, jacobian = 0)
            ypr = cv2.RQDecomp3x3(rotM)
            
          
            #idr is robot's id
            idr = i[2]
           
            x0=tvecs[i[0]][0][0] * 100
            y0=tvecs[i[0]][0][1] * 100
            seta = ypr[0][2]
            
            x = (corners[i[0]][0][0][0] + corners[i[0]][0][1][0] + corners[i[0]][0][2][0] + corners[i[0]][0][3][0]) / 4
            y = (corners[i[0]][0][0][1] + corners[i[0]][0][1][1] + corners[i[0]][0][2][1] + corners[i[0]][0][3][1]) / 4
            d = ((640-x)**2+(360-y)**2)**0.5
            z = d*0.1
            
            #2번카메라
            #aruco.drawAxis(image, cameraMatrix, distCoeffs, rvecs[i[0]], tvecs[i[0]], 0.1 )
            
            
            #calculate seta
            cv2.Rodrigues(rvecs2[i[1]], rotM, jacobian = 0)
            ypr2 = cv2.RQDecomp3x3(rotM)
            
          
            #idr is robot's id
            idr2 = i[2]
            
            x20=tvecs2[i[1]][0][0] * 100 -3.5
            y20=tvecs2[i[1]][0][1] * 100 -67
            seta2 = ypr2[0][2]
     
            x2 = (corners2[i[1]][0][0][0] + corners2[i[1]][0][1][0] + corners2[i[1]][0][2][0] + corners2[i[1]][0][3][0]) / 4
            y2 = (corners2[i[1]][0][0][1] + corners2[i[1]][0][1][1] + corners2[i[1]][0][2][1] + corners2[i[1]][0][3][1]) / 4
            d2 = ((640-x2)**2+(360-y2)**2)**0.5
            z2 = d2*0.1
          
           
            w = z2/(z+z2)
              
            #weight가 곱해진 x,y좌표
            x_f = (w*x0 + (1-w)*x20)
            y_f = (w*y0 + (1-w)*y20)
            
            al[idr].append([x0,x20,x_f,(x0+x20)/2])
            
            #print(idr,w,x0,x20,x_f,y0,y20,y_f)
            
            #print("both id: ",idr,"\n (",x, ", ",y, ", ", seta, ")\n","(",x2, ", ",y2,", ",seta,")\n x_f :", x_f,"\n y_f : ", y_f )
            #print("id : ", idr, "x의 비 : ",abs(abs(x_f)-abs(x))/abs(abs(x_f)-abs(x2)), "y의 비 :",abs(abs(y_f)-abs(y))/abs(abs(y_f)-abs(y2))   )
            #print(idr, tvecs[i[0]][0][2],tvecs[i[1]][0][2])
        
    #print(al)
    cv2.imshow('frame',image)
    cv2.imshow('frame2',image2)
    
    #cv2.resizeWindow('Video Out', 1920, 1536)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()