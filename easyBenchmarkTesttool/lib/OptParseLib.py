#!/usr/bin/env python
#-*- coding: utf-8 -*-
import optparse
import os
import json

class OptParseLib(object):
    def parse_args(self):
        usage=u"""%prog [options] datafile
        datafile——request data file,need to configue as filename under the directory of data whitin this project.
        easyily run this program like this:
        python %prog -p 0 -c 500 -t 2 HTTP_POST_JSON.data"""
        version=u"%prog 1.0"
        parse=optparse.OptionParser(usage=usage,version=version)

        help=u'''multi-process mode,configuration number should be less than the actual number of VCPU;
                -1:close multi-process mode;
                0:automatic detection of VCPU numbers and start the corresponding number of processes;
                    the default mode is 0.'''
        parse.add_option('-p','--processnum',help=help,type='int',metavar='Integer',dest="ProcessNUM",default=0)

        help=u"client number of each process"
        parse.add_option('-c','--clientnum',help=help,type='int',metavar='Integer',dest="ClientNUM",default=500)

        help=u"total test time,minute as unit,the default time is 2 minutes."
        parse.add_option('-t','--testtime',help=help,type='float',metavar='Float',dest="TEST_TIME",default=2)

        options,args=parse.parse_args()

        if(len(args)) != 1:
            parse.error("[ERROR]:Args Num Error")
            '''print(parse.format_help())
            parse.exit()'''
        if(not os.path.exists("./data/"+str(args[0]))):
            parse.error("[ERROR]:DataFile Not Exist")
        else:
            DataFile=json.load(open("data/"+str(args[0]), "r"),encoding='utf-8')

        return options,DataFile


if __name__ == "__main__":
    options,DataFile=OptParseLib().parse_args()
    print(options.ProcessNUM,options.ClientNUM,options.TEST_TIME,DataFile)

