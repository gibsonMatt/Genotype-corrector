from scipy.stats import chisquare
from optparse import OptionParser

msg_usage = '''python %prog [options]
example:
python ChiSquare_test.py -i input -p F2 or RIL -d 1~10 -o output'''
descr = '''DESCRIPTION: Filter phenotype frequencies using chisquare test
with different levels of stringency. For F2 population, test A:B against the
expected ration of 1:1. For RILs population, except for testing against 1:1, the
heterizygous proportion should not exceed 50%.
'''

optparser = OptionParser(usage = msg_usage, description = descr)
optparser.add_option('-i', '--genotype-matrix', dest = 'matrix_filename',
                     help = '''The genotype matrix file is tab delimited text
containing each sample's marker in each position. For more detail about genotype
matrix file please see our wiki page:
(https://github.com/freemao/Genotype-corrector/wiki/Genotype-Corrector).''')
optparser.add_option('-p', '--population_type', dest = 'population',
                     help = "set the population type, F2 or RIL")
optparser.add_option('-d', '--degree', dest = 'degree_level',
                     help = '''integer, 1 corresponds to the the pvalue of 1e-11(less strigenct)
for chisquare test, 10 corresponds to 1e-2 (more strigent). Users can test
different degrees(1-10) to get a reseanable result''')
optparser.add_option('-o', '--output', dest = 'output_filename',
                     help = 'Write the filtered results to this file.')
options, args = optparser.parse_args()

import numpy as np

def F2chitest(mapfile, p_value, output):
    f2 = open(output, 'w')
    expect_rate = np.array([0.5, 0.5])
    f = open(mapfile)
    firline = f.readline()
    f2.write(firline)
    for i in f:
        a_count = i.count('\tA')
        b_count = i.count('\tB')
        observed = np.array([a_count, b_count])
        cvalue, pvalue = chisquare(observed, expect_rate*np.sum(observed))
        if pvalue > p_value:
            f2.write(i)

def RILchitest(mapfile, p_value, output):
    f2 = open(output, 'w')
    expect_rate = np.array([0.5, 0.5])
    f = open(mapfile)
    firline = f.readline()
    f2.write(firline)
    N = len(firline.split()[1:])
    for i in f:
        a_count = i.count('\tA')
        b_count = i.count('\tB')
        x_count = i.count('\tX')
        hetero_rate = x_count/float(N)
        if hetero_rate <= 0.5:
            observed = np.array([a_count, b_count])
            cvalue, pvalue = chisquare(observed, expect_rate*np.sum(observed))
            if pvalue > p_value:
                print a_count,b_count
                f2.write(i)

if __name__ == "__main__":
    I = options.matrix_filename
    P = options.population
    D = options.degree_level
    O = options.output_filename
    if I and P and D and O:
        Pvalue = float('1e%s'%(int(D)-12))
        print Pvalue
        if P == 'F2':
            F2chitest(I,Pvalue, O )
        elif P == 'RIL':
            RILchitest(I,Pvalue, O )
        else:
            print 'Add -h to show help.'
    else:
        print 'Add -h to show help.'
