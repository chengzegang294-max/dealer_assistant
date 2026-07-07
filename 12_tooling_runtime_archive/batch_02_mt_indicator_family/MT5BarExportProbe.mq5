#property strict

input bool InpUseCommonFiles = true;
input string InpFilePrefix = "MT5_bars_export";
input ENUM_TIMEFRAMES InpExportTf = PERIOD_M15;

string TimeframeLabel(ENUM_TIMEFRAMES tf)
{
   switch(tf)
   {
      case PERIOD_M1: return "M1";
      case PERIOD_M5: return "M5";
      case PERIOD_M15: return "M15";
      case PERIOD_M30: return "M30";
      case PERIOD_H1: return "H1";
      case PERIOD_H4: return "H4";
      case PERIOD_D1: return "D1";
   }
   return IntegerToString((int)tf);
}

string NowStamp()
{
   datetime t = TimeCurrent();
   string stamp = TimeToString(t, TIME_DATE | TIME_MINUTES | TIME_SECONDS);
   StringReplace(stamp, ".", "");
   StringReplace(stamp, ":", "");
   StringReplace(stamp, " ", "_");
   ulong run_id = GetMicrosecondCount();
   return stamp + "__" + StringFormat("%I64u", run_id);
}

void ExportBars()
{
   static bool exported = false;
   if(exported)
      return;
   exported = true;

   ENUM_TIMEFRAMES tf = InpExportTf;
   if(tf == PERIOD_CURRENT)
      tf = (ENUM_TIMEFRAMES)_Period;
   int total_bars = Bars(_Symbol, tf);
   if(total_bars <= 0)
   {
      Print("MT5BarExportProbe: Bars failed, err=", GetLastError(), " export_tf=", EnumToString(tf), " chart_tf=", EnumToString((ENUM_TIMEFRAMES)_Period));
      return;
   }

   MqlRates rates[];
   ResetLastError();
   int copied = CopyRates(_Symbol, tf, 0, total_bars, rates);
   int copy_err = GetLastError();
   if(copied <= 0)
   {
      Print("MT5BarExportProbe: CopyRates failed, err=", copy_err, " total_bars=", total_bars, " export_tf=", EnumToString(tf), " chart_tf=", EnumToString((ENUM_TIMEFRAMES)_Period));
      return;
   }

   string file_name = InpFilePrefix + "_" + _Symbol + "_" + TimeframeLabel(tf) + "_" + NowStamp() + ".csv";
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
   if(InpUseCommonFiles)
      flags |= FILE_COMMON;

   int fh = FileOpen(file_name, flags);
   if(fh == INVALID_HANDLE)
   {
      Print("MT5BarExportProbe: FileOpen failed, err=", GetLastError(), " file=", file_name);
      return;
   }

   FileWrite(fh, "Date", "Time", "Open", "High", "Low", "Close", "TickVolume", "Spread", "RealVolume");
   for(int i = copied - 1; i >= 0; i--)
   {
      MqlRates rate = rates[i];
      FileWrite(
         fh,
         TimeToString(rate.time, TIME_DATE),
         TimeToString(rate.time, TIME_MINUTES),
         DoubleToString(rate.open, _Digits),
         DoubleToString(rate.high, _Digits),
         DoubleToString(rate.low, _Digits),
         DoubleToString(rate.close, _Digits),
         IntegerToString((int)rate.tick_volume),
         IntegerToString((int)rate.spread),
         IntegerToString((int)rate.real_volume)
      );
   }

   FileClose(fh);
   Print("MT5BarExportProbe: DONE file=", file_name, " copied=", copied, " bars=", total_bars, " export_tf=", EnumToString(tf), " chart_tf=", EnumToString((ENUM_TIMEFRAMES)_Period));
}

int OnInit()
{
   return(INIT_SUCCEEDED);
}

void OnTick()
{
}

void OnDeinit(const int reason)
{
   Print("MT5BarExportProbe: OnDeinit reason=", IntegerToString(reason));
   ExportBars();
}
