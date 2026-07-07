#property indicator_chart_window
#property indicator_buffers 8
#property indicator_color1 Sienna
#property indicator_color2 OrangeRed 
#property indicator_color3 Maroon
#property indicator_color4 Green
#property indicator_color5 Indigo
#property indicator_color6 Navy
#property indicator_color7 DarkSlateBlue
#property indicator_color8 DarkBlue

//---- input parameters
extern int CountBars=500;
extern bool alert = true;
extern int max_length = 30;
extern double error = 0.1;

extern color zz_clr   = Blue;
extern color bat_clr  = Sienna;
extern color crab_clr = OrangeRed;
extern color gar_clr = Maroon;
extern color ab_clr  = Green;
extern color but_clr = Indigo;

color get_harmony_color(int pattern){
   switch(pattern){
      case 1: return (ab_clr); break;
      case 2: return (gar_clr); break;
      case 3: return (but_clr); break;
      case 4: return (bat_clr); break;
      case 5: return (crab_clr); break;
      }
   return (zz_clr);
}

string get_harmony_pattern(int pattern,int shift){
   string pstr = "";
   switch(pattern){
      case 1: pstr = "AB=CD"; break;
      case 2: pstr = "Gartley"; break;
      case 3: pstr = "Butterfly"; break;
      case 4: pstr = "Bat"; break;
      case 5: pstr = "Crab"; break;
      }
   pstr = pstr + " at "+shift;
   return (pstr);
}

double bufBAT[];
double bufCRAB[];
double bufGAR[];
double bufAB[];
double bufBUT[];
double bufALL[];
double bufT0[];
double bufT1[];


int init(){
//----
   SetIndexStyle(0,DRAW_NONE,STYLE_SOLID,3);
   SetIndexStyle(1,DRAW_NONE,STYLE_SOLID,3);
   SetIndexStyle(2,DRAW_NONE,STYLE_SOLID,3);
   SetIndexStyle(3,DRAW_NONE,STYLE_SOLID,3);
   SetIndexStyle(4,DRAW_NONE,STYLE_SOLID,3);
   SetIndexStyle(5,DRAW_NONE);
   SetIndexStyle(6,DRAW_ARROW,STYLE_SOLID,2);
   SetIndexStyle(7,DRAW_ARROW,STYLE_SOLID,2);

   SetIndexBuffer(0,bufBAT);
   SetIndexBuffer(1,bufCRAB);
   SetIndexBuffer(2,bufGAR);
   SetIndexBuffer(3,bufAB);
   SetIndexBuffer(4,bufBUT);
   SetIndexBuffer(5,bufALL);
   SetIndexBuffer(6,bufT0);
   SetIndexBuffer(7,bufT1);

   //SetIndexBuffer(0,bufALL);

   SetIndexEmptyValue(0,0);
   SetIndexEmptyValue(1,0);
   SetIndexEmptyValue(2,0);
   SetIndexEmptyValue(3,0);
   SetIndexEmptyValue(4,0);
   SetIndexEmptyValue(5,0);
   SetIndexEmptyValue(6,0);
   SetIndexEmptyValue(7,0);
   
   SetIndexArrow(0,132);
   SetIndexArrow(1,133);
   SetIndexArrow(2,130);
   SetIndexArrow(3,129);
   SetIndexArrow(4,131);
   
   SetIndexArrow(6,167);
   SetIndexArrow(7,110);

   IndicatorDigits(MarketInfo(Symbol(),MODE_DIGITS)+2);
//----

   return(0);
  }

void delete_obj(){
   string  buff_str = "";
   for(int i=ObjectsTotal()-1;i>=0;i--){
      buff_str = ObjectName(i);
      if(StringFind(buff_str,"harmony_05_",0)==0) ObjectDelete(buff_str);
      }
}

static int acc = 0;

void update_zz(int from,double arr[],int ind[]){
   color c = Crimson;
   int off = 0 ;
   if(from==0){
      c = DarkBlue;
      off = 3;
      }
   for(int i=from;i<4;i++){
      create_line(ind[i],ind[i+1],get_harmony_color(7),arr[i],arr[i+1],0,STYLE_SOLID);
      if(i<3){
         place_text(
            DoubleToStr(MathAbs(arr[i+2]-arr[i+1])/MathAbs(arr[i]-arr[i+1]),3),
            (ind[i]+ind[i+2])/2,
            (arr[i]+arr[i+2])/2,
            zz_clr);
         create_line(ind[i],ind[i+2],Gray,arr[i],arr[i+2],0,STYLE_DOT);
         }
      switch(i){
         case 0:place_text("X",ind[i]+off,arr[i],c); break;
         case 1:place_text("A",ind[i]+off,arr[i],c); break;
         case 2:place_text("B",ind[i]+off,arr[i],c); break;
         case 3:place_text("C",ind[i]+off,arr[i],c); break;
         case 4:place_text("D",ind[i]+off,arr[i],c); break;
         }
      }
   if(from==0){
      create_triangle(ind[0],ind[1],ind[2],BurlyWood,arr[0],arr[1],arr[2]);
      create_triangle(ind[2],ind[3],ind[4],CadetBlue,arr[2],arr[3],arr[4]);
      }
   else{
      create_triangle(ind[2],ind[3],ind[4],Tomato,arr[2],arr[3],arr[4]);
      }
}

void place_text(string text,int x,double price,color c){
   static int acc = 0;
   string  buff_str = "harmony_05_text_"+acc; acc++;
      //OBJ_LABEL
   if(ObjectFind(buff_str)==-1){
      ObjectCreate(buff_str, OBJ_TEXT, 0, Time[x], price);
      }
   //ObjectSet(buff_str,OBJPROP_COLOR,c);
   ObjectSet(buff_str,OBJPROP_TIME1,Time[x]);
   ObjectSet(buff_str,OBJPROP_PRICE1,price);
   //ObjectSet(buff_str,OBJPROP_FONTSIZE,10);
   ObjectSetText(buff_str,text,10,"Arial",c);
   
}

void create_line(int from,int to,color c,double p0,double p1,int long,int type){
   static int acc = 0;
   string  buff_str = "harmony_05_"+acc; acc++;
   ObjectCreate(buff_str, OBJ_TREND, 0, Time[from], p0, Time[to], p1);
   ObjectSet(buff_str,OBJPROP_RAY,long);
   ObjectSet(buff_str,OBJPROP_COLOR,c);
   ObjectSet(buff_str,OBJPROP_XDISTANCE,100);
   ObjectSet(buff_str,OBJPROP_YDISTANCE,100);
   ObjectSet(buff_str,OBJPROP_STYLE,type);
   if(type!=STYLE_SOLID)
      ObjectSet(buff_str,OBJPROP_WIDTH,1);
   else
      ObjectSet(buff_str,OBJPROP_WIDTH,2);
}

int deinit(){
   delete_obj();
   return (0);
}

double last_time = 0;

double XA,XB,XD,AB,AC,BC,BD,CD,AD;
 
void init_lines(double arr[],int ind[]){
   XA = 0;
   if(MathAbs(ind[0]-ind[1])>1 && MathAbs(ind[1]-ind[2])>1 && MathAbs(ind[2]-ind[3])>1 && MathAbs(ind[3]-ind[4])>1){
      if(
         (arr[1]-arr[3])*(arr[2]-arr[3])<0 && 
         (arr[0]-arr[2])*(arr[1]-arr[2])<0
         ){
         XA = MathAbs(arr[1]-arr[0]) / Point;
         XB = MathAbs(arr[2]-arr[0]) / Point;
         XD = MathAbs(arr[4]-arr[0]) / Point;
         AB = MathAbs(arr[2]-arr[1]) / Point;
         AC = MathAbs(arr[3]-arr[1]) / Point;
         BC = MathAbs(arr[3]-arr[2]) / Point;
         BD = MathAbs(arr[4]-arr[2]) / Point;
         CD = MathAbs(arr[4]-arr[3]) / Point;
         AD = MathAbs(arr[4]-arr[1]) / Point;
         }
      }
}
/*
double get_retracement(int a,int b,double arr[],double ret){
   return (arr[a] + ((arr[a]-arr[b]) / Point)*ret*Point);
}
*/

bool is_ABCD_pattern(double arr[],int ind[],double offset){

   double F0,F1;
   bool found = false;
   F0 = NormalizeDouble(BC / AB,3);
   F1 = NormalizeDouble(CD / BC,3);
   found = 
      (F0>=0.382-offset && F0<=0.382+offset && F1>=2.240-offset && F1<=2.240+offset) ||
      (F0>=0.500-offset && F0<=0.500+offset && F1>=2.000-offset && F1<=2.000+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset && F1>=1.618-offset && F1<=1.618+offset) ||
      (F0>=0.707-offset && F0<=0.707+offset && F1>=1.414-offset && F1<=1.414+offset) ||
      (F0>=0.786-offset && F0<=0.786+offset && F1>=1.270-offset && F1<=1.270+offset) ;
      
   if(!found) return (false);
   bufAB[ind[4]]  = arr[4];
   bufALL[ind[4]] = 1.0;
   update_zz(1,arr,ind);
   bufT0[ind[4]]  = arr[4]+(((arr[2]-arr[4])/Point)*0.618)*Point;
   bufT1[ind[4]]  = arr[4]+(((arr[1]-arr[4])/Point)*0.618)*Point;
   
   place_text(get_harmony_pattern(1,ind[4]),ind[4],bufAB[ind[4]],get_harmony_color(1));
   //Print(harmony_pattern(1,ind[4]));
   return (true);
}

bool is_Gartley_pattern(double arr[],int ind[],double offset){
   double F0,F1;
   bool found = false;
   F0 = NormalizeDouble(AB / XA,3);
   F1 = NormalizeDouble(AD / XA,3);
   
   found = 
      (
      (F0>=0.382-offset && F0<=0.382+offset) ||
      (F0>=0.477-offset && F0<=0.477+offset) ||
      (F0>=0.500-offset && F0<=0.500+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset) 
      ) &&
      (
      (F1>=0.618-offset && F1<=0.618+offset) ||
      (F1>=0.786-offset && F1<=0.786+offset) 
      );
      //(F0==0.618/*-offset && F0<=0.618+offset*/ && F1==0.786/*-offset && F1<=0.786+offset*/);
   
   if(!found) return (false);
   
   F0 = NormalizeDouble(BC / AB,3);
   F1 = NormalizeDouble(CD / BC,3);
   found = 
      (F0>=0.382-offset && F0<=0.382+offset && F1>=2.240-offset && F1<=2.240+offset) ||
      (F0>=0.500-offset && F0<=0.500+offset && F1>=2.000-offset && F1<=2.000+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset && F1>=1.618-offset && F1<=1.618+offset) ||
      (F0>=0.707-offset && F0<=0.707+offset && F1>=1.414-offset && F1<=1.414+offset) ||
      (F0>=0.786-offset && F0<=0.786+offset && F1>=1.270-offset && F1<=1.270+offset) ||
      (F0>=0.886-offset && F0<=0.886+offset && F1>=1.129-offset && F1<=1.129+offset) ;
      
   if(!found) return (false);
   
   bufGAR[ind[4]] = arr[4]+10*Point;
   bufT0[ind[4]]  = arr[4]+(((arr[3]-arr[4])/Point)*0.618)*Point;
   bufT1[ind[4]]  = arr[4]+(((arr[1]-arr[4])/Point)*0.618)*Point;
   bufALL[ind[4]] = 2.0;
   update_zz(0,arr,ind);
   place_text(get_harmony_pattern(2,ind[4]),ind[4],bufGAR[ind[4]],get_harmony_color(2));
   //Print(harmony_pattern(2,ind[4]));
   return (true);
}

bool is_Butterfly_pattern(double arr[],int ind[],double offset){
   double F0,F1;
   bool found = false;
   F0 = NormalizeDouble(AB / XA,3);
   F1 = NormalizeDouble(AD / XA,3);
   
   found = 
      (
      (F0>=0.618-offset && F0<=0.618+offset) ||
      (F0>=0.786-offset && F0<=0.786+offset) ||
      (F0>=0.886-offset && F0<=0.886+offset) 
      ) &&
      (
      (F1>=1.270-offset && F1<=1.270+offset) ||
      (F1>=1.618-offset && F1<=1.618+offset) 
      );
      //(F0==0.618/*-offset && F0<=0.618+offset*/ && F1==0.786/*-offset && F1<=0.786+offset*/);
   
   if(!found) return (false);

   F0 = NormalizeDouble(BC / AB,3);
   F1 = NormalizeDouble(CD / BC,3);
   found = 
      (
      (F0>=0.382-offset && F0<=0.382+offset) 
         && (
            (F1>=2.240-offset && F1<=2.240+offset) ||
            (F1>=1.618-offset && F1<=1.618+offset) ||
            (F1>=2.618-offset && F1<=2.618+offset) 
            )
      ) ||
      (
      (F0>=0.500-offset && F0<=0.500+offset) 
         && (
            (F1>=2.000-offset && F1<=2.000+offset) ||
            (F1>=2.618-offset && F1<=2.618+offset) 
            )
      ) ||
      (
      (F0>=0.618-offset && F0<=0.618+offset) 
         && (
            (F1>=1.618-offset && F1<=1.618+offset) ||
            (F1>=2.000-offset && F1<=2.000+offset) ||
            (F1>=2.618-offset && F1<=2.618+offset) ||
            (F1>=2.240-offset && F1<=2.240+offset) 
            )
      ) ||
      (F0>=0.707-offset && F0<=0.707+offset && F1>=1.414-offset && F1<=1.414+offset) ||
      (
      (F0>=0.786-offset && F0<=0.786+offset) 
         && (
            (F1>=1.618-offset && F1<=1.618+offset) ||
            (F1>=2.618-offset && F1<=2.618+offset) ||
            (F1>=2.240-offset && F1<=2.240+offset) 
            )
      ) ||
      (F0>=0.886-offset && F0<=0.886+offset && F1>=1.270-offset && F1<=1.270+offset);
      
   if(!found) return (false);

   bufBUT[ind[4]] = arr[4]+20*Point;
   bufALL[ind[4]] = 3.0;
   bufT0[ind[4]]  = arr[4]+(((arr[3]-arr[4])/Point)*0.618)*Point;
   bufT1[ind[4]]  = arr[4]+(((arr[1]-arr[4])/Point)*0.618)*Point;
   update_zz(0,arr,ind);
   place_text(get_harmony_pattern(3,ind[4]),ind[4],bufBUT[ind[4]],get_harmony_color(3));
   //Print(harmony_pattern(3,ind[4]));
   return (true);
}

bool is_BAT_pattern(double arr[],int ind[],double offset){
   double F0,F1,F2;
   bool found = false;
   F0 = NormalizeDouble(AB / XA,3);
   F1 = NormalizeDouble(AD / XA,3);
   F2 = NormalizeDouble(CD / BC,3);
   found = 
      (F0>=0.382-offset && F0<=0.618+offset) 
      && (F1>=0.886-offset && F1<=0.886+offset)
      && (F2>=1.618-offset && F2<=2.618+offset)
      ;
   
   if(!found) return (false);

   F0 = NormalizeDouble(BC / AB,3);
   F1 = F2;
   
   found = 
      (F0>=0.500-offset && F0<=0.500+offset && F1>=2.618-offset && F1<=2.618+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset && F1>=2.000-offset && F1<=2.000+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset && F1>=2.240-offset && F1<=2.240+offset) ||
      (F0>=0.786-offset && F0<=0.786+offset && F1>=1.618-offset && F1<=1.618+offset) ||
      (F0>=0.886-offset && F0<=0.886+offset && F1>=1.270-offset && F1<=1.270+offset) ;
   if(!found) return (false);

   bufBAT[ind[4]] = arr[4]+30*Point;
   bufALL[ind[4]] = 4.0;
   bufT0[ind[4]]  = arr[4]+(((arr[3]-arr[4])/Point)*0.618)*Point;
   bufT1[ind[4]]  = arr[4]+(((arr[1]-arr[4])/Point)*0.618)*Point;
   update_zz(0,arr,ind);
   place_text(get_harmony_pattern(4,ind[4]),ind[4],bufBAT[ind[4]],get_harmony_color(4));
   
   return (true);
}

bool is_CRAB_pattern(double arr[],int ind[],double offset){
   double F0,F1;
   bool found = false;
   F0 = NormalizeDouble(AB / XA,3);
   F1 = NormalizeDouble(CD / BC,3);
   
   found = 
      (
      (F0>=0.382-offset && F0<=0.382-offset) ||
      (F0>=0.477-offset && F0<=0.477+offset) ||
      (F0>=0.500-offset && F0<=0.500+offset) ||
      (F0>=0.618-offset && F0<=0.618+offset) 
      )
      &&
      (
      (F1>=2.618-offset && F1<=2.618+offset) ||
      (F1>=3.140-offset && F1<=3.140+offset) ||
      (F1>=3.618-offset && F1<=3.618+offset) 
      );
   
   if(!found) return (false);
   
   bufCRAB[ind[4]] = arr[4]+40*Point;
   bufALL[ind[4]] = 5.0;
   bufT0[ind[4]]  = arr[4]+(((arr[3]-arr[4])/Point)*0.618)*Point;
   bufT1[ind[4]]  = arr[4]+(((arr[1]-arr[4])/Point)*0.618)*Point;
   update_zz(0,arr,ind);
   place_text(get_harmony_pattern(5,ind[4]),ind[4],bufCRAB[ind[4]],get_harmony_color(5));
   //Print(harmony_pattern(5,ind[4]));
   return (true);
}

int last = 0 ;
datetime last_ = 0;

int start(){
   if(last==Bars) return (0);
   delete_obj();
   last = Bars;
   //delete_obj();
  
  
   int point_arr[5];
   double val_arr[5];
   
   int i,l = 0;
   int pi = 4,j = 0;
   datetime ld;
   double gann = 0;
   int limit = CountBars;
   
   int found = limit;
   for(int len = max_length;len>2;len--){
      j = 0;
      pi = 4;
      while(j<limit && pi>=0){
         gann = iCustom(Symbol(),Period(),"a_ZZ",limit,0,len,0,j);
         //gann = iCustom(Symbol(),Period(),"0_ZigZag",Length,0,0,0,from,0,j);
         if(gann!=0.0){
            point_arr[pi] = j;
            val_arr[pi] = gann;
            pi--;
            }
         j++;
         }
      //limit -= 10;
      init_lines(val_arr,point_arr);
      if(XA!=0){
         if( 
             is_ABCD_pattern(val_arr,point_arr,error) ||
             is_Gartley_pattern(val_arr,point_arr,error) ||
             is_Butterfly_pattern(val_arr,point_arr,error) ||
             is_CRAB_pattern(val_arr,point_arr,error) ||
             is_BAT_pattern(val_arr,point_arr,error)
            ){
            if(found>point_arr[4]){
               found = point_arr[4];
               }
            Sleep(50);
            }
         }
      }
   if(found!=CountBars && Time[found]>last_){
      last_ = Time[found];
      if(alert) Alert(Symbol()+":: Possible Price Pattern found at "+found+" bar.");
      }
   //ObjectsRedraw();
   return(0);
  }
//+------------------------------------------------------------------+

void create_triangle(int p0,int p1,int p2,color c,double c0,double c1,double c2){
   static int acc = 0;
   string  buff_str = "harmony_05_tri_"+acc; acc++;
   
   datetime t0 = Time[p0],t1 = Time[p1],t2 = Time[p2];
   if(p1<0) t1 = Time[0] + Period()*60*MathAbs(p1);
   if(p2<0) t2 = Time[0] + Period()*60*MathAbs(p2);
   
   ObjectCreate(buff_str, OBJ_TRIANGLE, 0, t0, c0, t1, c1, t2, c2);
   ObjectSet(buff_str, OBJPROP_COLOR, c );
   ObjectSet(buff_str, OBJPROP_STYLE,  STYLE_DOT );
   ObjectSet(buff_str,OBJPROP_BACK,true);
}

