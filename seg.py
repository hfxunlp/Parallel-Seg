#encoding: utf-8

import sys
import pynlpir

def segline(strin):
	try:
		rs=pynlpir.segment(strin.encode("utf-8","ignore"), pos_tagging=False)
	except:
		rs=[]
	rs=" ".join(rs)
	return rs

def segfile(srcfile,rsfile):
	err=0
	with open(rsfile,"w") as fwrt:
		with open(srcfile) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					segrs=segline(tmp.decode("utf-8","ignore"))
					if segrs:
						segrs+="\n"
						fwrt.write(segrs.encode("utf-8","ignore"))
					else:
						err+=1
	if err>0:
		print("Seg:"+srcfile+",Error:"+str(err))

if __name__=="__main__":
	pynlpir.open()
	segfile(sys.argv[1],sys.argv[2])
	pynlpir.close()
