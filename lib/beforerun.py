import os

sp = os.path.sep

token = ""
prefix = ""

def varset(): # 변수 설정
    global token
    global prefix

    tokenfile = open("res"+sp+"security"+sp+"token.txt", "r")
    token = tokenfile.read()
    tokenfile.close()

    prefile = open("res"+sp+"prefix.txt", "r")
    prefix = prefile.read()
    prefile.close()