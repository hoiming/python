# -*- coding: UTF-8 -*-
import os
def fileList():
    
    lst = list()
    for dirpath,dirnames,filenames in os.walk('.'):
        #print "Directory",dirpath
        for filename in filenames:
            if filename.endswith(".java"):
               # print dirpath+"\\"+filename
                lst.append(  dirpath+"\\"+filename)
    return  lst
#获取java文件列表
lst = fileList()
teststr = ".\\src\\com\\haiming\\interview\\QuestionFourTest.java"
#print teststr

def process(filePath,charset):
    newlines = []
    with open(filePath,'r') as f:
        lines = f.readlines()
        for line in lines:
	    try:
                s = line.decode(charset)
		except UnicodeError:
		    print "Source file's encoding is not %s." % charset
		    continue
           	s = s.encode('UTF-8')
             newlines.append(s)

    #write to ouput file
    with open(filePath,'w+') as f:
        f.writelines(newlines)
for f in lst:
    print f
    process(f,"GBK")

