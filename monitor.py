#encoding: utf-8

import sys
import os
import subprocess
import threading
from time import sleep

nthread=8
sleeptime=5
plock=threading.Lock()
printlock=threading.Lock()
cmd='pypy seg.py'

def mulprint(strp):
	global printlock
	with printlock:
		print(strp)

def createPool(srcp, rsp):
	#return ["src/"+str(i)+".txt" for i in xrange(1946,2006)],["rs/"+str(i)+".txt" for i in xrange(1946,2006)]
	srcl=[]
	rsl=[]
	for root, dirs, files in os.walk(srcp):
		for file in files:
			srcf=os.path.join(root, file)
			srcl.append(srcf)
			rsl.append(srcf.replace(srcp, rsp))
	return srcl, rsl

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

def handle_one(cmd,srcf,rsf):
	mulprint("handle:"+srcf+",to:"+rsf)
	subprocess.call(" ".join((cmd,srcf,rsf,)),shell=True)

def core():
	global nthread, cmd
	state=True
	while state:
		srcf,rsf,state=get()
		if state:
			handle_one(cmd,srcf,rsf)
		else:
			nthread-=1

def handle(src, rs):
	global nthread
	srcp,rsp=createPool(src, rs)
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

if __name__=="__main__":
	if len(sys.argv)>3:
		cmd=sys.argv[3].decode("utf-8")
	handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"))
