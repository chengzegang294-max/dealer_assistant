#property strict

extern string IndicatorName = "Probe\\VoltyChannel_Stop_v2_1M";
extern int ProbeTimeframe = 60;
extern int MaxModes = 8;
extern int MaxShifts = 50;

string TfLabel(int tf)
{
   if(tf == 1) return("M1");
   if(tf == 5) return("M5");
   if(tf == 15) return("M15");
   if(tf == 30) return("M30");
   if(tf == 60) return("H1");
   if(tf == 240) return("H4");
   if(tf == 1440) return("D1");
   return(IntegerToString(tf));
}

int init()
{
   return(0);
}

int deinit()
{
   return(0);
}

int start()
{
   static bool done = false;
   if(done) return(0);
   done = true;

   string stamp = TimeToStr(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   StringReplace(stamp, ".", "");
   StringReplace(stamp, ":", "");
   StringReplace(stamp, " ", "_");
   string file_name = "MT4_probe_Volty_" + Symbol() + "_" + TfLabel(ProbeTimeframe) + "_" + stamp + ".csv";

   int fh = FileOpen(file_name, FILE_CSV|FILE_WRITE);
   if(fh < 0)
   {
      Print("MT4Probe_Volty: FileOpen failed err=", GetLastError());
      return(0);
   }

   FileWrite(fh, "symbol", Symbol());
   FileWrite(fh, "chart_tf", Period());
   FileWrite(fh, "indicator_tf", ProbeTimeframe);
   FileWrite(fh, "indicator_name", IndicatorName);
   FileWrite(fh, "max_modes", MaxModes);
   FileWrite(fh, "max_shifts", MaxShifts);

   for(int mode = 0; mode < MaxModes; mode++)
   {
      int err_count = 0;
      int non_empty = 0;
      double first_valid = EMPTY_VALUE;
      double last_valid = EMPTY_VALUE;

      for(int shift = 0; shift < MaxShifts; shift++)
      {
         ResetLastError();
         double v = iCustom(NULL, ProbeTimeframe, IndicatorName, mode, shift);
         int err = GetLastError();
         if(err != 0) err_count++;
         if(v != EMPTY_VALUE)
         {
            non_empty++;
            if(first_valid == EMPTY_VALUE) first_valid = v;
            last_valid = v;
         }
      }

      FileWrite(
         fh,
         "mode", mode,
         "non_empty", non_empty,
         "err_count", err_count,
         "first_valid", DoubleToStr(first_valid, 8),
         "last_valid", DoubleToStr(last_valid, 8)
      );
   }

   FileWrite(fh, "status", "DONE");
   FileClose(fh);
   Print("MT4Probe_Volty: DONE");
   return(0);
}
