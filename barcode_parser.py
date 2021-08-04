'''
Descripttion: 
version: 
Author: zpliu
Date: 2021-07-15 20:29:47
LastEditors: zpliu
LastEditTime: 2021-08-04 16:09:10
@param: 
'''
import pandas as pd
import os
import re
import gzip
import argparse
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_sequence_fasta(sequenceFile: str):
    '''
    args: input fasta file@str
          fasta format
    returns: @pd.DataFrame
    '''
    pattern = re.compile(r'^>')
    sequences = []
    with open(sequenceFile, 'r') as File:
        for line in File:
            if re.match(pattern, line):
                sequenceId = "".join(line.split(" ")[0].split(":")[-3:])
            else:
                sequenceLine = line.strip("\n")
                sequences.append((sequenceId, sequenceLine))
    outData = pd.DataFrame(sequences, columns=['seq_id', 'seq'])
    return outData


def reversed_sequence(sequence):
    '''
    reversed and complement the fasta sequences
    '''
    sequence = sequence.upper()[::-1]
    basecomplement = {
        "A": "T",
        "T": "A",
        "G": "C",
        "C": "G",
        'N':'N'
    }
    letters = list(sequence)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)


def fastq2fasta(fastqFile, reversedSeq=False):
    '''transform fastaq to fasta
     args:
        -fastqFile: raw sequence fastaq file
        -reverseseq: reversed and complement the R2 sequence
    '''
    try:
        File = gzip.open(fastqFile, 'rt')
        File.readline()
        File.seek(0)
    except:
        File = open(fastqFile, 'rt')
    out = []
    index = 0
    for line in File:
        if index % 4 == 0:
          #! sequence Id
            sequenceId = "".join(re.split(r"/[12]",line.split(" ")[0])[0])
            index += 1
        elif index % 4 == 1:
            #! sequence line
            if reversedSeq:
                sequenceLine = reversed_sequence(line.strip("\n"))
                out.append((sequenceId, sequenceLine))
            else:
                sequenceLine = line.strip("\n")
                out.append((sequenceId, sequenceLine))
            index += 1
        else:
            #! other line
            index += 1
    outSequence = pd.DataFrame(out, columns=['seq_id', 'seq'])
    return(outSequence)





if __name__=="__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('-R1',help='R1 sequence file')
    parser.add_argument('-R2',help='R2 sequence file')
    parser.add_argument('-vector5',help='verctor sequence adjacent to 5\' barcode',
    default='TATAAGCGAAAGAAGCATCAGATGGGCAAACAAAGCACCAGTGGTCTAGTGGTAGAATAGTACCCTGCCACGGTACAGACCCGGGTTCGATTCCCGGCTGGTGCA')
    parser.add_argument('-vector3',help='verctor sequence adjacent to 3\' barcode',
    default='TAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTTTTAGCGCGTGCATGCCTGCAGGTCCACAAATTCGGGTC')
    parser.add_argument('-o',help='out put file')
    
    args=parser.parse_args()
    ##################################
    #! barcode id
    ################################
    barcodeDict={}
    R1barcode=["GACGCCTAG","GACGCGCTA","GACGCGGAT","GACGCGTCA","GACGCTACG","GACGTACGA","GACGTCACG",
    "GACGTCGCT","GACGTCGTA","GACGTGGAC","GACGACATG","GACGACGTA","GACGACTGT","GACGAGTCA","GACGATCGA",
    "GACGCACCG","CGAGCCTAG","CGAGCGCTA","CGAGCGGAT","CGAGCGTCA","CGAGCTACG","CGAGTACGA","CGAGTCACG",
    "CGAGTCGCT","CGAGTCGTA","CGAGTGGAC","CGAGACATG","CGAGACGTA","CGAGACTGT","CGAGAGTCA","CGAGATCGA","CGAGCACCG"]
    R2barcode=[
        "ACGTCA","ACCATG","ACGAGC","ACAGCG","ATGATG",
        "ATCATC","ATGGTC","ATGCTG","AGCACG",
        "AGCTCA","AGATGT","AGACGA"
    ]
    for R1index,R1 in enumerate(R1barcode):
        for R2index,R2 in enumerate(R2barcode):
            barcodeKey="R1-"+str(R1index+1)+"~R2-"+str(R2index+1)
            barcodeDict[R1+"-"+R2]=barcodeKey
    #############################
    #!merge sequence
    #############################
    logger.info("read fastq file...")
    R1sequences=fastq2fasta(args.R1,reversedSeq=False)
    R2sequences=fastq2fasta(args.R2,reversedSeq=True)
    logger.info("merge the R1 and R2 file...")
    mergeSequence=pd.merge(left=R1sequences, right=R2sequences, left_on='seq_id', right_on='seq_id')
    # mergeSequence.to_csv("test.fa",header=False,sep="\t",index=False)
    # R1sequences.to_csv("R1.fa",header=False,sep="\t",index=False)
    # R2sequences.to_csv("R2.fa",header=False,sep="\t",index=False)
    #########################################
    # regular expression
    #########################################
    searchParrernStr='[ATCG]*([ATCG]{}{}.*{}[ATGC]{})[ATCG]*'.format('{9}',args.vector5,args.vector3,'{6}')
    # print(searchParrernStr)
    #! search barcode sequence
    barcodePattern=re.compile(searchParrernStr)
    containBarcodeSequence=mergeSequence.apply(
        lambda x: barcodePattern.match(x['seq_x']+x['seq_y'])[1] if barcodePattern.match(x['seq_x']+x['seq_y']) else None ,
        axis=1)
    barcodesequence=[]
    logger.info("count the barcode numbers")
    for sequence in containBarcodeSequence:
        if sequence:
            #! barcode sequence
            try:
                barcode=sequence[0:9]+"-"+reversed_sequence(sequence)[0:6]
            except KeyError:
                print(sequence)
            #! sgRNA sequence
            sgRNAstart=9+len(args.vector5)
            sgRNA=sequence[sgRNAstart:sgRNAstart+20] 
            barcodesequence.append((barcode,sgRNA))
        else:
            pass
    #####################################################
    #!barcode and sgRNA sequence
    #####################################################
    barcodeData=pd.DataFrame(barcodesequence,columns=['barcode','sgRNA'])
    outData=[]
    for barcodesequence in barcodeDict.keys():
        sgRNAData=barcodeData.loc[barcodeData['barcode']==barcodesequence]
        if sgRNAData.empty:
            #! without sequence sgRNA
            pass
        else:
            #! count the sgRNA number
            totalCount=sgRNAData.shape[0]
            sgRNAcount=dict(sgRNAData['sgRNA'].value_counts())
            for key,value in sgRNAcount.items():
                outData.append((
                    barcodeDict[barcodesequence],
                    barcodesequence, #barcode sequence
                    totalCount,     #barcode count
                    key,    #sgRNA sequence
                    value   #sgRNA count 
                ))
    if not outData:
        logger.warning("Sorry no barcode were detect in the sequence file!")
    outData=pd.DataFrame(outData,columns=['barcodeID','barcodesequence','barcodeCount','sgRNAsequence','sgRNACount'])
    outData.to_csv(args.o,header=True,index=False,sep="\t")
    logger.info("complete!")