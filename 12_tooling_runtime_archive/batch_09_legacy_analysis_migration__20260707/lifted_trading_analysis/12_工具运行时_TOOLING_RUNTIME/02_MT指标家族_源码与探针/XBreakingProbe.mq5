#property strict

input string InpIndicatorName = "XBreaking";
input ENUM_TIMEFRAMES InpIndicatorTf = PERIOD_H1;
input int InpBarsToProbe = 200;
input int InpMaxBuffers = 8;

string ProbeTimeframeLabel(ENUM_TIMEFRAMES tf)
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

void WriteLine(int fh, string k, string v)
{
   FileWrite(fh, k, v);
}

int OnInit()
{
   return(INIT_SUCCEEDED);
}

void OnTick()
{
   static bool done = false;
   if(done)
   {
      ExpertRemove();
      return;
   }
   done = true;

   string stamp = TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES | TIME_SECONDS);
   StringReplace(stamp, ".", "");
   StringReplace(stamp, ":", "");
   StringReplace(stamp, " ", "_");
   string file_name = "XBreaking_probe_" + _Symbol + "_" + ProbeTimeframeLabel(InpIndicatorTf) + "_" + stamp + ".csv";
   int fh = FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_COMMON);
   if(fh == INVALID_HANDLE)
   {
      Print("XBreakingProbe: FileOpen failed, err=", GetLastError());
      ExpertRemove();
      return;
   }

   WriteLine(fh, "symbol", _Symbol);
   WriteLine(fh, "chart_tf", EnumToString((ENUM_TIMEFRAMES)_Period));
   WriteLine(fh, "indicator_tf", EnumToString(InpIndicatorTf));
   WriteLine(fh, "indicator_name", InpIndicatorName);
   WriteLine(fh, "bars_to_probe", IntegerToString(InpBarsToProbe));
   WriteLine(fh, "max_buffers", IntegerToString(InpMaxBuffers));

   ResetLastError();
   int handle = iCustom(_Symbol, InpIndicatorTf, InpIndicatorName);
   int init_err = GetLastError();
   WriteLine(fh, "handle", IntegerToString(handle));
   WriteLine(fh, "init_err", IntegerToString(init_err));

   if(handle == INVALID_HANDLE)
   {
      WriteLine(fh, "status", "INVALID_HANDLE");
      FileClose(fh);
      Print("XBreakingProbe: INVALID_HANDLE err=", init_err);
      ExpertRemove();
      return;
   }

   for(int b = 0; b < InpMaxBuffers; b++)
   {
      double vals[];
      ArraySetAsSeries(vals, true);
      ResetLastError();
      int copied = CopyBuffer(handle, b, 0, InpBarsToProbe, vals);
      int err = GetLastError();
      int non_empty = 0;
      double first_valid = EMPTY_VALUE;
      double last_valid = EMPTY_VALUE;

      if(copied > 0)
      {
         for(int i = 0; i < copied; i++)
         {
            double v = vals[i];
            if(v != EMPTY_VALUE)
            {
               non_empty++;
               if(first_valid == EMPTY_VALUE)
                  first_valid = v;
               last_valid = v;
            }
         }
      }

      FileWrite(
         fh,
         "buffer",
         IntegerToString(b),
         "copied",
         IntegerToString(copied),
         "err",
         IntegerToString(err),
         "non_empty",
         IntegerToString(non_empty),
         "first_valid",
         DoubleToString(first_valid, 8),
         "last_valid",
         DoubleToString(last_valid, 8)
      );
   }

   IndicatorRelease(handle);
   WriteLine(fh, "status", "DONE");
   FileClose(fh);
   Print("XBreakingProbe: DONE");
   ExpertRemove();
}
