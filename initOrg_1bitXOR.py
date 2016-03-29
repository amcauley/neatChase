''' Create a starting organism for the initial population, and return it. '''

import Common
import Organism
import Genes
import random

''' Default connections. '''
c0 = None
c1 = None
c2 = None

def initOrg():
    ''' Initialization makes assumptions specific to the 1 bit XOR case - make sure the rest of the code agrees with these assumptions. '''
    assert(Common.fitnessFunc == 'fitness_1bitXOR')
    assert(Common.nInNodes == 3)
    assert(Common.nOutNodes == 1)
    
    org = Organism.Organism()
    
    org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object.
    org.nodeMap = dict(Common.ioNodeMap)
    org.revGeneMap = dict(Common.revMapInit)
    
    ''' Default structure is from Fig. 5 of Stanley pg. 113, where we randomly choose whether bias node to output node connection is
        present. Connections from input 1 to output and input 2 to output are always present. Connection weights are randomly chosen,
        as are node thresholds. '''
     
    global c0
    global c1
    global c2
    
    ''' Only create these conn genes once. They'll be cloned within addConn if they're picked up. '''
    if c0 is None:
        c0 = Genes.ConnectionGene('Con')
        c0.conn = (Common.ioNodes[1].nodeNum, Common.ioNodes[3].nodeNum)
        
        c1 = Genes.ConnectionGene('Con')
        c1.conn = (Common.ioNodes[2].nodeNum, Common.ioNodes[3].nodeNum)
        
        ''' Bias connection. '''
        c2 = Genes.ConnectionGene('Con')
        c2.conn = (Common.ioNodes[0].nodeNum, Common.ioNodes[3].nodeNum)
    
    ''' Add connections to the organism, with a random weight. '''
    c0.weight = random.uniform(-1.0, 1.0)
    org.addConn(c0, org)
    c1.weight = random.uniform(-1.0, 1.0)
    org.addConn(c1, org)
    if True: #random.choice([True, False]):
        c2.weight = random.uniform(-1.0, 1.0)
        org.addConn(c2, org)
        
    return org    