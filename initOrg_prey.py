''' Create a starting organism for the initial population, and return it. '''

import Common
import Organism
import Genes
import random

def commonInit():
    ''' 9 inputs: 1 bias node and 8 inputs for the squares surrounding the prey. '''
    Common.nInNodes = 9
    Common.nOutNodes = 4 # Movement cmds: up/down/left/right

def optOrg():
    ''' Create an optimum organism for this fitness measure. '''
    print('Creating optimal 1bitXOR org')
    
    assert(0) # Optimal prey not yet implemented
    
    return org    

def initOrg():
    ''' Initialization makes assumptions specific to the 1 bit XOR case - make sure the rest of the code agrees with these assumptions. '''
    assert(Common.fitnessFunc == 'fitness_prey')
    assert(Common.nInNodes == 9)
    assert(Common.nOutNodes == 4)
    
    org = Organism.Organism()
    
    org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object.
    org.nodeMap = dict(Common.ioNodeMap)
    org.revGeneMap = dict(Common.revMapInit)    
    
    assert(0) # Prey initOrg not yet implemented
        
    return org    