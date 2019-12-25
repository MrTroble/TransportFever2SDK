import sys
from PySide2 import QtCore, QtWidgets, QtGui
import asyncio
import os
import os.path
import re
import tcutil

app = QtWidgets.QApplication([])

language = {}
modinfo = {}

class MainWidg(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Starting the tools...")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

    def loadedmodinfo(self):
        global modinfo
        self.text.setText(modinfo["name"] + "\n" + modinfo["description"])
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(tcutil.cwd + "res\\")
        tree = QtWidgets.QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(tcutil.cwd + "res\\"))
        self.layout.addWidget(tree)

widget = MainWidg()

def stage(info):
    widget.text.setText(info)
    print(info)

def replacelangs(content):
    global language
    if not 'en' in language.keys():
        return content
    lang = language["en"]
    for itm, val in lang.items():
        if type(val) is str:
            val = '"' + val + '"'
        content = content.replace("_(\"" + itm +"\")", val)
    return content

async def startup():
    global language
    global modinfo

    stage("Checking project files")
    # check if a mod exist
    modpath = tcutil.cwd + "mod.lua"
    stringpath = tcutil.cwd + "strings.lua"
    if os.path.exists(modpath):
        stage("Check and load language files")
        # load languages
        if os.path.exists(stringpath):
            with open(stringpath, "r") as langfile:
                enlang = tcutil.evaldata(langfile.read())
                language = dict(enlang)
                for itm, val in enlang.items():
                    language[itm] = dict(val)

        stage("Checking mod.lua")
        # check the integrety of the mod.lua
        with open(modpath, "r") as modfile:
            content = modfile.read()
            content = replacelangs(content)
            modinfo = dict(tcutil.evaldata(content)["info"])
        
        stage("Loading complete: " + modinfo["name"])
        widget.loadedmodinfo()
        return
    else:
        stage("No mod found!\nCreate one:")
        return

widget.resize(800, 600)
widget.show()

asyncio.run(startup())

sys.exit(app.exec_())