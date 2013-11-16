# -*- coding: utf-8 -*-
import MySQLdb
import logging
import os

class Mysqltest(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user='haiming',\
                                    passwd='123456',db='test',charset='utf8')
        self.cur = self.conn.cursor()
        self.init_logger()
    def init_logger(self):
        '''
        初始化logger
        向终端和文件输出日志
        '''
        self.logger = logging.getLogger('myself.logger')
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler('log.txt')
        self.fh.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
        self.logger.info('aaaa')


    def init_table(self):
        '''
        创建一个表
        '''

        try:
            sql = "CREATE TABLE `user` (`id` int(11)\
NOT NULL AUTO_INCREMENT,`name` varchar(50) NOT NULL,\
`age` int(11) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB \
AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 ;";
            self.cur.execute(sql)
            self.logger.debug(sql)

        except Exception,e:
            self.logger.error('table already exists.')

    def insert(self):
        '''
        插入数据
        '''
        value =  '哈哈哈',24 
        sql = 'insert into user (name,age) values ("%s",%s)' % value
        self.logger.debug(sql)
        self.cur.execute(sql)


    def select(self):
        '''
        查找和输出数据
        '''
        sql = 'select * from user'
        self.logger.debug(sql)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        for r in result:
            print r[0],r[1],r[2]


    def delete(self,id):

        '''
        删除数据
        '''
        self.cur = self.conn.cursor()
        sql = 'delete from user where id=%s'  % id
        self.logger.debug(sql)
        result = self.cur.execute(sql)
        if result == 1:
            self.logger.debug( 'record with id %s deleted' % id)
        else:
            self.logger.error( 'No matched record founded')

    def beginTransaction(self):
        self.logger.debug('Begin Transaction')
        pass
    def commitTransaction(self):
        self.logger.debug('Commit Transaction')
        self.conn.commit()


    def rollbackTransaction(self):
        self.logger.debug('Roll Back Transaction')
        self.conn.rollback()

    def closeConnection(self):
        self.cur.close()
        self.conn.close()
        self.logger.info('Connection closed')
    def closeLogger(self):
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)
        self.ch.flush()
        self.fh.flush()
        logging.shutdown()

if __name__ == '__main__':

    test = Mysqltest()  
    test.init_table()
    test.beginTransaction()
    test.insert()
    test.insert()
    test.insert()
    
    test.commitTransaction()
    test.closeConnection()
    test.closeLogger()

