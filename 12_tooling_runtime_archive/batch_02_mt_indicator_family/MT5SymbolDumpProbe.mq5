#property strict

input bool InpDumpMarketWatch = true;
input bool InpDumpAllSymbols = true;

string NormalizeToken(string v)
{
   StringReplace(v, " ", "_");
   StringReplace(v, "\\", "_");
   StringReplace(v, "/", "_");
   StringReplace(v, ":", "_");
   StringReplace(v, "*", "_");
   StringReplace(v, "?", "_");
   StringReplace(v, "\"", "_");
   StringReplace(v, "<", "_");
   StringReplace(v, ">", "_");
   StringReplace(v, "|", "_");
   return v;
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

bool WriteSymbolsToFile(string file_name, bool selected)
{
   int fh = FileOpen(file_name, FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(fh == INVALID_HANDLE)
   {
      Print("MT5SymbolDumpProbe: FileOpen failed, err=", GetLastError(), " file=", file_name);
      return false;
   }

   int n = SymbolsTotal(selected);
   for(int i = 0; i < n; i++)
   {
      string name = SymbolName(i, selected);
      FileWriteString(fh, name + "\r\n");
   }
   FileClose(fh);
   return true;
}

int OnInit()
{
   string stamp = NowStamp();
   string server = NormalizeToken(AccountInfoString(ACCOUNT_SERVER));
   long login = AccountInfoInteger(ACCOUNT_LOGIN);
   string suffix = server + "__" + IntegerToString((int)login) + "__" + stamp;

   if(InpDumpMarketWatch)
   {
      WriteSymbolsToFile("mt5_symbols_marketwatch__" + suffix + ".txt", true);
   }
   if(InpDumpAllSymbols)
   {
      WriteSymbolsToFile("mt5_symbols_all__" + suffix + ".txt", false);
   }

   Print("MT5SymbolDumpProbe: DONE");
   ExpertRemove();
   return(INIT_SUCCEEDED);
}

