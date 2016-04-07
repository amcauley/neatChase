import math
import random
import neatChase
import Common

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x, offset = 0):
    return 1.0/(1.0 + math.exp(-10*(x-offset)))

''' Greater Than Zero test. '''
def isGTZ(x):
    return x > 0

''' Generate a random number according to the following PDF, which can be used to select an organism from a 
    fitness-sorted listed. Lower values/indices are more likely, since more fit organisms are more likely
    to be allowed to mate. '''    
def orgSelectPdfRand(b = 1.0):
    ''' PDF: p(x) = a/(x+b)^2
        By the constraint of all results falling in the range x = [0, 1), we get a = b^2 + b
        CDF: C(x) = (b+1)x/(b+x)

        To transform a uniform distribution (as returned by random.random()) into this desired distribution,
        we need to transform the uniform distribution by the *inverse* of the desired CDF:

        Cinv(x) = x*b/(b+1-x)
            
        The parameter b can adjusted subject to b > 0. The larger b gets, the more uniform the distribution
        becomes. '''
            
    x = random.random()
    a = b*(b+1.0)
    y = x*b/(b+1.0-x)
    return y
    
''' Test function for verifying pdf. Create a histogram of <bins> number of bins. '''
def testPdf(runs=10000, bins=10, b=0.4):
    binCnt = [0]*bins
    for k in range(runs):
        bin = int(orgSelectPdfRand(b)*bins)
        assert (bin < bins)
        binCnt[bin] += 1
        
    ''' Display output. '''        
    for k in range(bins):
        print('[' + str(k) + ']: ' + str(binCnt[k]))
        
''' Generate statistics about how often a program "succeeds." '''        
def testStats():
    Common.basicPrintEn = False
    numSuc = 0
    numRuns = 100
    print('start...')
    for k in range(numRuns):
        if neatChase.runProg() > 9.0:
            numSuc += 1
        print('run ' + str(k+1) + '/' + str(numRuns) + ', ' + str(numSuc*100.0/(k+1.0)) + '% success.')
        
if __name__ == "__main__":
    testStats()        