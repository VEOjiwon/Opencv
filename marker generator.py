import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import glob

#%matplotlib nbagg

"""
or use website : http://chev.me/arucogen/
"""

#딕셔너리 크기 설정
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

fig = plt.figure()
#몇 개 생성할것인지 가로 * 세로
nx = 3
ny = 4
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i, 2000)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

#저장경로 설정
plt.savefig("C:/Users/Some/Desktop/markers.pdf")
plt.show()