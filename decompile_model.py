import tcutil


def decompile(filename):
    with open(filename, "r") as file:
        data = tcutil.evaldata(file.read())
        data[]

#test
decompile(tcutil.cwd + "res\\models\\model\\asset\\temple_big_01.mdl")