#coding:utf8

import socket
import threading
import traceback


host = 'localhost'
port = 42345
inString =''
outString = ''
def sendMessage(sock):
    global outString
    while 1:
        try:
            outString = raw_input('Input: ')
            if outString:
                sock.sendall(outString)
        except:
            traceback.print_exc()
            sock.close()

def receiveMessage(sock):
    global inString
    while 1:
        try:
            inString = sock.recv(1024)
            if not inString:
                break
            if outString != inString:
                print inString
        except:
            traceback.print_exc()
            sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))
sm  = threading.Thread(target = sendMessage, args =(sock,))
sm.start()
rm = threading.Thread(target = receiveMessage, args = (sock,))
rm.start()

        
