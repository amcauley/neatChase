''' Fitness evaluation function that always returns 0, for testing.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as (4 - <sum of distance squared between output and actual XOR result for each possible input combo>),
            00 -> 0
            01 -> 1
            10 -> 1
            11 -> 1 
'''

def fitness(org):
    
    print('fitness (zero) = 0')
    
    return 0