''' Fitness evaluation function for 1 bit XOR function.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as (4 - <sum of distance squared between output and actual XOR result for each possible input combo>)^2,
            00 -> 0
            01 -> 1
            10 -> 1
            11 -> 1 
            
    There are 3 bits fed into each output computation: 1 bias bit and 2 bits to be XOR'd.
'''

import Common

def fitness(org, indvTestPrint = False):
    assert(Common.initOrgFile == 'initOrg_1bitXOR')
    
    outSum = 0
    
    ''' 0 XOR 0 = 0 '''
    input = [1, 0, 0]
    outputRaw = org.compOutput(input)
    output = outputRaw[0]
    outSum += output
  
    if (indvTestPrint):
        print('output 0^0: ' + str(outputRaw[0]))
  
    ''' 0 XOR 1 = 1 '''
    input = [1, 0, 1]
    outputRaw = org.compOutput(input)
    output = 1.0 - outputRaw[0]
    outSum += output

    if (indvTestPrint):
        print('output 0^1: ' + str(outputRaw[0]))    
    
    ''' 1 XOR 0 = 1 '''
    input = [1, 1, 0]
    outputRaw = org.compOutput(input)
    output = 1.0 - outputRaw[0]
    outSum += output

    if (indvTestPrint):
        print('output 1^0: ' + str(outputRaw[0]))    
    
    ''' 1 XOR 1 = 0 '''
    input = [1, 1, 1]
    outputRaw = org.compOutput(input)
    output = outputRaw[0]
    outSum += output
        
    if (indvTestPrint):
        print('output 1^1: ' + str(outputRaw[0]))        

    #print('geneMap: ' + str(org.geneMap))
    #print('revGeneMap: ' + str(org.revGeneMap))
    #assert(0)
      
    fitness = 4.0 - outSum
    fitness = fitness*fitness
    
    if Common.extraPrintEnFitness:
        print('fitness (1bitXOR) = ' + str(fitness))
    
    return fitness