''' Fitness evaluation function for 1 bit XOR function.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as (4 - <sum of distance squared between output and actual XOR result for each possible input combo>),
            00 -> 0
            01 -> 1
            10 -> 1
            11 -> 1 
'''

import Common

def fitness(org):
    
    outSum = 0
    
    ''' 0 XOR 0 = 0 '''
    input = [1, 0, 0]
    output = org.compOutput(input)
    output = 1 - output[0]
    outSum = outSum + output*output

    ''' 0 XOR 1 = 1 '''
    input = [1, 0, 1]
    output = org.compOutput(input)
    output = output[0]
    outSum = outSum + output*output

    ''' 1 XOR 0 = 1 '''
    input = [1, 1, 0]
    output = org.compOutput(input)
    output = output[0]
    outSum = outSum + output*output

    ''' 1 XOR 1 = 0 '''
    input = [1, 1, 1]
    output = org.compOutput(input)
    output = 1 - output[0]
    outSum = outSum + output*output
        
    fitness = outSum
    
    if Common.extraPrintEn:
        print('fitness (1bitXOR) = ' + str(fitness))
    
    return fitness