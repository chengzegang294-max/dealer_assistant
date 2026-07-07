#property strict

input string InpSymbol = "EURUSD";
input int InpTimeframe = PERIOD_M1;
input int InpBars = 3000;
input string InpFileName = "eurusd_export.csv";

string TfToString(int tf)
{
   if(tf==PERIOD_M1) return "M1";
   if(tf==PERIOD_M5) return "M5";
   if(tf==PERIOD_M15) return "M15";
   if(tf==PERIOD_M30) return "M30";
   if(tf==PERIOD_H1) return "H1";
   if(tf==PERIOD_H4) return "H4";
   if(tf==PERIOD_D1) return "D1";
   if(tf==PERIOD_W1) return "W1";
   if(tf==PERIOD_MN1) return "MN1";
   return IntegerToString(tf);
}

void OnStart()
{
   string symbol = InpSymbol;
   int tf = InpTimeframe;
   int bars_total = iBars(symbol, tf);
   if(bars_total <= 0) return;

   int bars_to_export = InpBars;
   if(bars_to_export > bars_total) bars_to_export = bars_total;

   int handle = FileOpen(InpFileName, FILE_CSV|FILE_WRITE|FILE_COMMON, ',');
   if(handle == INVALID_HANDLE) return;

   FileWrite(handle, "Date", "Time", "Open", "High", "Low", "Close", "Volume");

   for(int i = bars_to_export - 1; i >= 0; i--)
   {
      datetime t = iTime(symbol, tf, i);
      string d = TimeToString(t, TIME_DATE);
      string tm = TimeToString(t, TIME_MINUTES);
      double o = iOpen(symbol, tf, i);
      double h = iHigh(symbol, tf, i);
      double l = iLow(symbol, tf, i);
      double c = iClose(symbol, tf, i);
      long v = iVolume(symbol, tf, i);
      FileWrite(handle, d, tm, DoubleToString(o, Digits), DoubleToString(h, Digits), DoubleToString(l, Digits), DoubleToString(c, Digits), IntegerToString((int)v));
   }

   FileClose(handle);
}

