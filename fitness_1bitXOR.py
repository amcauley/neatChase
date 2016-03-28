''' Fitness evaluation function for 1 bit XOR function.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as (4 - <sum of distance squared between output and actual XOR result for each possible input combo>),
            00 -> 0
            01 -> 1
            10 -> 1
            11 -> 1 
            
    There are 3 bits fed into each output computation: 1 bias bit and 2 bits to be XOR'd.
'''

import Common

def fitness(org):
    assert(Common.initOrgFile == 'initOrg_1bitXOR')
    
    outSum = 0
    
    ''' 0 XOR 0 = 0 '''
    input = [1, 0, 0]
    output = org.compOutput(input)
    output = 1 - output[0]
    outSum += output

    ''' 0 XOR 1 = 1 '''
    input = [1, 0, 1]
    output = org.compOutput(input)
    output = output[0]
    outSum += output

    ''' 1 XOR 0 = 1 '''
    input = [1, 1, 0]
    output = org.compOutput(input)
    output = output[0]
    outSum += output

    ''' 1 XOR 1 = 0 '''
    input = [1, 1, 1]
    output = org.compOutput(input)
    output = 1 - output[0]
    outSum += output
        
    fitness = 4.0 - outSum
    fitness = fitness*fitness
    
    if Common.extraPrintEn:
        print('fitness (1bitXOR) = ' + str(fitness))
    
    return fitness