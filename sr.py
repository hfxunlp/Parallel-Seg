#encoding: utf-8
from hashlib import sha1
import sys
import os
from shutil import rmtree
import monitor

def getID(file, max_block=False, block_size=65536):
	calcer=sha1()
	if max_block:
		nr=1
		with open(file, 'rb') as f:
			data=f.read(block_size)
			while data:
				calcer.update(data)
				nr+=1
				if nr<max_block:
					data=f.read(block_size)
				else:
					break
	else:
		with open(file, 'rb') as f:
			data=f.read(block_size)
			while data:
				calcer.update(data)
				data=f.read(block_size)
	rs=calcer.hexdigest()
	return rs

def cutfile(srcf, srcp, bsize):
	if os.path.exists(srcp):
		rmtree(srcp, True)
	os.makedirs(srcp)
	curf=1
	wrtf=open(os.path.join(srcp, str(curf)), "wb")
	with open(srcf, "rb") as frd:
		curl=1
		for line in frd:
			wrtf.write(line)
			curl+=1
			if curl>=bsize:
				wrtf.close()
				curf+=1
				wrtf=open(os.path.join(srcp, str(curf)), "wb")
		wrtf.close()
	return curf

def mergers(rsf, rsp, nf):
	with open(rsf, "wb") as fwrt:
		for i in xrange(1, nf+1):
			with open(os.path.join(rsp, str(i)), "rb") as frd:
				for line in frd:
					fwrt.write(line)

def handle(srcf, rsf, bsize=32768):
	cached=".cache"
	tid=getID(srcf, 1024)
	rd=os.path.join(cached, tid)
	srcp=os.path.join(rd, "src")
	nfile=cutfile(srcf, srcp, bsize)
	rsp=os.path.join(rd, "rs")
	monitor.handle(srcp, rsp)
	mergers(rsf, rsp, nfile)
	rmtree(rd)
	try:
		os.removedirs(cached)
	except:
		pass

if __name__=="__main__":
	if len(sys.argv)>3:
		handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"), int(sys.argv[3].decode("utf-8")))
	else:
		handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"), 32768)
