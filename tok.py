#encoding: utf-8

import sys
from nltk.tokenize.nist import NISTTokenizer as Tokenizer

def segline(strin, tok, to_lower = False):
	def clearstr(lin, to_lower):
		rs = []
		for tmpu in lin:
			if tmpu:
				rs.append(tmpu)
		if to_lower:
			return " ".join(rs).lower()
		else:
			return " ".join(rs).lower()
	return clearstr(tok.tokenize(strin, return_str=True, escape=False).split(), to_lower)

def handle(srcfile,rsfile):
	err=0
	with open(rsfile,"wb") as fwrt:
		with open(srcfile,"rb") as frd:
			tok = Tokenizer()
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=segline(tmp.decode("utf-8", "ignore"), tok)
					if tmp:
						fwrt.write(tmp.encode("utf-8", "ignore"))
					else:
						err+=1
				fwrt.write("\n")
	if err>0:
		print("".join(("Seg:",srcfile,",Error:",str(err),)))

if __name__=="__main__":
	handle(sys.argv[1], sys.argv[2])
