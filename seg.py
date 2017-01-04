#encoding: utf-8

import sys
from pynlpir import nlpir

def segline(strin):
	try:
		rs=nlpir.ParagraphProcess(strin.encode("utf-8","ignore"), 1)
	except:
		rs=""
	return rs.decode("utf-8","ignore")

def segfile(srcfile,rsfile):
	err=0
	with open(rsfile,"wb") as fwrt:
		with open(srcfile,"rb") as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					segrs=segline(tmp.decode("utf-8","ignore").replace(" ",""))
					if segrs:
						segrs+="\n"
						fwrt.write(segrs.encode("utf-8","ignore"))
					else:
						err+=1
	if err>0:
		print("Seg:"+srcfile+",Error:"+str(err))

if __name__=="__main__":
	nlpir.Init(nlpir.PACKAGE_DIR,nlpir.UTF8_CODE,None)
	segfile(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
	nlpir.Exit()
