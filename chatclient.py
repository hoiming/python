#coding:utf8

import socket
import threading
import traceback
import Queue
import sys

class ChatClient(object):

    def __init__(self):
        '''
        初始化
        '''
        self.host = 'localhost'
        self.port = 32345
        self.queue = Queue.Queue()
        self.outString = ''
        self.inString =''
    def sendMessage(self,sock):
        while 1:
            try:
                self.outString = raw_input('Input: ')
                if self.outString:
                    sock.sendall(self.outString)
                    self.queue.put(self.outString)
            except:
                traceback.print_exc()
                sock.close()
                

    def receiveMessage(self,sock):
        while 1:
            try:
                self.inString = sock.recv(1024)
                if not self.inString:
                    raise
                if self.inString != self.outString:
                    print self.inString
            except:
                traceback.print_exc()
                sock.close()
                break

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host,self.port))
        sm  = threading.Thread(target = self.sendMessage, args =(sock,))
        sm.start()
        rm = threading.Thread(target = self.receiveMessage, args = (sock,))
        rm.start()
        self.queue.put("")

if __name__ == '__main__':
    chatClient = ChatClient()
    chatClient.run()
        
