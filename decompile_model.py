import tcutil


def decompile(filename):
    with open(filename, "r") as file:
        data = tcutil.evaldata(file.read())
        for itm, val in data.items():
            print(dict(val))

#test
decompile(tcutil.cwd + "res\\models\\model\\asset\\temple_big_01.mdl")