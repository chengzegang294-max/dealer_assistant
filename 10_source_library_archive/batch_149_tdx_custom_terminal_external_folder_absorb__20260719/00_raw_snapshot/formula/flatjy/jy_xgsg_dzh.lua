--根据PBMODE判断取哪个字段作为股东代码
function gddm(pbmode, f123, f124)
	if pbmode == "1" then
		return f124
	else
		return f123
	end
end