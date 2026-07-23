--买入金额
function buyamount(deal, amount)
	if deal == "0" or deal == "15" or deal == "69"then
		return amount
	else
		return 0
	end
end

--卖出金额
function sellamount(deal, amount)
	if deal == "1" or deal == "16" or deal == "70" then
		return amount
	else
		return 0
	end
end

--市场标志
function scbz(scbz)
	if scbz == "12" or scbz == "60" then
		return 44
	elseif scbz == "1" then
		return 1
	elseif scbz == "0" then
		return 0
	elseif scbz == "2" then
		return 0
	elseif scbz == "3" then
		return 1
	else
		return 44
	end
end