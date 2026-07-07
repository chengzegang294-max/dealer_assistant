#property strict

input string InpSymbol = "EURUSD";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M1;
input int InpBars = 3000;
input string InpFileName = "eurusd_export.csv";

string TfToString(ENUM_TIMEFRAMES tf)
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
   return IntegerToString((int)tf);
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

   FileWrite(handle, "Date", "Time", "Open", "High", "Low", "Close", "TickVolume");

   for(int i = copied - 1; i >= 0; i--)
   {
      datetime t = rates[i].time;
      string d = TimeToString(t, TIME_DATE);
      string tm = TimeToString(t, TIME_MINUTES);
      FileWrite(handle,
                d,
                tm,
                DoubleToString(rates[i].open, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)),
                DoubleToString(rates[i].high, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)),
                DoubleToString(rates[i].low, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)),
                DoubleToString(rates[i].close, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)),
                IntegerToString((int)rates[i].tick_volume));
   }

   FileClose(handle);
}

