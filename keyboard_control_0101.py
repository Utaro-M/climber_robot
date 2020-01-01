#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time			# time.sleepを使いたいので
#import pygame		# pygameでジョイスティックを読む
import sys
import serial
import readchar
#ser=serial.Serial('/dev/ttyACM0',9600)
ser=serial.Serial("COM5",9600)
#ser=serial.Serial("COM3",9600)

def main():
    time.sleep(0.5)		# 通信が安定するまでちょっと待つ
    #Ctrl+cが押されるまでループ
    #print("OK")
    #inp=''
    try :
        flag=0
        while True:
            # inp=input()
            inp =readchar.readchar()
            #print(inp)
            #sys.stdout.write(inp)
            str_ = ""
            if(inp=='y'):
                flag=1
                str_="Forward"
                ser.write('f'.encode())
            elif(inp=='b'):
                flag=1
                str_="Back"
                ser.write('b'.encode())
            elif(inp=='u'):
                flag=1
                str_="Both Up"
                ser.write('y'.encode())

            elif(inp=='h'):
            	flag=1
            	str_="Both Down"
            	ser.write('h'.encode())

            elif(inp=='i'):

            	flag=1
            	str_="Right Up"
            	ser.write('r'.encode())

            elif(inp=='n'):
            	flag=1
            	str_="Right Down"
            	ser.write('a'.encode())

            elif(inp=='r'):

            	flag=1
            	str_="Left Up"  #r_rotate_reverse
            	ser.write('l'.encode())

            elif(inp=='v'):
            	flag=1
            	str_="Left Down"  #l_rotate_reverse
            	ser.write('b'.encode())

    		# if(R1==1 and L1==1):
    		# 	if(arm_up_down>50):
    		# 		flag=1
    		# 		str_="Both Up"
    		# 		ser.write('y'.encode())
    		# 	elif(arm_up_down<-50):
    		# 		flag=1
    		# 		str_="Both Down"
    		# 		ser.write('h	'.encode())
    		# elif(R1==1 ):
    		# 	if(arm_up_down>50):
    		# 		flag=1
    		# 		str_="Right Up"
    		# 		ser.write('r'.encode())
    		# 	elif(arm_up_down<-50):
    		# 		flag=1
    		# 		str_="Right Down"
    		# 		ser.write('a'.encode())
    		# elif(L1==1):
    		# 	if(arm_up_down>50):
    		# 		flag=1
    		# 		str_="Left Up"  #r_rotate_reverse
    		# 		ser.write('l'.encode())
    		# 	elif(arm_up_down<-50):
    		# 		flag=1
    		# 		str_="Left Down"  #l_rotate_reverse
    		# 		ser.write('b'.encode())

            elif(inp=='t'):
            	flag=1
            	str_="Center Up"
            	ser.write('u'.encode())
            elif(inp=='g'):
            	flag=1
            	str_="Center Down"
            	ser.write('d'.encode())

            elif(inp=='q'):
            	flag=1
            	str_="Reset"
            	ser.write('i'.encode())


            if (inp=='s'):
            	str_="Stop"
            	sys.exit()
            if(flag == 1):
            	ser.write('x'.encode())
            	flag=0

            #print("{:16}".format(str_),end='')
    		# if(not KeyboardInterrupt):
    		# 	return -1

    		# # rcコマンドを送信
    		# drone.send_command( 'rc %s %s %s %s'%(a, b, c, d) )
    		#
    		# if btn1 == 1:		# 離陸
    		# 	drone.takeoff()
    		# elif btn2 == 1:		# 着陸
    		# 	drone.land()
            time.sleep(0.05	)
    		#time.sleep(0.03)	# 適度にウェイトを入れてCPU負荷を下げる
    # except:
    # 	return -1

    except KeyboardInterrupt :    # Ctrl+cが押されたら離脱
    	print( "SIGINTを検知" )
    	#sys.exit
    	return -1

    # # telloクラスを削除
    # del drone

    # "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":
        # importされると"__main__"は入らないので，実行かimportかを判断できる．
        print("OK")
        main()    # メイン関数を実行
