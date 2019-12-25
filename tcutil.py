from lupa import LuaRuntime
import re
import os

cwd = os.getcwd() + "\\..\\"

lua = LuaRuntime(unpack_returned_tuples=True)
#regex storage
datafunctionre = re.compile(r"function data\(\)[\s\w\W]*end", re.M)

def evaldata(content):
    datafnc = datafunctionre.search(content).group(0)
    if datafnc == None:
        return None
    datafnc = datafnc.replace("data()", "()")
    fnc = lua.eval(datafnc)
    return fnc()
