#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time			# time.sleepを使いたいので
import pygame		# pygameでジョイスティックを読む
import sys
import serial
#ser=serial.Serial('/dev/ttyACM0',9600)
ser=serial.Serial(port="COM13")

def main():
	# pygameの初期化とジョイスティックの初期化
	pygame.init()
	joy = pygame.joystick.Joystick(0)	# ジョイスティック番号はjstest-gtkで確認しておく
	joy.init()


	time.sleep(0.5)		# 通信が安定するまでちょっと待つ

	#Ctrl+cが押されるまでループ
	try:
		i=0
		flag=0
		while True:
			# Joystickの読み込み
			#   get_axisは　-1.0〜0.0〜+1.0 で変化するので100倍して±100にする
			#   プラスマイナスの方向が逆の場合は-100倍して反転させる
			left_right = int( joy.get_axis(0)*100 )		# aは左右移動
			forward_back = int( joy.get_axis(1)*-100 )		# bは前後移動
			arm_up_down = int( joy.get_axis(3)*-100 )		# cは腕の上下移動
			#center = int (joy.get_axis(4)*100)
			#center4 = int (joy.get_axis(4)*100)R2
			#center5 = int (joy.get_axis(5)*100)L2
			#center6 = int (joy.get_axis(6)*100) error
			#d = int( joy.get_axis(2)*100 )		# dは旋回 使わない
			btn0 = joy.get_button(0)
			center_down = joy.get_button(1)
			btn2 = joy.get_button(2)
			center_up = joy.get_button(3)
			L1 = joy.get_button(4)
			R1 = joy.get_button(5)
			#center = joy.get_button(6)
			pygame.event.pump()		# イベントの更新
			#print("4=%d 5=%d 6=%d"%(center4,center5,))
			# プラスマイナスの方向や離陸/着陸に使うボタンを確認するためのprint文
			print("l/r=%d  f/b=%d  u/d=%d   btn0=%d  center_down=%d  btn2=%d  center_up=%d  L1=%d  R1=%d"%(left_right, forward_back, arm_up_down, btn0, center_down, btn2, center_up,L1,R1))

			test=joy.get_button(5)
			print(test)

			i=i+1
			if(i==200):
				break

			if(forward_back>50):
				flag=1
				print("f")
				ser.write('f'.encode())

			if(forward_back<-50):
				flag=1
				print("b")
				ser.write('b'.encode())

			if(R1==1 ):
				if(arm_up_down>50):
					flag=1
					print("ru")
					ser.write('r'.encode())
				elif(arm_up_down<-50):
					flag=1
					print("rd")
					ser.write('a'.encode())
			elif(L1==1):
				if(arm_up_down>50):
					flag=1
					print("a")  #r_rotate_reverse
					ser.write('l'.encode())
				elif(arm_up_down<-50):
					flag=1
					print("b")  #l_rotate_reverse
					ser.write('b'.encode())

			if(center_down==1):
				flag=1
				print("u")
				ser.write('u'.encode())
			if(center_up==1):
				flag=1
				print("d")
				ser.write('d'.encode())

			if(flag == 1):
				ser.write('x'.encode())
				flag=0
			# if(not KeyboardInterrupt):
			# 	return -1

			# # rcコマンドを送信
			# drone.send_command( 'rc %s %s %s %s'%(a, b, c, d) )
			#
			# if btn1 == 1:		# 離陸
			# 	drone.takeoff()
			# elif btn2 == 1:		# 着陸
			# 	drone.land()

			time.sleep(0.03)	# 適度にウェイトを入れてCPU負荷を下げる
	# except:
	# 	return -1

	except KeyboardInterrupt :    # Ctrl+cが押されたら離脱
		print( "SIGINTを検知" )
		#sys.exit
		return -1

	# # telloクラスを削除
	# del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":		# importされると"__main__"は入らないので，実行かimportかを判断できる．
	main()    # メイン関数を実行
