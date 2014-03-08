#!/usr/bin/env python
#-*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

def Sendmail_Textreport(version=u"UPPS-1.0.9.0",content_sub=u" 性能自动化测试报告",from_mail_addr="yangjun03@baidu.com",
to_mail_addr="yangjun03@baidu.com",server="mail2-in.baidu.com",img_description_list=[u"QPS(query per second)曲线:",u"CPU_IDLE曲线",u"内存占用曲线"],
img_file_list=["../img/query_period_distribution_plot.png","../img/server_cpu_idle_plot.png","../img/server_memory_usage_plot.png"],
starttime='2014-03-02 06:31:44',endtime='2014-03-02 06:41:44',timeelapsed='600.0',
totalrequest='4987873',totalresponse='4981873',responserate='99.880%',totalerror='0',errorrate='0.000%',QPS='8303',latency='5'):
    sub_str=u"【请阅】"+version+content_sub
    img_id_list=["image1","image2","image3"]
    img_alt_list=img_description_list

    body_content=u"""<p style='color:black;text-align:center;font-size:20px;font-family:微软雅黑'><b><span style='color:blue'>"""
    body_content+=version
    body_content+=u"""</span>"""
    body_content+=content_sub
    body_content+="""</b></p>"""
    body_content+=u"""<p style='font-family:微软雅黑;font-style:italic;text-align:right;margin-right:50%'>"""
    body_content+=u"@easyBenchmarkTesttool 2014"
    body_content+="""</p>"""
    body_content+=u"""
    <style type="text/css">
    #ID_Tbl_Summary{
    	background-color: #e5e5e5;
    	margin-right:15%;
    	margin-left:0;

    	border-style:solid;
    	border-width:medium;
    	border-color:#e5e5e5;
    	height:18px;

    	font-family: 微软雅黑;
    	font-weight: bold;
    	font-size: 15px;
    	color:lightgblue;

    	position:relative;
    	right:0px;
    }

    td{
    	#text-align:center;
    	text-align:left;
        text-indent:5px;
    	#color:green;
    }

    table{
    	border-collapse:collapse;
    	border:1px solid white;
    	background:#e5e5e5;
    	height:20px;
    }
    th,td{
    	border-collapse:collapse;
    	border:1px solid white;
    	background:#e5e5e5;
    	height:30px;
    }
    .title{
    	font-weight: normal;
        color:CadetBlue;
    }
    .con{
    	color:black;
    	font-weight: normal;
        font-style:italic;
    }

    </style>
    <meta http-equiv="content-type" content="text/html" charset="utf-8"/>

    <p style='font-size:18px;font-family: 微软雅黑;font-weight:bold'>一、指标统计</p>
    <table id="ID_Tbl_Summary" border="0" width="70%" height="20px" cellpadding="0" cellspacing="0" bgcolor="#000000">
    <tbody id="ID_TBody">
    	<tr><td class='title'>StartTime:</td> <td class='con'>"""
    body_content+=starttime
    body_content+=u"""</td> <td class='title'>EndTime:</td> <td class='con'>"""
    body_content+=endtime
    body_content+=u"""</td> <td class='title'>TimeElapsed(s):</td> <td class='con'>"""
    body_content+=timeelapsed

    body_content+=u"""</td> </tr>
    	<tr><td class='title'>TotalRequest:</td> <td class='con'>"""
    body_content+=totalrequest
    body_content+=u"""</td> <td class='title'>TotalResponse:</td> <td class='con'>"""
    body_content+=totalresponse
    body_content+=u"""</td> <td class='title'>ResponseRate:</td> <td class='con'>"""
    body_content+=responserate

    body_content+=u"""</td> </tr>
    	<tr><td class='title'>TotalResponse:</td> <td class='con'>"""
    body_content+=totalresponse
    body_content+=u"""</td> <td class='title'>TotalError:</td> <td class='con'>"""
    body_content+=totalerror
    body_content+=u"""</td> <td class='title'>ErrorRate:</td> <td class='con'>"""
    body_content+=errorrate
    body_content+=u"""</td> </tr>"""

    body_content+=u"""</td> </tr>
    	<tr><td class='title'>QPS:</td> <td class='con'>"""
    body_content+=QPS
    body_content+=u"""</td> <td class='title'>Latency(ms):</td> <td class='con'>"""
    body_content+=latency
    body_content+=u"""</td> <td class='title'></td> <td class='con'>"""
    body_content+=''
    body_content+=u"""</td> </tr>
    </tbody>
    </table>
    <p style='font-size:18px;font-family: 微软雅黑;font-weight:bold'>二、性能曲线</p>
    """

    mail=MIMEMultipart()
    mail["Subject"]=sub_str
    for i in range(len(img_file_list)):
        try:
            fp=open(img_file_list[i])
            img=MIMEImage(fp.read())
            fp.close()
            img.add_header('Content-ID','<'+img_id_list[i]+'>')
            mail.attach(img)
        except Exception:
            pass
        body_content+="""<p><li>"""
        body_content+=img_description_list[i]
        body_content+="""</li><br/><img src="cid:"""
        body_content+=img_id_list[i]
        body_content+="""" alt="""
        body_content+=img_alt_list[i]
        body_content+=""""</p>"""

    body = MIMEText(body_content,'html','utf-8')
    mail.attach(body)

    mail["From"]=from_mail_addr
    mail["To"]=to_mail_addr
    smtp=smtplib.SMTP(server)
    smtp.sendmail(mail["From"], mail["To"].split(","), mail.as_string())
    smtp.quit()

if __name__ == '__main__':
    Sendmail_Textreport()

