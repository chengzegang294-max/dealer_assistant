#property  copyright "ANG3110@latchess.com"
//-------------ang_Amp_ZZ---------------
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_color1 Blue

//--------------------------------
extern int cbars=1000;
extern int from=0;
extern int Length=10;
extern double error = 0.1;
extern bool draw = false;

//---------------------------------
double ha[],la[],zz[],un[],pattern[],position[];
double hi,li,hm,lm,di,j;
int f,f1,ai,bi,aii,bii,f0,aibar,bibar;
//----------------------------------------------
string id = "a_zz_";

int init()  {   
   id = id + Length +"_";
   IndicatorBuffers(6);
   SetIndexStyle(0,DRAW_SECTION,STYLE_SOLID,2);

   SetIndexBuffer(0,zz);
   SetIndexBuffer(1,la);
   SetIndexBuffer(2,ha);   
   SetIndexBuffer(3,un);
   SetIndexBuffer(4,pattern);
   SetIndexBuffer(5,position);
   
   

   SetIndexEmptyValue(0,0);
   SetIndexEmptyValue(1,0);
   SetIndexEmptyValue(2,0);
   SetIndexEmptyValue(3,0);
   SetIndexEmptyValue(4,0);
   SetIndexEmptyValue(5,0);
   
   return(0);  
}

void place_text(string text,int x,double price,color c){
   if(!draw) return (0);
   string  buff_str = id+text+x+price;
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

void create_line(int from,int to,color c,double p0,double p1,int long,int style){
   if(!draw) return (0);
   static int acc = 0;
   string  buff_str = id+acc; acc++;
   ObjectCreate(buff_str, OBJ_TREND, 0, Time[from], p0, Time[to], p1);
   ObjectSet(buff_str,OBJPROP_RAY,long);
   ObjectSet(buff_str,OBJPROP_COLOR,c);
   ObjectSet(buff_str,OBJPROP_XDISTANCE,100);
   ObjectSet(buff_str,OBJPROP_YDISTANCE,100);
   ObjectSet(buff_str,OBJPROP_STYLE,style);
   ObjectSet(buff_str,OBJPROP_BACK,true);
   //ObjectSet(buff_str,OBJPROP_WIDTH,2);
}

void delete_obj(){
   string  buff_str = "";
   for(int i=ObjectsTotal()-1;i>=0;i--){
      buff_str = ObjectName(i);
      if(StringFind(buff_str,id,0)==0) ObjectDelete(buff_str);
      }
}

int deinit(){
   delete_obj();
   return (0);
}

int last=0;
//================================
int start()  {   
   if(last==Bars) return (0);
   last=Bars;
   delete_obj();
   ArrayInitialize(zz,0);
   //ArrayInitialize(ha,0);
   //ArrayInitialize(la,0);
   
   int shift,Swing,Swing_n,uzl,i,zu,zd,mv;
   double LL,HH,BH,BL,NH,NL; 
   double Uzel[10000][3]; 
   string text;
// loop from first bar to current bar (with shift=0) 
   Swing_n=0;Swing=0;uzl=0; 
   
   int barn = from + cbars;
   BH =High[barn];
   BL=Low[barn];
   zu=barn;
   zd=barn; 

   for(shift=barn;shift>=from;shift--) { 
      LL=10000000;
      HH=-100000000; 
      for(i=shift+Length;i>=shift+1;i--) { 
         if (Low[i]< LL) LL=Low[i];
         if (High[i]>HH) HH=High[i]; 
         } 
         
      if (Low[shift]<LL && High[shift]>HH){ 
         Swing=2; 
         if (Swing_n==1)  zu=shift+1; 
         if (Swing_n==-1) zd=shift+1; 
         }
      else{ 
         if (Low[shift]<LL)  Swing=-1; 
         if (High[shift]>HH) Swing=1; 
         } 
         
      if (Swing!=Swing_n && Swing_n!=0) { 
         if (Swing==2) {
            Swing=-Swing_n;
            BH = High[shift];
            BL = Low[shift]; 
            } 
         uzl=uzl+1; 
         if(Swing==1) {
            Uzel[uzl][1]=zd;
            Uzel[uzl][2]=BL;
            } 
         if(Swing==-1) {
            Uzel[uzl][1]=zu;
            Uzel[uzl][2]=BH; 
            } 
         BH = High[shift];
         BL = Low[shift]; 
         } 
      if (Swing==1) { 
         if(High[shift]>=BH) {
            BH=High[shift];
            zu=shift;
            }
         } 
      else if(Swing==-1) {
         if(Low[shift]<=BL) {
            BL=Low[shift]; 
            zd=shift;
            }
         } 
      Swing_n=Swing; 
      } 
   
   for(i=1;i<=uzl;i++) { 
      mv=StrToInteger(DoubleToStr(Uzel[i][1],0));
      zz[mv]=Uzel[i][2];
      } 

   //--------------------------------
   int dir = 0;
   int pos[3]; int cpos = 0; int id = 0;
   for(i=barn; i>=from; i--){ 
      un[i] = 0;
      if(zz[i]!=0){
         pos[cpos] = i; cpos++;
         if(cpos==3){
            un[i]    =  (MathAbs(zz[pos[2]]-zz[pos[1]])/Point) /  // AB
                        (MathAbs(zz[pos[0]]-zz[pos[1]])/Point);   // XA
            double d = get_real_value(un[i],error);
            if(d!=0){
               place_text(DoubleToStr(d,3),(pos[0]+pos[2])/2,(zz[pos[0]]+zz[pos[2]])/2,Crimson);
               create_line(pos[0],pos[2],Gray,zz[pos[0]],zz[pos[2]],0,STYLE_DASHDOT);
               }
               
            pos[0]   = pos[1];
            pos[1]   = pos[2];
            cpos     = 2;
            }
         }
      }

    zz[from] = Close[from];
    pos[cpos] = 0; cpos++;
    if(cpos==3){
      un[from]    =  (MathAbs(zz[pos[2]]-zz[pos[1]])/Point) /  // AB
                  (MathAbs(zz[pos[0]]-zz[pos[1]])/Point);   // XA
      d = get_real_value(un[from],error);
      if(d!=0){
         place_text(DoubleToStr(d,3),(pos[0]+pos[2])/2,(zz[pos[0]]+zz[pos[2]])/2,Crimson);
         create_line(pos[0],pos[2],Gray,zz[pos[0]],zz[pos[2]],0,STYLE_DASHDOT);
         }
      }
   int cp = 0;
   for(i=from; i<barn; i++){ 
      if(un[i]!=0){
         pattern[cp] = un[i];
         position[cp] = i;
         cp++;
         }
      }

//------------------------------------
return(0);  
}

double get_real_value(double v,double err){
   double table[15] = {
      0.382,2.240,
      0.500,2.000,
      0.618,1.618,
      0.707,1.414,
      0.786,1.270,
      0.886,1.129,
      3.140,3.618,
      2.618
      };
   for(int i=0;i<15;i++){
      if(v>=table[i]-err && v<=table[i]+err){
         return (table[i]);
         }
      }
   return (v);
}