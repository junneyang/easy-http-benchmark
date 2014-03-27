#!/usr/bin/env python
#-*- coding: utf-8 -*-
from lib.OptParseLib import OptParseLib
import tornado.httpclient
import tornado.ioloop
from tornado import process
import logging
import json
import time
import os
import random
import numpy
from lib.randomList import getRandomData

import brukva
ConfFilePath=u"./conf/easyBenchmarkTestTool.conf"
filepath="./data/testData.txt"
RANDOM_DATA=getRandomData(filepath)

class easyBenchmarkTesttool(object):
    def __init__(self,ClientNUM,TEST_TIME,DataFile):
        self.ClientNUM=ClientNUM
        self.TEST_TIME=TEST_TIME
        self.DataFile=DataFile
        assert(self.DataFile["PROTOCOL_TYPE"] == u"RedisProtocol")

        self._client=brukva.Client(host=DataFile['HOST'], port=DataFile['PORT'],selected_db=DataFile['SELECTED_DB'])
        self._client.connect()
        self._io_loop = self._client.connection._stream.io_loop
    def get_request(self):
        index=random.randrange(0,9988)
        data=RANDOM_DATA[index]
        x=data['x']
        y=data['y']
        logging.info(u"Send New Request")
        self._client.execute_command("GEOSEARCH", self.handle_request, "allpoi" ,"MERCATOR", x, y, "RADIUS","1000","WITHCOORDINATES","WITHDISTANCES")

    def benchmark_test(self):
        for i in xrange(self.ClientNUM):
            self.get_request()
        self.start=time.time()
        self.end=self.start+self.TEST_TIME*60
        self._io_loop.start()

    def handle_request(self,response):
        self.ret=response
        #print(self.ret)
        assert(self.ret)
        logging.info(u"Recv New Response")
        if time.time()>self.end:
            self._client.disconnect()
            self._io_loop.stop()
            return

        self.get_request()


def main():
    options,DataFile=OptParseLib().parse_args()
    ConfFile=json.load(open(ConfFilePath, "r"),encoding='utf-8')
    #print(ConfFile)
    #print(options.ProcessNUM,options.ClientNUM,options.TEST_TIME,DataFile)
    print(u"Start Benchmark Test...")
    if options.ProcessNUM != -1:
        process.fork_processes(options.ProcessNUM)
    logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(asctime)s) <%(message)s>',datefmt='%a,%Y-%m-%d %H:%M:%S',
    filename=ConfFile["LogFilePath"]+str(tornado.process.task_id())+".log",filemode='w')
    easyBC=easyBenchmarkTesttool(options.ClientNUM,options.TEST_TIME,DataFile)
    easyBC.benchmark_test()
    print(u"Benchmark Test End...")


if __name__ == "__main__":
    main()



