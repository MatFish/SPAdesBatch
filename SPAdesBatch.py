#!/usr/bin/env python3

import subprocess
import glob
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from collections import defaultdict
import re

def size_input():
    """Sets size cut-off and check for valid user input."""
    global size
    while True:
        size = input('Enter size cut-off for SPAdes output (Press enter for 500 bp default): ')
        default_size = 500
        if not size:
            size = default_size
            break
        elif not size.isdigit():
            print('Invalid input. Please try again')
            continue
        else:
            break 

def cov_input():
    """Sets coverage cut-off and check for valid user input."""
    global cov
    while True:
        cov = input('Enter coverage cut-off for SPAdes output (Press enter for 10 times default): ')
        default_cov = 10
        if not cov:
            cov = default_cov
            break
        elif not cov.isdigit():  
            print('Invalid input. Please try again')
            continue
        else:
            break

def assemble_type():
    """Asks user what settings they would like to use for SPAdes assembly"""
    global assemble_choice, final_choice
    while True:
        print('\nWhat type of SPAdes assembly would you like to run?\n')
        print('   1) SPAdes w/ error correct and assemble')
        print('   2) SPAdes careful w/ error correct and assemble')
        print('   3) metaSPAdes w/ error correct and assemble')
        print('   4) SPAdes w/ assemble only')
        print('   5) SPAdes careful w/ assemble only')
        print('   6) metaSPAdes w/ assemble only')
        print('   7) Custom input (manually enter options)\n')
        assemble_choice = input('Enter the number for your selection: ')
        if assemble_choice == '1':
            final_choice = 'SPAdes w/ error correction and assembly'
            break
        elif assemble_choice == '2': 
            final_choice = 'SPAdes careful w/ error correct and assemble'
            break
        elif assemble_choice == '3': 
            final_choice = 'metaSPAdes w/ error correct and assemble'
            break
        elif assemble_choice == '4': 
            final_choice = 'SPAdes w/ assemble only'
            break
        elif assemble_choice == '5':
            final_choice = 'SPAdes careful w/ assemble only'
            break
        elif assemble_choice == '6': 
            final_choice = 'metaSPAdes w/ assemble only'
            break
        elif assemble_choice == '7': 
            print('\nEnter modifiers/parameters as you would enter then into a manual SPAdes run (eg. --meta).')
            print('Do not enter input file name(s) and output folder name as they will be automatically selected.')
            final_choice = input('Enter custom options: ')
            break
        else:
            print('Invalid input. Please try again')
            continue

def parameter_input():
    """Sets cut-off parameters and checks if they are correct."""
    while True:
        size_input()
        cov_input()
        assemble_type()
        print('\n***CURRENT SETTINGS***\n   - Size cut-off:', size, 'bp\n   - Coverage cut-off:', cov, 'times\n   - Assembly type:', final_choice)
        begin = input('\nContinue (Y/N)? ').lower()
        if begin[0] == 'y':
            break
        else:
            print('Please try again. \n')
            continue

def size_and_cov_filter():
    """ Filters SPAdes output by size and coverage """
    contig_dict = defaultdict(list) 
    for fasta in glob.glob('*/contigs.fasta'):            
        contig_dict[fasta] = [rec for rec in SeqIO.parse(fasta, 'fasta')]           
    for keys,values in contig_dict.items():            
        contig_dict[keys] = [v for v in values if float(v.name.split('_')[5]) >= float(cov) and float(v.name.split('_')[3]) >= float(size)]
    for keys,values in contig_dict.items():        
        filtered_filename = str.replace(keys,".fasta","_filtered.fasta")        
        SeqIO.write(values, filtered_filename, 'fasta')       

def pipeline():
    """Finds each set of paired reads and assigns them to variable R1 and R2.
    Generates name for output file from name of R1.
    Runs SPAdes assembly on all paired files in current directory.
    Filters SPAdes results and runs local blastn search."""
    for file in glob.glob('*_R1_*fastq*'):
        global R1, R2, out
        R1 = file
        R2 = str.replace(R1, '_R1_', '_R2_')
        out = re.sub(r'.fastq.*', '', R1) + '_SpadesOutput'
        if assemble_choice == '1':                              
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out])
        elif assemble_choice == '2':
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, '--careful'])
        elif assemble_choice == '3':
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, '--meta'])
        elif assemble_choice == '4':                                                                                                                                            
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, '--only-assembler'])                                                                       
        elif assemble_choice == '5':
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, '--careful', '--only-assembler'])
        elif assemble_choice == '6':
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, '--meta', '--only-assembler'])
        elif assemble_choice == '7':
            subprocess.call(['spades.py', '-1', R1, '-2', R2, '-o', out, final_choice])
        size_and_cov_filter()
        blast_contig()

def blast_contig():
    """Performs local blastn search of filtered SPAdes contigs against nr/nt database.
    Using subprocess call for now, but may try to implement biopython in the future.
    Added 'export BLASTDB=/home/bio/BLASTDB' to ~/.bashrc to set BLASTDB environment variable."""
    query = out + '/contigs_filtered.fasta'
    output = out + '/BlastResults'
    subprocess.call(['blastn', '-task', 'megablast', '-query', query, '-out', output, '-outfmt', '6 qseqid sseqid pident length qlen stitle sblastnames', '-num_alignments', '1', '-max_hsps', '1', '-db', 'nt', '-num_threads', '56'])

parameter_input()
pipeline()
