#property strict

input string InpSymbol = "EURUSD";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M1;
input int InpBars = 3000;
input string InpFileName = "eurusd_export_utc.csv";

datetime ToUtc(datetime t_server)
{
   long offset = (long)(TimeCurrent() - TimeGMT());
   return (t_server - offset);
}

void OnStart()
{
   string symbol = InpSymbol;
   ENUM_TIMEFRAMES tf = InpTimeframe;

   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   int copied = CopyRates(symbol, tf, 0, InpBars, rates);
   if(copied <= 0) return;

   int handle = FileOpen(InpFileName, FILE_CSV|FILE_WRITE|FILE_COMMON, ',');
   if(handle == INVALID_HANDLE) return;

   FileWrite(handle, "Time (UTC)", "Open", "High", "Low", "Close", "TickVolume");

   for(int i = copied - 1; i >= 0; i--)
   {
      datetime t_utc = ToUtc(rates[i].time);
      string ts = TimeToString(t_utc, TIME_DATE|TIME_MINUTES);
      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      FileWrite(handle,
                ts,
                DoubleToString(rates[i].open, digits),
                DoubleToString(rates[i].high, digits),
                DoubleToString(rates[i].low, digits),
                DoubleToString(rates[i].close, digits),
                IntegerToString((int)rates[i].tick_volume));
   }

   FileClose(handle);
}

