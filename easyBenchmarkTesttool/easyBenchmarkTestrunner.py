#!/usr/bin/env python
#-*- coding: utf-8 -*-
import commands

if __name__ == '__main__':
    cmdstr=""" python easyBenchmarkTesttool.py -p 0 -c 500 -t 2 HTTP_POST_JSON.data &&
    python easyBenchmarkStat.py"""
    status,output=commands.getstatusoutput(cmdstr)
    if(status == 0):
        print output
