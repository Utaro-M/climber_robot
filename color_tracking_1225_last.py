#!/usr/bin/env python
# -*- coding: utf-8 -*-

#同じ形のものであればnum個までの距離
#青の球を用いた

import cv2
import numpy as np
import math

#検出したいものの個数
num=2


def color_detect(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV) #256段階

    #値域 #青を検出してる
    hsv_min=np.array([0,127,0])
    hsv_max=np.array([30,255,255])

    mask1=cv2.inRange(hsv,hsv_min,hsv_max)

    #値域　青
    hsv_min=np.array([150,127,0])
    hsv_max=np.array([179,255,255])
    # #青を検出してる
    # hsv_min=np.array([200,127,0])
    # hsv_max=np.array([256,255,255])

    mask2=cv2.inRange(hsv,hsv_min,hsv_max)

    return mask1+mask2

#max_index
def index_emax(cnt):
    max_num = 0

    max_i = -1

    for i in range(len(cnt)):
        cnt_num=len(cnt[i])
        if cnt_num > max_num:

            max_num = cnt_num

            max_i = i

    return max_i

#multi_index 大きいもの上位num個を検出する、num個のindexを返す
#要素の長さについて　バブルソート
def sort_index(cnt,num):
    max_num=0
    index=[-1]*num
    #　バブルソート
    for i in range(len(cnt)):
        cnt_num=len(cnt[i])
        if (cnt_num > max_num):
            max_num=cnt_num
            #num個のインデクスをスライドする
            for j in range(num-1):
                index[num-1-j]=index[num-1-j-1]
            index[0]=i
    #print(index)
    return index


def main():

    #基準距離
    h1=300
    #距離を測りたいものの高さ
    H=63
    #測りたいものを基準距離の位置においたときの画面上で得られる測りたいものの高さ　initializeファイルを実行
    L1=110


    cap=cv2.VideoCapture(0)

    #画面上の位置
    cx=[320]*num
    cy=[240]*num
    #実際の位置
    X=[1]*num
    Y=[1]*num
    Z=[1]*num

    while(cap.isOpened()):
        ret,frame=cap.read()

        mask1=color_detect(frame)
        mask2=mask1
        #輪郭
        _,contours, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        #contoursの内大きさの上位num個のもののインデクス
        index=sort_index(contours,2)

        mask2[:]=0
        #x,y,Xなどのためのインデクス
        j=0


        for i in index:

            if(i != -1):
                approx = cv2.convexHull(contours[i])

                #mask等に書き込み
                cv2.drawContours(mask2,[approx],0,(255),-1) #source,輪郭、輪郭のインデクス、色、太さ
                cv2.drawContours(frame,[approx],0,(0,200,0),3)

                #moment
                M1=cv2.moments(contours[i])
                if(M1["m00"] != 0):
                    cx[j],cy[j] = int(M1["m10"]/M1["m00"]),int(M1["m01"]/M1["m00"])

                #print(cx[j],cy[j])

                #重心の高さ
                mask = cv2.bitwise_and(mask1,mask1,mask=mask2)
                mask = cv2.Canny(mask2,100,200)
                y,x = np.where(mask == 255)


                if len(y)!= 0:
                    # 対象物体の画像上の高さh2を計算
                    ymax,ymin = np.amax(y),np.amin(y)
                    h2 = ymax - ymin
                    if(h2 !=0):
                        # 奥行きL2を計算
                        L2 = (h1/float(h2))*L1
                        # 1px当たりの大きさを計算
                        a = H/float(h2)
                        # 三次元位置（X, Y, Z）を計算
                        X[j] = (cx[j]-320)*a
                        Y[j] = (ymax-cy[j])*a

                        if L2 > X[j]:
                                Z[j] = math.sqrt(L2*L2-X[j]*X[j])
                        X[j],Y[j],Z[j],L2 = round(X[j]),round(Y[j]),round(Z[j]),round(L2)

                    j+=1

        print("X={}".format(X))
        print("Y={}".format(Y))
        print("Z={}".format(Z))

#frame 検出部を曲線で囲む　Mask1　検出部が白く表示される
        cv2.namedWindow("Frame",)
        cv2.imshow("Frame",frame)
        cv2.moveWindow("Frame",1000,0)
        cv2.imshow("Mask1",mask1)
        cv2.imshow("Mask1",mask1)
        cv2.moveWindow("Mask1",1000,1000)
        cv2.imshow("Mask2",mask2)
        cv2.imshow("Mask2",mask2)
        cv2.moveWindow("Mask2",100,1000)

        if cv2.waitKey(25) & 0xFF ==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
