  //name="code"]
  int set_pos (unsigned char id, int pos)
{
  digitalWrite(EN_PIN,LOW);
  unsigned char tx[3]; // 送信用のデータ
  unsigned char rx[3]; // 受信用のデータ
  //unsigned int rx[3]; // 受信用のデータ
  int i; // 繰り返し処理のためにつかう変数
  int dat; // 現在位置を計算するための変数

  tx[0] = 0x80 | id;
  //tx[1] = (unsigned char)(pos &gt;&gt; 7 &amp; 0x7F);
  //tx[2] = (unsgined char)(pos &amp; 0x7F);
  tx[1] =(unsigned char) ((pos >> 7) && 0x7F);
  tx[2] =(unsigned char) ((pos) && (0x7F));

  int ch=0;
  digitalWrite(EN_PIN,HIGH);
  for (i = 0; i < 3; i++)
  {
    putchar (tx[i]); // コマンドを１バイトずつ送信する
  }
  
  digitalWrite(EN_PIN,LOW);
  //delay(100);
  //SerialBT.println("transpose");
  for (i = 0; i < 3; i++)
  {
    //if((scanf("%d",&ch)) !=EOF){
    if((ch=getchar()) !=EOF){
//      rx[i] = getchar (); // モーターからの返値を受け取り、rxに代入する
        rx[i] = ch; // モーターからの返値を受け取り、rxに代入する
    }else{
      SerialBT.println("erorr ");
    }
  }

//  dat = (int)(rx[1] &amp; 0x7F);
//  dat = (dat &lt;&lt; 7) + (int)rx[2];
  dat = (int)((rx[1]) && (0x7F));
  dat = (dat << 7) + (int)(rx[2]);
  //SerialBT.println(dat);

  return dat;
}
