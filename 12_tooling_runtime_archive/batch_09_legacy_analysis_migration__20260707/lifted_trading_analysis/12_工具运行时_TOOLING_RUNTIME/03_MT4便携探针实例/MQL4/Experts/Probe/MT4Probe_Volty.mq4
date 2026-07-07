#property strict

extern string IndicatorName = "Probe\\VoltyChannel_Stop_v2_1M";
extern int ProbeTimeframe = 240;
extern int MaxModes = 8;
extern int MaxShifts = 50;
extern bool DumpSeries = false;
extern int DumpModeStart = 0;
extern int DumpModeEnd = -1;

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

int OpenProbeFile(string file_name, bool &used_common)
{
   used_common = false;
   ResetLastError();
   int fh = FileOpen(file_name, FILE_CSV|FILE_WRITE);
   if(fh >= 0) return(fh);

   int err_local = GetLastError();
   Print("MT4Probe_Volty: local FileOpen failed err=", err_local, " file=", file_name);

   ResetLastError();
   fh = FileOpen(file_name, FILE_CSV|FILE_WRITE|FILE_COMMON);
   if(fh >= 0)
   {
      used_common = true;
      return(fh);
   }

   Print("MT4Probe_Volty: common FileOpen failed err=", GetLastError(), " file=", file_name);
   return(-1);
}

void RunProbe()
{
   static bool done = false;
   if(done) return;
   done = true;

   Print("MT4Probe_Volty: RunProbe begin symbol=", Symbol(), " chart_tf=", Period(), " indicator_tf=", ProbeTimeframe);

   string stamp = TimeToStr(TimeCurrent(), TIME_DATE|TIME_SECONDS);
   StringReplace(stamp, ".", "");
   StringReplace(stamp, ":", "");
   StringReplace(stamp, " ", "_");
   string file_name = "MT4_probe_Volty_" + Symbol() + "_" + TfLabel(ProbeTimeframe) + "_" + stamp + ".csv";

   bool used_common = false;
   int fh = OpenProbeFile(file_name, used_common);
   if(fh < 0) return;

   Print("MT4Probe_Volty: FileOpen ok file=", file_name, " common=", used_common);

   FileWrite(fh, "symbol", Symbol());
   FileWrite(fh, "chart_tf", Period());
   FileWrite(fh, "indicator_tf", ProbeTimeframe);
   FileWrite(fh, "indicator_name", IndicatorName);
   FileWrite(fh, "max_modes", MaxModes);
   FileWrite(fh, "max_shifts", MaxShifts);
   FileWrite(fh, "used_common", used_common ? 1 : 0);

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

   if(DumpSeries)
   {
      int start_mode = DumpModeStart;
      if(start_mode < 0) start_mode = 0;
      if(start_mode >= MaxModes) start_mode = MaxModes - 1;
      int end_mode = DumpModeEnd;
      if(end_mode < 0) end_mode = start_mode;
      if(end_mode >= MaxModes) end_mode = MaxModes - 1;
      if(end_mode < start_mode) end_mode = start_mode;

      for(int mode = start_mode; mode <= end_mode; mode++)
      {
         for(int shift = 0; shift < MaxShifts; shift++)
         {
            ResetLastError();
            double v = iCustom(NULL, ProbeTimeframe, IndicatorName, mode, shift);
            int err = GetLastError();
            datetime t = iTime(NULL, ProbeTimeframe, shift);
            FileWrite(
               fh,
               "series", 1,
               "mode", mode,
               "shift", shift,
               "bar_time", TimeToStr(t, TIME_DATE|TIME_SECONDS),
               "value", DoubleToStr(v, 8),
               "err", err
            );
         }
      }
   }

   FileWrite(fh, "status", "DONE");
   FileClose(fh);
   Print("MT4Probe_Volty: DONE file=", file_name, " common=", used_common);
}

int OnInit()
{
   RunProbe();
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
}

void OnTick()
{
   RunProbe();
}
