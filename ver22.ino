#include <IcsHardSerialClass.h>
#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
#include<stdio.h>

const byte EN_PIN = 2;
const long BAUDRATE =1250000; //115200;
const int TIMEOUT = 10;    //通信できてないか確認用にわざと遅めに設定

IcsHardSerialClass krs(&Serial,EN_PIN,BAUDRATE,TIMEOUT);  //インスタンス＋ENピン(2番ピン)およびUARTの指定

byte val=0,pre_val=0;

//#define 
int s=5;

#define n 0
#define f 1
#define b 2
#define u 3
#define d 4
#define r 5
#define l 6



typedef struct{
  int flag_hold=0;
  int current_angle=0;
  int ref_angle=0;
  float w=1;
  int last_state=0;
  int ki=0;
}servo;

servo servo_vector[6];



void setup() {
  s+=1;
  SerialBT.begin("ESP32");
  //Serial.begin(9600);
  digitalWrite(2,OUTPUT);
  
//ICS用
  pinMode(4,OUTPUT);
  digitalWrite(4,HIGH);
  krs.begin();  //サーボモータの通信初期設定

//servo_vectorを初期化
  for (int i=0;i<6;i++){
    servo_vector[i].current_angle=krs.setPos(i,7500);
    servo_vector[i].ref_angle=krs.setPos(i,7500);
    servo_vector[i].flag_hold=1;
    servo_vector[i].w=0.8;
    servo_vector[i].ki=1;    
    servo_vector[i].last_state=n;
  }
  
}

float pre_time=0;
void loop() {
  int r_pos=0;
  for (int i=0;i<6;i++){
    servo_vector[i].current_angle=krs.getPos(i);
    
    if(servo_vector[i].flag_hold==1){
      int dif=servo_vector[i].ref_angle-servo_vector[i].current_angle;
      if(2<abs(dif) && abs(dif)<500){
        krs.setPos(i,pi(dif,i));
      }
    }
  }
  pre_time=micros();
  
  if(SerialBT.available()>0){
    val=SerialBT.read();
    //SerialBT.println("init");
  }
  
  if(val=='f'){
    forward();
    hold_check(f);
    
  }else if(val=='b'){
    back();
    SerialBT.println("back");
    hold_check(b);
    
  }else if(val=='u'){
    pull_up();
    SerialBT.println("pull_up");
    hold_check(u);
    
  }else if(val=='d'){
    pull_down();
    SerialBT.println("pull_down");
    hold_check(d);
    
  }else if(val=='r'){
    r_rotate();
    SerialBT.println("r_rotate");
    hold_check(r);
    
  }else if(val=='l'){
    l_rotate();
    SerialBT.println("l_rotate");
    hold_check(l);

  }else if(val=='y'){
    l_rotate();
    r_rotate();
    SerialBT.println("both_rotate");
    hold_check(l);
    hold_check(r);

  }
  else if(val=='t'){
  //r_pos=set_pos(4,7400);
  
//  SerialBT.println(r_pos);
   //r_pos=krs.setPos(4,8000);
   //r_pos=krs.setFree(4);
   //r_pos=krs.getPos(4);

   r_pos=krs.setPos(4,7500);////////
   
   
   SerialBT.println(r_pos);
   }
  else{
//    krs.setPos(4,7500);/////////
//    krs.setPos(1,7500);
//    krs.setPos(3,7500);
//    krs.setFree(2);
//    //krs.setFree(4);/////////
//    krs.setFree(5);
//    //hold_all();

    hold_check(n);
    SerialBT.println("quit");
  }
  

  
}
