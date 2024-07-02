import os

sp = os.path.sep

token = ""
myid = ""
ttsin = ""
ttsout = ""
prefix = ""

def varset(): # 변수 설정
    global token
    global myid
    global ttsin
    global ttsout
    global prefix

    tokenfile = open("res"+sp+"security"+sp+"token.txt", "r")
    token = tokenfile.read()
    tokenfile.close()

    idfile = open("res"+sp+"security"+sp+"myid.txt", "r")
    myid = idfile.read()
    idfile.close()

    ttsinputfile = open("res"+sp+"security"+sp+"ttsinput.txt", "r")
    ttsin = ttsinputfile.read()
    ttsinputfile.close()

    ttsoutputfile = open("res"+sp+"security"+sp+"ttsoutput.txt", "r")
    ttsout = ttsoutputfile.read()
    ttsoutputfile.close()

    prefile = open("res"+sp+"prefix.txt", "r")
    prefix = prefile.read()
    prefile.close()