#!/usr/bin/env python
#-*- coding: utf-8 -*-
import commands
import json
import time
import datetime
import matplotlib.pyplot as plt
import numpy
import math
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

import lib.EMailLib

ConfFilePath=u"./conf/easyBenchmarkTestTool.conf"
ConfFile=json.load(open(ConfFilePath, "r"),encoding='utf-8')
response_period_distribution_statfile=u"./stat/easyBenchmarkTestTool.stat"
img_file_save=["./img/query_period_distribution_plot","./img/query_period_distribution_plot","./img/query_period_distribution_plot"]
img_file_list=[file+".png" for file in img_file_save]

class easyBenchmarkStat(object):
    def get_totalrequest(self):
        cmdstr="""grep 'Send' log/*.log | awk -F']' '{ print $2,$3 }' | awk -F'[' '{ print $2,$3 }' | wc -l"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            return output
    def get_totalresponse(self):
        cmdstr="""grep 'Recv' log/*.log | awk -F']' '{ print $2,$3 }' | awk -F'[' '{ print $2,$3 }' | wc -l"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            return output
    def get_totalerror(self):
        cmdstr="""grep 'ERROR' log/*.log | awk -F']' '{ print $2,$3 }' | awk -F'[' '{ print $2,$3 }' | wc -l"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            return output
    def get_response_period_distribution(self):
        cmdstr="""grep 'Recv' log/*.log | awk -F'[()]' '{ print $2 }' | awk -F'[ ,-]' '{ print $2,$3,$4,$5}' | awk -F'[ :]' '{ a[$1"-"$2"-"$3" "$4":"$5]++ }END{ for ( i in a ) print i,a[i] }'"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            file_object = open(response_period_distribution_statfile, 'w')
            file_object.write(str(output))
            file_object.close( )
    def get_starttime(self):
        #cmdstr="""grep 'Send' log/TestLog.0.log | head -n 1 |awk -F'[(,)]' '{ print $3 }'"""
        cmdstr="""awk 'NR==1' log/TestLog.0.log |awk -F'[(,)]' '{ print $3 }'"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            timestamp=time.mktime(time.strptime(str(output),'%Y-%m-%d %H:%M:%S'))
            return str(output),timestamp
    def get_endtime(self):
        cmdstr="""tail -n 1 log/TestLog.0.log | awk -F'[(,)]' '{ print $3 }'"""
        status,output=commands.getstatusoutput(cmdstr)
        if(status == 0):
            timestamp=time.mktime(time.strptime(str(output),'%Y-%m-%d %H:%M:%S'))
            return str(output),timestamp
    def get_query_period_distribution_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xaxis = ax.xaxis
        yaxis = ax.yaxis
        yList=[]
        dateList=[]
        lines=[]
        fp=open(response_period_distribution_statfile)
        line=fp.readline()
        while(line):
            lines.append(line)
            line=fp.readline()
        fp.close()
        temps=[[] for i in range(len(lines))]
        for i in range(len(lines)):
            lines[i].strip()
            line_list=lines[i].split(" ")
            temps[i].append(str(line_list[0])+" "+str(line_list[1]))
            temps[i].append(line_list[2])
        def get_timestamp(x):
            return time.mktime(time.strptime(x[0],'%Y-%m-%d %H:%M'))
        temps.sort(lambda x,y:cmp(get_timestamp(x),get_timestamp(y)))
        for temp in temps:
            yList.append(temp[1])
            dateList.append(temp[0])

        t=time.strptime(dateList[0], "%Y-%m-%d %H:%M")
        startDate = datetime.datetime(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        t=time.strptime(dateList[-1], "%Y-%m-%d %H:%M")
        endDate = datetime.datetime(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        delta = datetime.timedelta(minutes=1)
        dates = drange(startDate , endDate, delta)
        ax.plot_date(dates,  yList,  'm-',  marker='.',  linewidth=1)

        xaxis.set_major_formatter( DateFormatter('%Y-%m-%d %H:%M') )
        ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
        fig.autofmt_xdate()
        plt.savefig(img_file_list[0])


if __name__ == "__main__":
    print("*"*80)
    print(u"log analysis in progress,please wait a moment...")
    easyBenchmarkStat=easyBenchmarkStat()
    starttime,starttimestamp=easyBenchmarkStat.get_starttime()
    #开始时间获取
    starttime=str(starttime)
    print("starttime:"+starttime)
    endtime,endtimestamp=easyBenchmarkStat.get_endtime()
    #结束时间获取
    endtime=str(endtime)
    print("endtime:"+str(endtime))
    #测试时间
    timeelapsed=str(endtimestamp-starttimestamp)
    print("timeelapsed:"+timeelapsed)

    #总请求数
    totalrequest=easyBenchmarkStat.get_totalrequest()
    print("totalrequest:"+totalrequest)
    #总回应数
    totalresponse=easyBenchmarkStat.get_totalresponse()
    #应答率
    responserate="%0.3f%%" %((float(totalresponse)/float(totalrequest))*100)
    print("totalresponse:"+totalresponse+"\t\t"+"responserate:"+responserate)
    #错误数
    totalerror=easyBenchmarkStat.get_totalerror()
    #错误率
    errorrate="%0.3f%%" %((float(totalerror)/float(totalresponse))*100)
    print("totalerror:"+totalerror+"\t\t\t"+"errorrate:"+errorrate)
    #QPS
    QPS=str(int(totalresponse)/int(endtimestamp-starttimestamp))
    print("QPS(query per second):"+QPS)
    response_period_distribution=easyBenchmarkStat.get_response_period_distribution()
    easyBenchmarkStat.get_query_period_distribution_plot()
    print("*"*80)
    print("log analysis completed,curve of performance test at the directory of ./img/")
    print("please pay attention to your mail of this benchmark test")

    lib.EMailLib.Sendmail_Textreport(version=ConfFile['version'],content_sub=u" 性能自动化测试报告",from_mail_addr=ConfFile['from_mail_addr'],
to_mail_addr=ConfFile['to_mail_addr'],server=ConfFile['server'],img_description_list=[u"QPS(query per second)曲线:",u"CPU_IDLE曲线",u"内存占用曲线"],
img_file_list=img_file_list,starttime=starttime,endtime=endtime,timeelapsed=timeelapsed,
totalrequest=totalrequest,totalresponse=totalresponse,responserate=responserate,totalerror=totalerror,errorrate=errorrate,QPS=QPS)

