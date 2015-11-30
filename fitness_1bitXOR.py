''' Fitness evaluation function for 1 bit XOR function.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as (4 - <sum of distance squared between output and actual XOR result for each possible input combo>),
            00 -> 0
            01 -> 1
            10 -> 1
            11 -> 1 
            
        We'll peg the output range between 0 and 1.   
'''

def fitness(org):
    
    diffCnt = 0
    
    ''' 0 XOR 0 = 0 '''
    input = [1, 0, 0]
    output = org.compOutput(input)
    output = 1 - max(min(output[0], 1), 0)
    diffCnt = diffCnt + output*output

    ''' 0 XOR 1 = 1 '''
    input = [1, 0, 1]
    output = org.compOutput(input)
    output = max(min(output[0], 1), 0)
    diffCnt = diffCnt + output*output

    ''' 1 XOR 0 = 1 '''
    input = [1, 1, 0]
    output = org.compOutput(input)
    output = max(min(output[0], 1), 0)
    diffCnt = diffCnt + output*output

    ''' 1 XOR 1 = 0 '''
    input = [1, 1, 1]
    output = org.compOutput(input)
    output = 1 - max(min(output[0], 1), 0)
    diffCnt = diffCnt + output*output
        
    fitness = diffCnt
    
    print('fitness = ' + str(fitness))
    
    return fitness