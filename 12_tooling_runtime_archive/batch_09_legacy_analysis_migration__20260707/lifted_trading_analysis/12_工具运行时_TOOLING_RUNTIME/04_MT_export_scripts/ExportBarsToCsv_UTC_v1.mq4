#property strict

input string InpSymbol = "EURUSD";
input int InpTimeframe = PERIOD_M1;
input int InpBars = 3000;
input string InpFileName = "eurusd_export_utc.csv";

datetime ToUtc(datetime t_server)
{
   int offset = (int)(TimeCurrent() - TimeGMT());
   return (t_server - offset);
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

   FileWrite(handle, "Time (UTC)", "Open", "High", "Low", "Close", "Volume");

   for(int i = bars_to_export - 1; i >= 0; i--)
   {
      datetime t = iTime(symbol, tf, i);
      datetime t_utc = ToUtc(t);
      string ts = TimeToString(t_utc, TIME_DATE|TIME_MINUTES);
      double o = iOpen(symbol, tf, i);
      double h = iHigh(symbol, tf, i);
      double l = iLow(symbol, tf, i);
      double c = iClose(symbol, tf, i);
      long v = iVolume(symbol, tf, i);
      FileWrite(handle, ts, DoubleToString(o, Digits), DoubleToString(h, Digits), DoubleToString(l, Digits), DoubleToString(c, Digits), IntegerToString((int)v));
   }

   FileClose(handle);
}

