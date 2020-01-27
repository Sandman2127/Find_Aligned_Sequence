#use python 3 env

import argparse, re, os

parser = argparse.ArgumentParser(description='Parse sam file for sequence')
parser.add_argument('-inputSam', type=str, help='i.e.: /path/to/your/sam/file.sam', required=True)
parser.add_argument('-inputList', type=str, help='i.e.: /path/to/your/sam/list.txt', required=False)

args = parser.parse_args()

SAMFILE = args.inputSam
LISTFILE = args.inputList

testList = ['GTTTACCCGCCAATATATCCTGTCA','GTTTACACCACAATATATCCTGCCA','TTGATCCCGAGGGGAACCCTGTGGT','GAGGGGTTGGATCAAAGTACT','CTGAAAGTTGACCCGCTTCATGG','CAGCTTGGTGTGATCCTCCGCCGGCAA','GCCTTGGCGTACCGCGTACATCTT','CAGATAGCAGCTCGGTAATGGTCTT','ATTTACTCTGGTAGCTGCGCGATGTATT','TCATCTACTCATTTATTCATTTGCTC','CCATGCCGCCTCCTTTAGCCGCTAAAAT','TCGGTGCCTGGTTGTTCTTGATTTT','CCACACATGGGGCATTCCACGGCG','TGTGGACGGAACACGCGGCCGGGCTTGTC','GGATCACCTCGCCAGCTCGTCGGTCA','GCGGTTGCCGGGATTCTTTGCGGATTCGA','ACTTCTCCACCAGGTCATCACCCAG','GCCGCGCCGATTTGTACCGGGCCGGA','CAGGTCGTAATCCCACACACTGGC','CTCTTTTCTCTTAGGTTTACCCGCCA','AATATCCGTTATTCTAATAAACG','ATAAACCTTTTCACGCCCTTTTA','TTGGCATGCACATACAAATGGACGAACGG','TTGATCCCGAGGGGAACCCTGTGG','GAACCCTGTGGTTGGCATGCACA','TATATCCTGTCAAACACTGATAGTTTA','CTAATAAACGCTCTTTTCT','CACTCAGAAGAACTCGTCAAGAAGGC']

def parse_list():
    outList = []
    with open(LISTFILE,"r") as inputF:
        for line in inputF:
            line = line.strip()
            line = line.split()
            outList.extend(line)
    return outList


def make_output_dir(path,access_rights):
    try:
        os.mkdir(path, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

def parse_sam(path,input_list):
    # open a log file to describe the operations of the find
    logFileName = str(path) + "Regex_find_log.txt"
    logFile = open(logFileName,"w+")

    for FINDSEQ in input_list:

        # open new output sam file in output directory:
        fileName = str(path) + str(FINDSEQ) + ".sam"
        fileOut = open(fileName,"w+")
        message1 = "Opening new file: " + str(FINDSEQ) + ".sam in " + str(path) + "\n"
        logFile.write(message1)

        # define hits and total variables
        hits = 0
        total = 0

        # parse sam file looking for those characters:
        with open(SAMFILE,'r') as inputFILE:
            message2 = "Parsing Sam File: " + str(SAMFILE) + " using REGEX to find the string: " + str(FINDSEQ) + " in SEQ column" + "\n"
            logFile.write(message2)
            for line in inputFILE:
                line = line.strip()
                line = line.split()

                #header
                if line[0][0:1] == '@':
                    fileOut.write(cat_and_print_line(line))
                
                # SAM format lines
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
                else:
                    QNAME,FLAG,RNAME,POS,MAPQ,CIGAR,RNEXT,PNEXT,TLEN,SEQ,QUAL = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10]
                    total += 1 
                    match = re.search(str(FINDSEQ), str(SEQ))
                    if match:
                        fileOut.write(cat_and_print_line(line))
                        hits += 1
        fileOut.close()
        total_perc = 100*(hits/total)
        message3 = "Found " + str(hits) + " lines containing the DNA sequence: " + str(FINDSEQ) + " in " + str(SAMFILE) + "\n"
        message4 = "This amounts to: " + str(total_perc) + "% of the mapped reads within " + str(SAMFILE) + "\n"
        logFile.write(message3)
        logFile.write(message4)
        logFile.write("\n")

    logFile.close()

def cat_and_print_line(lineA):
    x = 0
    lineout = ""
    for field in lineA:
        # for first field just initialize lineout
        if x == 0 :
            x = 1
            lineout = field
        # for second and further add them with tabs
        else:
            x = x + 1
            lineout = lineout + "\t" + field
    # add new line character at end of line
    lineout = lineout + "\n"
    return lineout



if __name__ == "__main__":
    #TODO: define output directory
    cwd = os.getcwd()
    path_output_dir = str(cwd) + "/output_sams/"

    #TODO: define the access rights
    access_rights = 0o775
    #TODO: make output directory
    make_output_dir(path_output_dir,access_rights)
    
    #TODO: determine if using a list or the built in test list, and parse your sam and output hits to output directory
    if LISTFILE:
        print("Parsing sam file for user defined input sequence list")
        output_List = parse_list()
        parse_sam(path_output_dir,output_List)
    else:
        parse_sam(path_output_dir,testList)

    

    

