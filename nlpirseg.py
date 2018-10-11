#encoding: utf-8

import sys
from pynlpir import nlpir

def segcore(strin):
	try:
		rs=nlpir.ParagraphProcess(strin.encode("utf-8", "ignore"), 1)
	except:
		rs=""
	return rs.decode("utf-8","ignore")

def segline(strin):
	def clear_tag(strin):
		tmp = strin.split()
		rs = []
		for tmpu in tmp:
			ind = tmpu.rfind("/")
			if ind > 0:
				rs.append(tmpu[:ind])
			else:
				rs.append(tmpu)
		return " ".join(rs)
	tmp = segcore(strin)
	if tmp:
		return clear_tag(tmp)
	else:
		return tmp

def handle(srcfile,rsfile):
	err=0
	ens="\n".encode("utf-8")
	with open(rsfile,"wb") as fwrt:
		with open(srcfile,"rb") as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					try:
						tmp = tmp.decode("utf-8")
					except Exception as e:
						tmp = ""
					if tmp:
						tmp=segline(tmp)
						if tmp:
							fwrt.write(tmp.encode("utf-8"))
						else:
							err+=1
					else:
						err+=1
				fwrt.write(ens)
	if err>0:
		print("".join(("Seg:",srcfile,",Error:",str(err),)))

if __name__=="__main__":
	nlpir.Init(nlpir.PACKAGE_DIR,nlpir.UTF8_CODE,None)
	#nlpir.SetPOSmap(nlpir.PKU_POS_MAP_SECOND)#ICT_POS_MAP_SECOND/FIRST
	handle(sys.argv[1], sys.argv[2])
	nlpir.Exit()
