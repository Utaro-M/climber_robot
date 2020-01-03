#!/usr/bin/env python
# -*- coding: utf-8 -*-

#同じ形のものであればnum個までの距離
#青の球を用いた

import cv2
import numpy as np
import math
from sklearn.cluster import KMeans
import rospy
# from ros_start.msg import steps
# from ros_start.msg import step
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
#検出したいものの個数


#色を検出　maskする
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

def publisher(n_cluster,step):

    rospy.init_node('color_tracking')
    pub=rospy.Publisher('steps_info',PoseArray , queue_size=10)
    #rate=rospy.Rate(10)
    #rospy.sleep(1)

    #while not rospy.is_shuttdown():
    steps_tmp=PoseArray()
    steps_tmp.header.stamp=rospy.Time.now()

    for i in range(n_cluster):
        step_tmp=Pose()
        step_tmp.position.x=step[i].dist #xをdistに対応させる
        step_tmp.position.y=step[i].width #yをwidthに対応させる
        step_tmp.position.z=step[i].height #zをheightに対応させる
        steps_tmp.poses.append(step_tmp)

    pub.publish(steps_tmp)


class cluster:
    def __init__(self):
        self.X=[]
        self.Y=[]
        self.Z=[]
        self.width=0
        self.height=0
        self.dist=0


def main():



    num=2
    n_cluster=2
    depth=250
    threshold_size=200
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
    X=np.ones(num)
    Y=np.ones(num)
    Z=np.ones(num)
    # X=[1]*num
    # Y=[1]*num
    # Z=[1]*num

    # init=cluster()
    # step=[init]*(n_cluster)


    while(cap.isOpened()):
        ret,frame=cap.read()
        print(frame)

        mask1=color_detect(frame)
        mask2=mask1
        #輪郭
        _,contours, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        #contoursの内大きさの上位num個のもののインデクス
        index=sort_index(contours,num)

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

                if(M1["m00"] >  threshold_size):
                    cx[j],cy[j] = int(M1["m10"]/M1["m00"]),int(M1["m01"]/M1["m00"])
                    print("M1 = {}".format(M1["m00"]))
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
        print("Z={}".format(Z))
        if(X[X != 0].shape[0] >=2):
            flag_empty = 0
        else:
            flag_empty = 1

        dif_y=abs(np.max(Y)-np.min(Y))
        dif_z=abs(np.max(Z)-np.min(Z))


        if( dif_z < (depth*1) ):
            n_cluster=1
        elif( dif_z < ((depth*2))):
            n_cluster=2
        elif(dif_z < (depth*3)):
            # n_cluster=3 errorが出て面倒なのでとりあえず２にした
            n_cluster=2

        init=cluster()
        step=[init]*(n_cluster)

        if(flag_empty==1):
            step[0].width=0
            step[0].height=0
            step[0].dist=0
            print("nothing was detected")

        else:
            if(n_cluster==1):
                pred=np.zeros(num)
                #pred=[0]*num
                print(X[pred==0])

            #     step[0].width=np.max(step[0].X)-np.min(step[0].X)
            #     step[0].height=np.max(step[0].Y)-np.min(step[0].Y)
            #     step[0].dist=np.mean(step[0].Z)
            else:
                pred=KMeans(n_cluster).fit_predict(Z.reshape(num,1))
                # init=cluster()
                # step=[init]*n_cluster

            for i in range(n_cluster):
                for j in range(X[pred==i].shape[0]):
                    step[i].X.append(X[pred==i][j])
                    step[i].Y.append(Y[pred==i][j])
                    step[i].Z.append(Z[pred==i][j])


            #IndexError: too many indices for array
            # for i in range(n_cluster):
            #     step[i].X=X[pred==i]
            #     step[i].Y=Y[pred==i]
            #     step[i].Z=Z[pred==i]
                if(len(step[i].X) >= 2):

                    step[i].width=np.max(step[i].X)-np.min(step[i].X)
                    step[i].height=np.max(step[i].Y)-np.min(step[i].Y)
                    step[i].dist=np.mean(step[i].Z)
                else:
                    # step[i].width=
                    # step[i].height=
                    step[i].dist=np.mean(step[i].Z)

                print("dist[{}]={}".format(i,step[i].dist))
                print("width[{}]={}".format(i,step[i].width))




        # print("X={}".format(X.tolist()))
        # print("Y={}".format(Y.tolist()))
        # print("Z={}".format(Z.tolist()))


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

        #publisher
        publisher(n_cluster,step)

        if cv2.waitKey(25) & 0xFF ==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException :pass
