import subprocess, glob, string, re

def size_input():
    """Sets size cut-off and check for valid user input."""
    global size
    while True:
        size = raw_input('Enter size cut-off for SPAdes output (Press enter for 500 bp default): ')
        if size == '':
            size = 500
            break
        elif not size.isdigit():
            print 'Invalid input. Please try again'
            continue
        else:
            break 

def cov_input():
    """Sets coverage cut-off and check for valid user input."""
    global cov
    while True:
        cov = raw_input('Enter coverage cut-off for blast output (Press enter for 10 times default): ')
        if cov == '':
            cov = 10
            break
        elif not cov.isdigit():  
            print 'Invalid input. Please try again'
            continue
        else:
            break 

def assemble_type():
    """Asks user what settings they would like to use for SPAdes assembly"""
    global assemble_choice, final_choice
    while True:
        print '\nWhat type of SPAdes assembly would you like to run?\n'
        print '   1) SPAdes w/ error correct and assemble'
        print '   2) SPAdes careful w/ error correct and assemble'
        print '   3) metaSPAdes w/ error correct and assemble'
        print '   4) SPAdes w/ assemble only'
        print '   5) SPAdes careful w/ assemble only'
        print '   6) metaSPAdes w/ assemble only'
        print '   7) Custom input (manually enter options)\n'
        assemble_choice = raw_input('Enter the number for your selection: ')
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
            print '\nEnter modifiers/parameters as you would enter then into a manual SPAdes run (eg. --meta).'
            print 'Do not enter input file name(s) and output folder name as they will be automatically selected.'
            final_choice = raw_input('Enter custom options: ')
            break
        else:
            print 'Invalid input. Please try again'
            continue

def parameter_input():
    """Sets cut-off parameters and checks if they are correct."""
    while True:
        size_input()
        cov_input()
        assemble_type()
        print '\n***CURRENT SETTINGS***\n   - Size cut-off:', size, 'bp\n   - Coverage cut-off:', cov, 'times\n   - Assembly type:', final_choice
        begin = raw_input('\nContinue (Y/N)? ').lower()
        if begin[0] == 'y':
            break
        else:
            print 'Please try again. \n'
            continue

def fasta_to_tab():
    """Converts fasta output from SPAdes into tab format for easier filtering"""
    with open(out + '/' + 'contigs.fasta', 'r') as f, open(out + '/' + 'contigs.tab', 'w') as file_out:
        for line in f:
            line = line.strip()
            if line[0] == '>':
                 file_out.write('{}\t'.format(line))
            else:
                 file_out.write('{}\n'.format(line))

def size_filter():

def pre_blast_filter():
    fasta_to_tab()
    subprocess.call([])

def pipeline():
    """Finds each set of paired reads and assigns them to variable R1 and R2.
    Generates name for output file from name of R1.
    Runs SPAdes assembly on all paired files in current directory."""
    for file in glob.glob('*_R1_*fastq*'):
        global R1, R2, out
        R1 = file
        R2 = string.replace(R1, '_R1_', '_R2_')
        out = re.sub(r'.fastq.*', '', R1) + '_SpadesOutput'
        if assemble_choice == '1':                              
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out])
        elif assemble_choice == '2':
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, '--careful'])
        elif assemble_choice == '3':
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, '--meta'])
        elif assemble_choice == '4':                                                                                                                                            
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, '--only-assembler'])                                                                       
        elif assemble_choice == '5':
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, '--careful', '--only-assembler'])
        elif assemble_choice == '6':
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, '--meta', '--only-assembler'])
        elif assemble_choice == '7':
            subprocess.call(['echo', 'spades.py', '-1', R1, '-2', R2, '-o', out, final_choice])
        pre_blast_filter()

parameter_input()
pipeline()