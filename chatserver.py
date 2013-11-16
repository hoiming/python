#coding:utf-8
import socket, traceback
import threading


host = 'localhost'
port = 42345
condition = threading.Condition()
data = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)
print 'Server is up'

def clientThreadIn(conn):
    '''
    从客户端接收数据，更新data
    '''
    global data
    while 1:
        try:
            temp = conn.recv(1024)
            if not temp:
                conn.close()
                return
            NotifyAll(temp)
            print data
        except:
            NotifyAll(conn.getpeername()[0] + ' disconnect')
            print data
            return

def NotifyAll(message):
    '''
    更新当前的数据，唤醒所有等待的线程
    '''
    global data
    if condition.acquire():
        data = message
        condition.notifyAll()
        condition.release()

def clientThreadOut(conn):
    '''
    获得锁，等待数据
    '''
    global data
    while 1:
        if condition.acquire():
            condition.wait()
            if data:
                try:
                    conn.sendall(data)
                    condition.release()
                except:
                    condition.release()
                    return

while 1:
    try:
        '''
        接收连接，启动线程
        '''
        conn,addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        NotifyAll(conn.getpeername()[0] + ' is in the room.')
        print data
        threading.Thread(target = clientThreadIn, args = (conn,)).start()
        threading.Thread(target = clientThreadOut, args = (conn, )).start()

    except:
        traceback.print_exc()
        s.close()
        print 'socket is closed'


