#encoding: utf-8

import sys
from pyltp import Postagger

def tagline(srcl, ptag):
	wds=srcl.split()
	tags=ptag.postag(wds)
	rs=["/".join(mu) for mu in zip(wds,tags)]
	return " ".join(rs)

def handle(srcf, rsf):
	global mfile
	with open(srcf) as frd:
		ptagger=Postagger()
		ptagger.load(mfile)
		with open(rsf, "w") as fwrt:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8","ignore")
					tmp=tagline(rs, ptagger)
					fwrt.write(tmp.encode("utf-8","ignore"))
				fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	mfile="/media/Storage/data/ltp_data/pos.model"
	handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"))
