#-*- coding: utf-8 -*-
import pdb

def readIni(filename):
    '''
    读取以filename为文件名的文件，等号左边的作为键，等号右边的作为值，返回
    一个dict
    '''
#    pdb.set_trace()
    try:
        with open(filename) as f:
            lines = f.readlines()
            #存放结果
            inidict = {}
            tlist = []
            sectionName = None
            for line in lines:
                line = line.strip()
                if not line:
                    #空行
                    continue
                #忽略注释
                if line.find(';') != -1:
                    line = line[:line.find(';')]
                #处理section
                if line.startswith('[') and line.endswith(']'):
                    if not sectionName:
                        #文件的开头
                        sectionName = line.strip('[').strip(']')
                        continue
                    else:
                        #处理完一个section
                        tmpdict = {sectionName:dict(tlist)}
                        inidict.update(tmpdict)
                        sectionName = line.strip('[').strip(']')
                        tlist = []
                else:
                    #section里面的键值对
                    pair = line.split('=',1)
                    tup = pair[0].strip(),pair[1].strip()
                    tlist.append(tup)

            #只有一个section的情况
            if sectionName:
                tmpdict = {sectionName:dict(tlist)}
                inidict.update(tmpdict)
            return inidict
    except Exception,e:
        print e
       
if __name__ == '__main__':
    print readIni('haha.ini')
