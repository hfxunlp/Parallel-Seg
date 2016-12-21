#encoding: utf-8

import sys
import subprocess
import threading
from time import sleep

nthread=8
sleeptime=5
plock=threading.Lock()
printlock=threading.Lock()

def mulprint(strp):
	global printlock
	with printlock:
		print(strp)

def createPool():
	return ["src/"+str(i)+".txt" for i in xrange(1946,2006)],["rs/"+str(i)+".txt" for i in xrange(1946,2006)]

def get():
	global plock,srcp,rsp
	rstate=False
	with plock:
		if len(srcp)>0:
			rstate=True
			rsrc=srcp.pop()
			rs=rsp.pop()
	if not rstate:
		rsrc=""
		rs=""
	return rsrc,rs,rstate

def oneseg(srcf,rsf):
	mulprint("seg:"+srcf+",to:"+rsf)
	subprocess.call('python seg.py '+srcf+" "+rsf,shell=True)

def core():
	global nthread
	state=True
	while state:
		srcf,rsf,state=get()
		if state:
			oneseg(srcf,rsf)
		else:
			nthread-=1

if __name__=="__main__":
	srcp,rsp=createPool()
	tpool=[]
	for i in xrange(nthread):
		t=threading.Thread(target=core)
		t.setDaemon(True)
		t.start()
		tpool.append(t)
	while nthread>0:
		sleep(sleeptime)
	del tpool
	del srcp
	del rsp
