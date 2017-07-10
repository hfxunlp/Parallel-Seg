#encoding: utf-8

import sys
from pynlpir import nlpir

def segline(strin):
	try:
		rs=nlpir.ParagraphProcess(strin.encode("utf-8"), 1)
	except:
		rs=""
	return rs.decode("utf-8","ignore")

def handle(srcfile,rsfile):
	err=0
	with open(rsfile,"wb") as fwrt:
		with open(srcfile,"rb") as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=segline(tmp.decode("utf-8","ignore"))
					if tmp:
						fwrt.write(tmp.encode("utf-8"))
					else:
						err+=1
				fwrt.write("\n")
	if err>0:
		print("".join(("Seg:",srcfile,",Error:",str(err),)))

if __name__=="__main__":
	nlpir.Init(nlpir.PACKAGE_DIR,nlpir.UTF8_CODE,None)
	#nlpir.SetPOSmap(nlpir.PKU_POS_MAP_SECOND)#ICT_POS_MAP_SECOND/FIRST
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
	nlpir.Exit()
