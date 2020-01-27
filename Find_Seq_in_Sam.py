#use python 3 env

import argparse, re

parser = argparse.ArgumentParser(description='Parse sam file for sequence')
parser.add_argument('-inputSam', type=str, help='i.e.: /path/to/your/sam/file.sam', required=True)

args = parser.parse_args()

SAMFILE = args.inputSam

# SAM format
# Col	Field	Type	Brief description
# 1	QNAME	String	Query template NAME
# 2	FLAG	Int	bitwise FLAG
# 3	RNAME	String	References sequence NAME
# 4	POS	Int	1- based leftmost mapping POSition
# 5	MAPQ	Int	MAPping Quality
# 6	CIGAR	String	CIGAR String
# 7	RNEXT	String	Ref. name of the mate/next read
# 8	PNEXT	Int	Position of the mate/next read
# 9	TLEN	Int	observed Template LENgth
# 10	SEQ	String	segment SEQuence
# 11	QUAL	String	ASCII of Phred-scaled base QUALity+33

def parse_sam():
    with open(SAMFILE,'r') as inputFILE:
        for line in inputFILE:
            line = line.strip()
            line = line.split()
            #header
            if line[0][0:1] == '@':
                print(line)

            else:
                QNAME,FLAG,RNAME,POS,MAPQ,CIGAR,RNEXT,PNEXT,TLEN,SEQ,QUAL = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10]
                print(SEQ)

def cat_and_print_line():


if __name__ == "__main__":
    parse_sam()

    

    

