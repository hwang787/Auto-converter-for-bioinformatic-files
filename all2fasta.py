#! /usr/bin/env python3
import sys
import argparse
import os
import re
parser = argparse.ArgumentParser()
parser.add_argument("-i","--i",help="this is Input file")
parser.add_argument('-f', '--fold', type=int, default = 70)
#read1=sys.argv[1]
#read2=sys.argv[2]
args = parser.parse_args()
num = args.fold
print(args)
if args.i:
        Input1 = str(args.i)
        print(Input1)
#with open(Input1,"r") as input1:
#some_words = 'This is a test'
#print(re.search(pattern = 'test', string = some_words))
def process(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}                  
def readFastq(fn):
    
    os.system("echo 'stop' >> fn")
    contain=0
    with open(fn, 'r') as fh:
        records = []
        
        for line in fh:
            
            
            if (re.search(pattern = '\\+', string = line)is not None):
                
                record={}
            if (re.search(pattern = '\\?', string = line)is None) and(re.search(pattern = '@', string = line)is not None):
                record={}
                record['name']=line.replace("@",">").strip('\n')    
                
                
            elif (re.search(pattern = '\\?', string = line)is None) and(re.search(pattern = '[ATCGn]+', string = line)is not None):
                    record["seq"]= line.strip("\n")
                    if(len(re.findall(r'[^ATCGNatcgn]+', record["seq"]))!=0):
                        contain =1
                    record["len"]= len(line.strip("\n"))
                    record["descr"]="descr= You didn't provide that hahaha"
                    records.append(record)
    return records,contain

def readGeneBank(fn):
    contain=0
    with open(fn, 'r') as fh:
        lines = []
        record = {}
        a =0
        for line in fh:
            if a == 1:
                lines.append(line)
            if (line.strip() != ''):
                
                if (re.search(pattern = 'ACCESSION', string = line) is not None):      
                    record["name"]=">"+(line.split())[1].strip('\n')
                if (re.search(pattern = 'DEFINITION', string = line) is not None):               
                    record["descr"]=(line.strip('\n').replace('DEFINITION', 'descr='))
                if (re.search(pattern = 'LOCUS', string = line) is not None): 
                    
                    record["len"]=line.split()[2].strip('\n')
                if (re.search(pattern = 'ORIGIN', string = line) is not None): 
                    a = 1
                if (re.search(pattern = '//', string = line) is not None): 
                    
                    seq='' 
                    for i in range(1, len(lines)-1):
                        seq += ''.join(lines[i].split()[1:])
                    record["seq"]=seq.upper().strip('\n')
                    if(len(re.findall(r'[^ATCGNatcgn]+', record["seq"]))!=0):
                        contain =1
    return [record],contain
def readMEGA(fn):
    contain=0
    with open(fn, 'r') as fh:
        lines=[]
        header= []
        seq = []
        records =[]
        for line in fh:
            lines.append(line)
        content_list = ("".join(lines[2:])).split("#")
        for each in content_list:
            info = each.split("\n")
    
            header.append(info[0])
            seq.append("".join(info[1:]))
    header = header[1:]
    seq = seq[1:] 
    print(header[0])
    if len(header)==0:
        record={}
        record["name"]=header[0].strip('\n')
        record["seq"]=seq[0].strip('\n')
        record["len"]=len(seq[0]).strip('\n')
        record["descr"]="descr= You didn't provide that hahaha"
        records.append(record)
    else:
        
        for i in range(0, len(header)) :
            
                record={}
                record["name"]=header[i].strip('\n')
                record["seq"]=seq[i].strip('\n')
                record["len"]=len(seq[i]).strip('\n')
                if(len(re.findall(r'[^ATCGNatcgn]+', seq[i]))!=0):
                    contain =1
                record["descr"]="descr= You didn't provide that hahaha"
                records.append(record)
    return records,contain

def readEMBL(fn):
    contain=0
    with open(fn, 'r') as fh:
        lines = []
        record = {}
        a =0
        for line in fh:
            if a == 1:
                lines.append(line)
            if (line.strip() != ''):
                
                
                if (re.search(pattern = 'ID', string = line) is not None):      
                    record["name"]=">"+(line.split())[1].strip('\n')
                if (re.search(pattern = 'DE  ', string = line) is not None):               
                    record["descr"]=(line.strip('\n').replace('DE   ', 'descr='))
                if (re.search(pattern = 'SQ', string = line) is not None): 
                    a = 1
                    record["len"]=line.split()[2].strip('\n')
                    
                if (re.search(pattern = '//', string = line) is not None): 
                    
                    seq='' 
                    for i in range(1, len(lines)-1):
                        seq += ''.join(lines[i].split()[0:-1])
                    record["seq"]=seq.upper().strip('\n')
                    if(len(re.findall(r'[^ATCGNatcgn]+', record["seq"]))!=0):
                        contain =1    
    return [record],contain
    
with open(Input1,"r") as input1:
    first_line = input1.readline()
    #print(first_line)
    match = re.search(pattern = '@', string = first_line)
    if (match is not None):
        print("match to fastq")
        records,contain = readFastq(Input1)
        
        
        #print(records)
        #writeFasta(Input1, fasta.out)
    else:
        match = re.search(pattern = 'ID', string = first_line)
        if (match is not None):
            records,contain = readEMBL(Input1)
            print("match to EMBL")
            #print(records)
        else:
            match = re.search(pattern = 'LOCUS', string = first_line)
            if (match is not None):
                records,contain = readGeneBank(Input1)
                #print(records)
                print("match to GeneBank")
            else: 
                    match = re.search(pattern = '#MEGA', string = first_line)
                    if (match is not None):
                        print("match to MEGA")
                        records,contain= readMEGA(Input1)
                        #print(records)
                    else:
                        print("not matched")
    
print(records)
filename = Input1.split(".")
if (contain ==0 ):
    appendix = "fna"
    
    
else:
    appendix = "faa"
if filename[-1]=="fna" or filename[-1]=="faa":
    output =".".join(filename)
    Output = open(output, "w")
elif len(filename)==1:
    ouput = filename[0]+"."+appendix
    Output = open(output, "w")
else:
    filename[-1]=appendix
    ouput = output =".".join(filename)
    Output = open(output, "w")

    
for record in records:
    Output.write(str(record['name'])+"|"+str(record['descr'])+"|len="+str(record['len']))
    Output.write("\n")
    
    n = 0
    for c in list(str(record['seq'])):
        Output.write(str(c))
        n+=1
        if n > num :
            n=0
            Output.write("\n")
    Output.write("\n")