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
ConfFilePath=u"./conf/easyBenchmarkTestTool.conf"

class easyBenchmarkTesttool(object):
    def __init__(self,ClientNUM,TEST_TIME,DataFile):
        self.ClientNUM=ClientNUM
        self.TEST_TIME=TEST_TIME
        self.DataFile=DataFile
        self._io_loop =tornado.ioloop.IOLoop()
        if(self.DataFile["PROTOCOL_TYPE"] == u"HTTP_POST_JSON" or self.DataFile["PROTOCOL_TYPE"] == u"HTTP_GET"):
            self._client=tornado.httpclient.AsyncHTTPClient(self._io_loop,max_clients=self.ClientNUM)

    def get_request(self):
        #could add choice to select random request in a sequence
        #testdata= random.choice(testdata)
        if(self.DataFile["PROTOCOL_TYPE"] == u"HTTP_POST_JSON"):
            url=self.DataFile["URL"]
            headers=self.DataFile["HEADERS"]
            body=self.DataFile["BODY"]
            if(len(body)==1):
                body=body[0]
            else:
                body=random.choice(body)
            body=json.JSONEncoder().encode(body)
            httprequest_post = tornado.httpclient.HTTPRequest(url=url,
            headers=headers,method="POST",body=body,connect_timeout=self.DataFile["CONNECTION_TMOUT"],request_timeout=self.DataFile["REQUEST_TMOUT"])
            logging.info(u"Send New Request")
            return httprequest_post
        elif(self.DataFile["PROTOCOL_TYPE"] == u"HTTP_GET"):
            url=self.DataFile["URL"]
            if(len(url)==1):
                url=url[0]
            else:
                url=random.choice(url)
            httprequest_get=tornado.httpclient.HTTPRequest(url=url,
            connect_timeout=self.DataFile["CONNECTION_TMOUT"],request_timeout=self.DataFile["REQUEST_TMOUT"])
            logging.info(u"Send New Request")
            return httprequest_get

    def benchmark_test(self):
        for i in xrange(self.ClientNUM):
            self._client.fetch(self.get_request(), self.handle_request)
        self.start=time.time()
        self.end=self.start+self.TEST_TIME*60
        self._io_loop.start()

    def handle_request(self,response):
        if(self.DataFile["PROTOCOL_TYPE"] == u"HTTP_POST_JSON" or self.DataFile["PROTOCOL_TYPE"] == u"HTTP_GET"):
            self.ret=response.body
            #print self.ret
            '''self.ret=json.loads(self.ret,encoding='UTF-8')
            self.ret=self.ret['response']['items']
            if(self.ret != self.DataFile["EXP_DATA"]):
                logging.info(u"ERROR Response")'''
            logging.info(u"Recv New Response")
        if time.time()>self.end:
            self._client.close()
            self._io_loop.stop()
            return

        self._client.fetch(self.get_request(), self.handle_request)

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

