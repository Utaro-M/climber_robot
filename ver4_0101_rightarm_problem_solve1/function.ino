int tmp=0;
void forward(void){
//  hold(1);
//  hold(2);
//  hold(3);
  krs.setPos(4,7100);
  krs.setPos(5,7900);
  if((tmp=krs.getPos(4))!=-1){
    servo_vector[4].ref_angle=tmp;  
  }
  if((tmp=krs.getPos(5))!=-1){
    servo_vector[5].ref_angle=tmp;  
  }
  
  servo_vector[4].flag_hold=0;
  servo_vector[5].flag_hold=0;
  servo_vector[4].last_state=f;
  servo_vector[5].last_state=f;
  SerialBT.println("forward");
  SerialBT.println(servo_vector[4].ref_angle);
  //krs.setFree(4);

}

void back(void){
//  hold(1);
//  //hold(2);
//  hold(3);
  krs.setPos(4,7900);
  krs.setPos(5,7100);
  if((tmp=krs.getPos(4))!=-1){
    servo_vector[4].ref_angle=tmp;  
  }
  if((tmp=krs.getPos(5))!=-1){
    servo_vector[5].ref_angle=tmp;  
  }
//  servo_vector[4].ref_angle=krs.getPos(4);
//  servo_vector[5].ref_angle=krs.getPos(5);
  servo_vector[4].flag_hold=0;
  servo_vector[5].flag_hold=0;
  servo_vector[4].last_state=b;
  servo_vector[5].last_state=b;
  //krs.setFree(4);

}


void pull_up(void){
  krs.setPos(2,7900);
  if((tmp=krs.getPos(2))!=-1){
    servo_vector[2].ref_angle=tmp;  
  }
  //servo_vector[2].ref_angle=krs.getPos(2);
  servo_vector[2].flag_hold=0;
  servo_vector[2].last_state=u;
//  hold(1);
//  hold(3);
//  hold(4);
//  hold(5);
}

void pull_down(void){
  krs.setPos(2,7100);
  if((tmp=krs.getPos(2))!=-1){
    servo_vector[2].ref_angle=tmp;  
  }
  //servo_vector[2].ref_angle=krs.getPos(2);
  servo_vector[2].flag_hold=0;
  servo_vector[2].last_state=d;
//  hold(1);
//  hold(3);
//  hold(4);
//  hold(5);
}


void r_rotate(void){
  krs.setPos(3,7800);
  if((tmp=krs.getPos(3))!=-1){
    servo_vector[3].ref_angle=tmp;  
  }
  //servo_vector[3].ref_angle=krs.getPos(3);
  servo_vector[3].flag_hold=0;
  servo_vector[3].last_state=r;

  //servo_vector[3].current_angle=krs.getPos(3);
  SerialBT.println(servo_vector[3].current_angle);
//  krs.setPos(1,7500);
//  krs.setPos(4,7500);
//  krs.setPos(5,7500);
}

void r_rotate_reverse(void){
  krs.setPos(3,7200);
  if((tmp=krs.getPos(3))!=-1){
    servo_vector[3].ref_angle=tmp;  
  }
  //servo_vector[3].ref_angle=krs.getPos(3);
  servo_vector[3].flag_hold=0;
  servo_vector[3].last_state=rr;

  //servo_vector[3].current_angle=krs.getPos(3);
  SerialBT.println(servo_vector[3].current_angle);
//  krs.setPos(1,7500);
//  krs.setPos(4,7500);
//  krs.setPos(5,7500);
}


void l_rotate(void){
  krs.setPos(1,7200);
  if((tmp=krs.getPos(1))!=-1){
    servo_vector[1].ref_angle=tmp;  
  }
  //servo_vector[1].ref_angle=krs.getPos(1);
  servo_vector[1].flag_hold=0;
  servo_vector[1].last_state=l;

  //servo_vector[1].current_angle=krs.getPos(1);
  SerialBT.println(servo_vector[1].current_angle);
//  krs.setPos(1,7500);
//  krs.setPos(4,7500);
//  krs.setPos(5,7500);
}

void l_rotate_reverse(void){
  krs.setPos(1,7800);
  
  if((tmp=krs.getPos(1))!=-1){
    servo_vector[1].ref_angle=tmp;  
  }
  //servo_vector[1].ref_angle=krs.getPos(1);
  servo_vector[1].flag_hold=0;
  servo_vector[1].last_state=lr;

  //servo_vector[1].current_angle=krs.getPos(1);
  SerialBT.println(servo_vector[1].current_angle);
//  krs.setPos(1,7500);
//  krs.setPos(4,7500);
//  krs.setPos(5,7500);
}

//servo_vectorを初期化 setup()
void init_servo_vector(void){
  for (int i=0;i<6;i++){
    servo_vector[i].current_angle=krs.setPos(i,7500);
    servo_vector[i].ref_angle=krs.setPos(i,7500);
    servo_vector[i].flag_hold=1;
    servo_vector[i].w=0.7;
    servo_vector[i].ki=0.8;
    servo_vector[i].last_state=n;
  }
}

//val==iの時
void reset_servo_vector(void){
  for (int i=0;i<6;i++){
    servo_vector[i].current_angle=krs.setPos(i,7500);
    servo_vector[i].ref_angle=krs.setPos(i,7500);
    servo_vector[i].flag_hold=0;
    servo_vector[i].w=0.7;
    servo_vector[i].ki=1.2;
    servo_vector[i].last_state=n;
  }
}

//使ってない
void hold(int num1){
  servo_vector[num1].current_angle=krs.setFree(num1);
  servo_vector[num1].flag_hold=1;
  //krs.setPos(num1,7500);
  Serial.print("hold");
}

//pid制御？？？
int pi(int dif,int i){
  return (int)(7500+servo_vector[i].w*dif+servo_vector[i].ki*dif*(micros()-pre_time)/ 1000000);
}

//now_state servo_vector[i].last_stateが異なるときに
void hold_check(int now_state){
  int tmp=0;
  for (int i=0;i<s;i++){
    if(servo_vector[i].last_state==now_state){
    }else{
      if((tmp=krs.getPos(i))!=-1){ //getPos(i)が取れなかったときはlast_state等を変更せず次のループでもう一度取り直す
        servo_vector[i].flag_hold=1;
        servo_vector[i].last_state=n;
        servo_vector[i].ref_angle=tmp;
      }else{
//        tmp=krs.getPos(i);
//        while(tmp==-1){
//          tmp=krs.getPos(i);
//        }
//        servo_vector[i].flag_hold=1;
//        servo_vector[i].last_state=n;
//        servo_vector[i].ref_angle=tmp;
      }
    }
  }
}

void free_all(void){

}

void hold_all(void){
  krs.setPos(1,7500);
  //krs.setPos(2,7500);
  krs.setPos(3,7500);
  krs.setPos(4,7500);
  krs.setPos(5,7500);
  Serial.println("hold all");
}
