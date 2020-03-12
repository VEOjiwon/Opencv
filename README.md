 # Opencv - Localization
Arucomarker를 이용하여 단일 및 더블 카메라에서 마커 위치 및 각도 측정을 위한 코드입니다.

## 1. Getting Started
### Installation
1. python 3.7.6
2. Open cv
3. numpy
4. MATLAB calibration tool or GMLCarmeracalibration (카메라 캘리브레이션용)

### Environment
1. 로지텍 c920웹캠
2. 책상높이 72cm, 책상 ~ 카메라 높이 : 188cm
3. Aruco Marker Dict 4*4, 10cm크기 마커사용 

referencephoto 폴더 참조바랍니다.


## 2. How to use
### 1. Calibration
매트랩 혹은 GMLCalibration을 이용한다.
자세한 사용방법은

matlab : http://www.vision.caltech.edu/bouguetj/calib_doc/

GMLCalibration : http://graphics.cs.msu.ru/en/node/911

open cv의 calibration 관련 문서는 https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html

칼리브레이션시 오차범위가 발생한다 이를 줄이기 위해 calibration_combination_calculator.py파일을 이용하여 오차범위 내에서 distCoeffs을 조합하여 오류를 줄이고자 하였으나 특정상황에만 맞게 overfitting되는 경향 및 콤비네이션 특성상 시간 복잡도가 n^4까지 가는 등의 문제점이 있어서 실제로 적용하지는 못하였다.


### 2. CreateMarker
marker generator.py파일을 이용하거나

http://chev.me/arucogen/

에서 손쉽게 만들 수 있다


### 3. 단일카메라
uni_cam_csv_measure.py 파일, 단일카메라로 마커의 x,y, theta측정 및 csv파일 생성하기 그리고 성능측정과 관련된 코드들이 있다.

### 4. 멀티카메라
multicarmera.py 파일, 2대의 카메라를 이용해서 마커 위치를 구하는 코드이다.

겹치는 영역을 만들어 그 구역내에서는 distortion값을 이용해 w(가중치)를 구하여 좌표를 보정하도록 하였다.

여기서 distortion값은 각각의 카메라로 부터 마커까지의 거리, w는 w = (1/d1)/((1/d1)+(1/d2))를 사용하였다.



## Contact
E-mail : top9076@naver.com

