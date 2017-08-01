#encoding: utf-8

import sys
from pyltp import Segmentor

ltpdata="/media/Storage/data/ltp_data/"
segmfile=ltpdata+"cws.model"

def segline(strin, segger):
	try:
		rs=" ".join(segger.segment(strin.encode("utf-8", "ignore")))
	except:
		rs=""
	return rs.decode("utf-8","ignore")

def handle(srcfile,rsfile):
	err=0
	global segmfile
	with open(srcfile,"rb") as frd:
	  	segger = Segmentor()
		segger.load(segmfile)
		with open(rsfile,"wb") as fwrt:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=segline(tmp.decode("utf-8","ignore"), segger)
					if tmp:
						fwrt.write(tmp.encode("utf-8"))
					else:
						err+=1
				fwrt.write("\n")
	if err>0:
		print("".join(("Seg:",srcfile,",Error:",str(err),)))

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"))
