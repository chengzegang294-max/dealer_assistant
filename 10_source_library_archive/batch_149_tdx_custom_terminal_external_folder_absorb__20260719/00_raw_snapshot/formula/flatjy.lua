

--当日成交买入金额
function buyamount(F130,F154)
	if F130 == "0" or F130 == "15" or F130 == "69"then
		return F154
	else
		return 0
	end
end

--当日成交卖出金额
function sellamount(F130,F154)
	if F130 == "1" or F130 == "16" or F130 == "70" then
		return F154
	else
		return 0
	end
end




--行情市场
function hqsc(F125)
	if F125 == "12" or F125 == "60" then
		return 44
	elseif F125 == "1" then
		return 1
	elseif F125 == "0" then
		return 0
	elseif F125 == "2" then
		return 0
	elseif F125 == "3" then
		return 1
	elseif F125 == "40" or F125 == "41" then
		return 71
	elseif F125 == "21" then
		return 28
	elseif F125 == "23" then
		return 29
	elseif F125 == "22" then
		return 30
	elseif F125 == "26" then
		return 47
	elseif F125 == "37" then
		return 8
	elseif F125 == "42" then
		return 9	
	elseif F125 == "43" then
		return 66	
	else
		return 44
	end
end

--交易市场
function jysc(F125)
	if F125 == "40" then
		return "沪港通"
	elseif F125 == "41" then
		return "深港通"
	else
		return F125
	end
end





--期货持仓盈亏
function ccyk(F736,F130,now,F520,F704,F200,F1227)
	if F736 == "今仓" and F130 == "买入" then
		return (now-F520)* F200*F1227		
	elseif F736 == "今仓" and F130 == "卖出" then
		return (F520-now)* F200*F1227	
	elseif F736 == "昨仓" and F130 == "买入" then
		return (now-F704)* F200*F1227		
	elseif F736 == "昨仓" and F130 == "卖出" then
		return (F704-now)* F200*F1227
	else
		return "--"		
	end
end



--期货逐笔盈亏
function zbyk(F130,now,F520,F200,F1227)
	if F130 == "买入" then
		return (now-F520)* F200*F1227		
	elseif F130 == "卖出" then
		return (F520-now)* F200*F1227	
	else
		return "--"		
	end
end


--期货持仓均价
function cbj(F736,F520,F704)
	if F736 == "今仓" then
		return F520	
	else
		return F704		
	end
end


--期货昨仓
function zc(F736,F200)
	if F736 == "昨仓" then
		return F200	
	else
		return 0	
	end
end

--期货今仓
function jc(F736,F200)
	if F736 == "今仓" then
		return F200	
	else
		return 0	
	end
end

--根据PBMODE判断取哪个字段作为股东代码
function gddm(pbmode, f123, f124)
	if pbmode == "1" then
		return f124
	else
		return f123
	end
end







--质押入库计算
function incalc(exchangename, incount)
	if exchangename == "上海证券交易所" then
		incount = incount * 10
		return string.format("%d", incount)
	elseif exchangename == "深圳证券交易所" then
		return string.format("%d", incount)
	else
		return "--"
	end	  
end




