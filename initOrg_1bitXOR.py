''' Create a starting organism for the initial population, and return it. '''

import Common
import Organism
import Genes
import random

''' Default connections. '''
c0 = None
c1 = None
c2 = None

def commonInit():
    ''' For initial testing, just try to compute a 1-bit XOR '''
    Common.nInNodes = 3 #1 bit from each input + 1 bias node
    Common.nOutNodes = 1

def optOrg():
    ''' Create an optimum organism for this fitness measure. '''
    print('Creating optimal 1bitXOR org')
    
    ''' Optimal organism is as follows (thresholds in parentheses):
    
                        OUT(0.5)
                       1/  |   \1
                       /   |-2  \
                      | MID(1.5) |
                      |/1      1\|
                      +          +
                     /            \
        BIAS(IN0)  IN1            IN2
        
    '''
    
    org = Organism.Organism()
    
    org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object.
    org.nodeMap = dict(Common.ioNodeMap)
    org.revGeneMap = dict(Common.revMapInit)    
    
    ''' Thresholds on input nodes don't matter - they're not actually used for anything. '''
    ''' Set output threshold. '''
    assert(org.nodeGenes[3].nodeType == 'Out')
    org.nodeGenes[3] = org.nodeGenes[3].clone()
    org.nodeGenes[3].thresh = 0.5
    
    ''' Direct input to output connections: '''
    optC0 = Genes.ConnectionGene('Con')
    optC0.conn = (Common.ioNodes[1].nodeNum, Common.ioNodes[3].nodeNum)
    optC0.weight = 1.0    
    org.addConn(optC0, org)
    
    optC1 = Genes.ConnectionGene('Con')
    optC1.conn = (Common.ioNodes[2].nodeNum, Common.ioNodes[3].nodeNum)
    optC1.weight = 1.0  
    org.addConn(optC1, org)
    
    ''' Middle node. '''
    midNode = Genes.NodeGene('Mid')
    midNode.thresh = 1.5
    org.addNode(midNode)
    
    ''' Input to middle node connections: '''
    optC2 = Genes.ConnectionGene('Con')
    optC2.conn = (Common.ioNodes[1].nodeNum, midNode.nodeNum)
    optC2.weight = 1.0  
    org.addConn(optC2, org)
    
    optC3 = Genes.ConnectionGene('Con')
    optC3.conn = (Common.ioNodes[2].nodeNum, midNode.nodeNum)
    optC3.weight = 1.0
    org.addConn(optC3, org)
    
    ''' Mid node to output connection: '''
    optC4 = Genes.ConnectionGene('Con')
    optC4.conn = (midNode.nodeNum, Common.ioNodes[3].nodeNum)
    optC4.weight = -2.0
    org.addConn(optC4, org)
    
    return org    

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
    
        ''' For the very first organism, provide an optimal organism for testing, if requested. '''
        if (Common.startWithOptOrg):
            org = optOrg()
            print('optOrg: ')
            for node in org.nodeGenes:
                print(node)
            for conn in org.connGenes:
                print(conn)
            print('Opt. Fitness: ' + str(org.compFitness()))
            #assert(0)
            return org
    
    ''' Add connections to the organism, with a random weight. '''
    c0.weight = random.uniform(-1.0, 1.0)
    org.addConn(c0, org)
    c1.weight = random.uniform(-1.0, 1.0)
    org.addConn(c1, org)
    if random.choice((True, False)):
        c2.weight = random.uniform(-1.0, 1.0)
        org.addConn(c2, org)
        
    return org    