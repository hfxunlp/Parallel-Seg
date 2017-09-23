#encoding: utf-8

import sys
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import os

ltpdata="/media/Storage/data/ltp_data/"
segmfile=os.path.join(ltpdata, "cws.model")
posmfile=os.path.join(ltpdata, "pos.model")
parmfile=os.path.join(ltpdata, "parser.model")

def buildata(wdl, tl, al):
	rs=[]
	for wd, t, au in zip(wdl, tl, al):
		rs.append("\t".join((wd, t, au.relation, str(au.head),)))
	return rs

def handleline(srcl, segger, ptagger, parser):
	wds=segger.segment(srcl.encode("utf-8"))
	tags=ptagger.postag(wds)
	arcs=parser.parse(wds, tags)
	return "\n".join(buildata(wds, tags, arcs)).decode("utf-8","ignore")

def handle(srcf, rsf):
	global segmfile, posmfile, parmfile
	with open(srcf) as frd:
		segger=Segmentor()
		segger.load(segmfile)
		ptagger=Postagger()
		ptagger.load(posmfile)
		parser=Parser()
		parser.load(parmfile)
		with open(rsf, "w") as fwrt:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8","ignore")
					tmp=handleline(tmp, segger, ptagger, parser)
					fwrt.write(tmp.encode("utf-8"))
				fwrt.write("\n\n")

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"))
