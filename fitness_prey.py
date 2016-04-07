''' Fitness evaluation function for prey in pred/prey chase.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as how many rounds the organism lasts IN THE ARENA THIS SUNDAY.
    
    1 bias input.
    
    8 danger inputs (top left, top mid, top right, left, right, bot left, bot mid, bot right), which are
    binary values: 0 means safe, 1 means danger (either the predator or the edge of the arena).
    
    4 outputs - (move up, move down, move left, move right). If two contradictory directions, those cancel
    out.
'''

import Common

def fitness(org, indvTestPrint = False):
    assert(Common.initOrgFile == 'initOrg_prey')