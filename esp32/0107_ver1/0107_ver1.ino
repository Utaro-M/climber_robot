
#include <ESP32Servo.h>

#include <IcsHardSerialClass.h>
#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
#include<stdio.h>


//test 用
float kp=0.8;
float ki=0.5  ;
float kd=0.4;



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
#define rr 7
#define lr 8


//servo for camera
// create for servo objects
Servo servo1;
int servo1Pin = 12;

// Published values for SG90 servos; adjust if needed
int minUs = 500;
int maxUs = 2400;
int pos = 0;      // position in degrees

typedef struct{
  int flag_hold=0;
  int current_angle=0;
  int ref_angle=0;
  int init_angle=0;
  float w=1;
  float kp=1;
  float ki=1;
  float kd=1;
  int last_state=0;
  int dif_array[3]={0,0,0};

}serv;

serv servo_vector[6];




void setup() {

  //servo for camera
  servo1.setPeriodHertz(50);      // Standard 50hz servo
  servo1.attach(servo1Pin, minUs, maxUs);

  s+=1;
  SerialBT.begin("ESP32");
  //Serial.begin(9600);
  digitalWrite(2,OUTPUT);

//ICS用
  pinMode(4,OUTPUT);
  digitalWrite(4,HIGH);
  krs.begin();  //サーボモータの通信初期設定

//servo_vectorを初期化

  init_servo_vector();

//resetしてから4秒内に電源ONで目標角度、現在角度を取得
  delay(4000);
  for(int i=0;i<6;i++){
    servo_vector[i].current_angle=krs.getPos(i);
    servo_vector[i].ref_angle=servo_vector[i].current_angle;
  }
}
int tmp=0;

int count=0;
float pre_time=0;
//camera_servoの角度を保持
float camera_servo_pos=30;
void loop() {



//  for (pos = 0; pos <= 180; pos += 1) { // sweep from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    servo1.write(pos);
//    delay(2);             // waits 20ms for the servo to reach the position
//  }
//  for (pos = 180; pos >= 0; pos -= 1) { // sweep from 180 degrees to 0 degrees
//    servo1.write(pos);
//    delay(2);
//  }

  //SerialBT.println(krs.getPos(3));
 //SerialBT.println(servo_vector[3].ref_angle);

  int r_pos=0;
  //hold
  for (int i=0;i<6;i++){

    if((tmp=krs.getPos(i))!=-1){
      servo_vector[i].current_angle=tmp;
    }
    //flag_holdが１だとholdする、hold_check()で連続して同じコマンドが送られているときは０、コマンドが切れたときは１にする
    if(servo_vector[i].flag_hold==1){
      //目標値と現在値の差

      int dif=servo_vector[i].ref_angle-servo_vector[i].current_angle;
      if(1<abs(dif) && abs(dif)<500){
        krs.setPos(i,pi(dif,i));
      }else if(abs(dif)>9510){//3500->11500 or 11500->3500
        //forward後の場合　４が左、５が右？
        if(dif<0){
          servo_vector[i].ref_angle=12495;
        }else if(dif>0){
          servo_vector[i].ref_angle=2505;
        }

//        if(servo_vector[i].last_state==f){
//          switch (i){
//            case 4 :
//            servo_vector[i].ref_angle=12500;
//            break;
//            case 5:
//            servo_vector[i].ref_angle=2500;
//            break;
//          }
//
//        }else if(servo_vector[i].last_state==b){// backの後の場合　４が左、５が右？
//          switch (i){
//            case 4 :
//            servo_vector[i].ref_angle=3500;
//            break;
//            case 5:
//            servo_vector[i].ref_angle=11500;
//            break;
//          }
//        }else if(servo_vector[i].last_state==u){
//          servo_vector[2].ref_angle=11500;
//        }else if(servo_vector[i].last_state==d){
//          servo_vector[2].ref_angle=3500;
//        }else if(servo_vector[i].last_state==r or servo_vector[i].last_state==lr){
//          servo_vector[i].ref_angle=12500;
//        }else if(servo_vector[i].last_state==l or servo_vector[i].last_state==rr){
//          servo_vector[i].ref_angle=2500;
//        }

      }
        // servo_vector[i].current_angle=krs.getPos(i);
        // krs.setPos(i,servo_vector[i].current_angle);


//   int r_pos=0;
//   for (int i=0;i<6;i++){
//     servo_vector[i].current_angle=krs.getPos(i);

//     if(servo_vector[i].flag_hold==1){
//       int dif=servo_vector[i].ref_angle-servo_vector[i].current_angle;
//       if(2<abs(dif) && abs(dif)<500){
//         krs.setPos(i,pid(dif,i));
//       }

    }
  }
  pre_time=micros();

  if(SerialBT.available()>0){
    val=SerialBT.read();
    //SerialBT.println("init");
  }else{
    val='o';
  }
  Serial.println(val);
  if(val=='f'){
    forward();
    hold_check(f);

  }else if(val=='b'){
    back();
    //SerialBT.println("back");
    hold_check(b);

  }else if(val=='u'){
    pull_up();
    //SerialBT.println("pull_up");
    hold_check(u);

  }else if(val=='d'){
    pull_down();
    //SerialBT.println("pull_down");
    hold_check(d);

  }else if(val=='r'){
    r_rotate();
    //SerialBT.println("r_rotate");
    hold_check(r);

  }else if(val=='l'){
    l_rotate();
    //SerialBT.println("l_rotate");
    hold_check(l);

  }else if(val=='a'){
    r_rotate_reverse();
    //SerialBT.println("r_rotate_reverse");
    hold_check(rr);

  }else if(val=='c'){
    l_rotate_reverse();
    //SerialBT.println("l_rotate_reverse");
    hold_check(lr);

  }else if(val=='y'){
    l_rotate();
    r_rotate();
    //SerialBT.println("both_rotate");
    hold_check(l);
    hold_check(r);

  }else if(val=='h'){
    l_rotate_reverse();
    r_rotate_reverse();
    //SerialBT.println("both_rotate_reverse");
    hold_check(lr);
    hold_check(rr);

  }
  else if(val=='i'){
    // reset_servo_vector();
    // delay(1000);
    for(int i=0;i<6;i++){
      krs.setFree(i);
    }
    delay(4000);
    init_servo_vector();


  }
  else if(val=='t'){
  //r_pos=set_pos(4,7400);

//  SerialBT.println(r_pos);
   //r_pos=krs.setPos(4,8000);
   //r_pos=krs.setFree(4);
   //r_pos=krs.getPos(4);

   r_pos=krs.setPos(4,7500);////////


   //SerialBT.println(r_pos);
   }else if(val=='P'){
    for (int i=0;i<6;i++){
      servo_vector[i].kp+=0.1;
      servo_vector[i].ki=ki;
      servo_vector[i].kd=kd;
    }
    //SerialBT.println(servo_vector[1].kp);
   }else if(val=='I'){
    for (int i=0;i<6;i++){
      servo_vector[i].kp=kp;
      servo_vector[i].ki+=0.1;
      servo_vector[i].kd=kd;
    }
    //SerialBT.println(servo_vector[1].ki);
   }else if(val=='D'){
    for (int i=0;i<6;i++){
      servo_vector[i].kp=kp;
      servo_vector[i].ki=ki;
      servo_vector[i].kd+=0.1;
    }
    //SerialBT.println(servo_vector[1].kd);
   }else if(val=='m'){
    if(camera_servo_pos<140){
      camera_servo_pos+=1;
      servo1.write(camera_servo_pos);
    }else{
      servo1.write(camera_servo_pos);
    }

  }else if(val=='n'){
    if(20<camera_servo_pos){
      camera_servo_pos-=1;
      servo1.write(camera_servo_pos);
    }else{
      servo1.write(camera_servo_pos);
    }
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
    //SerialBT.println("quit");
    //SerialBT.println(count++);
  }



}
