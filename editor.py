import sys
from PySide2 import QtCore, QtWidgets, QtGui
import asyncio
from lupa import LuaRuntime
import os
import os.path
import re

app = QtWidgets.QApplication([])
lua = LuaRuntime(unpack_returned_tuples=True)
cwd = os.getcwd() + "\\..\\"

class MainWidg(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Starting the tools...")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

widget = MainWidg()

#regex storage
datafunctionre = re.compile(r"function data\(\)[\s\w\W]*end", re.M)

def stage(info):
    widget.text.setText(info)
    print(info)

def evaldata(content):
    datafnc = datafunctionre.search(content).group(0)
    if datafnc == None:
        stage("Error parsing content of data method!")
        return None
    datafnc = datafnc.replace("data()", "()")
    fnc = lua.eval(datafnc)
    return fnc()

language = {}

async def startup():
    stage("Checking project files")
    # check if a mod exist
    modpath = cwd + "mod.lua"
    stringpath = cwd + "strings.lua"
    if os.path.exists(modpath):
        stage("Check and load language files")
        # load languages
        if os.path.exists(stringpath):
            with open(stringpath, "r") as langfile:
                enlang = evaldata(langfile.read())["en"]
                for itm, val in enlang.items():
                    language[itm] = val
                    lua.execute(str(itm) + " = \"" + str(val) + "\"") 

        stage("Checking mod.lua")
        # check the integrety of the mod.lua
        with open(modpath, "r") as modfile:
            content = modfile.read()
            
    else:
        stage("No mod found!\nCreate one:")
        return

widget.resize(800, 600)
widget.show()

asyncio.run(startup())

sys.exit(app.exec_())