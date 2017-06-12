#!/usr/bin/env python3

import subprocess
import glob
import os
from Bio import SeqIO
from collections import defaultdict
import re

def size_input():
    """Sets size cut-off and check for valid user input."""
    global size
    while True:
        size = input('Enter size cut-off for SPAdes output (Press enter for 500 bp default): ')
        if size == '':
            size = 500
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
        cov = input('Enter coverage cut-off for blast output (Press enter for 10 times default): ')
        if cov == '':
            cov = 10
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
        
        for keys,values in cov_dir.iteritems():
            contig_dict[keys] = [v for v in values if 
                    float(v.name.split('_')[3]) >= float(size_input()) and 
                    float(v.name.split('_')[5]) >= float(cov_input())
                    ]
            
            filtered_filename = str.replace(k,".fasta","")
            
            new_extension = "filtered.fasta"
            
            SeqIO.write(v, os.path.join(filtered_filename + new_extension), 'fasta')

def pipeline():
    """Finds each set of paired reads and assigns them to variable R1 and R2.
    Generates name for output file from name of R1.
    Runs SPAdes assembly on all paired files in current directory."""
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
        #pre_blast_filter()

parameter_input()
pipeline()
size_filter()
coverage_filter()
