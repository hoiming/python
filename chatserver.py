#coding:utf-8
import socket, traceback
import threading
import Queue

class ChatServer(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 32345
        self.que = Queue.Queue()
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.bind((self.host,self.port))
        self.sk.listen(10)
        self.socketlist = []
        print 'Server is up'

    def clientThreadIn(self,conn):
        '''
        接收数据
        '''
        data = ''
        while 1:            
            try:
                data = conn.recv(1024)
                if not data:
                    conn.close()
                    break
                self.que.put(data)
                print data
            except:
                traceback.print_exc()
                data = conn.getpeername()[0] + ' disconnect'
                self.que.put(data)
                self.socketlist.remove(conn)
                
                print data
                break

    def clientThreadOut(self):
        '''
        发送数据
        '''
        #从队列中取出一条消息
        while 1:
            try:
                
                data = self.que.get()
                for sk in list(self.socketlist):
                    sk.sendall(data)
            except:
                traceback.print_exc()
      
    def run(self):

        #发送消息的线程
        threading.Thread(target = self.clientThreadOut).start()
        while 1:
            try:
                '''
                接收连接，启动线程
                '''
                conn,addr = self.sk.accept()
                print 'Connected with ' + addr[0] + ':' + str(addr[1])
                data = conn.getpeername()[0] + ' is in the room.'
                self.que.put(data)
                print data
                threading.Thread(target = self.clientThreadIn, args = (conn,)).start()
                self.socketlist.append(conn)

            except:
                traceback.print_exc()
                self.sk.close()
                print 'socket is closed'
        
        

if __name__ == '__main__':
    chatServer = ChatServer()
    chatServer.run()


