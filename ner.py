#encoding: utf-8

import sys
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import os

ltpdata="/media/Storage/data/ltp_data/"
segmfile=os.path.join(ltpdata, "cws.model")
posmfile=os.path.join(ltpdata, "pos.model")
nermfile=os.path.join(ltpdata, "ner.model")

def buildata(wdl, tl, netags):
	rs=[]
	for wd, t, netu in zip(wdl, tl, netags):
		rs.append("\t".join((wd, t, netu,)))
	return rs

def handleline(srcl, segger, ptagger, recognizer):
	wds=segger.segment(srcl.encode("utf-8"))
	tags=ptagger.postag(wds)
	netags=recognizer.recognize(wds, tags)
	return "\n".join(buildata(wds, tags, netags)).decode("utf-8","ignore")

def handle(srcf, rsf):
	global segmfile, posmfile, nermfile
	with open(srcf) as frd:
		segger=Segmentor()
		segger.load(segmfile)
		ptagger=Postagger()
		ptagger.load(posmfile)
		recognizer=NamedEntityRecognizer()
		recognizer.load(nermfile)
		with open(rsf, "w") as fwrt:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8","ignore")
					tmp=handleline(tmp, segger, ptagger, recognizer)
					fwrt.write(tmp.encode("utf-8"))
				fwrt.write("\n\n")

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"))
