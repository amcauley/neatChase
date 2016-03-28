'''Population size'''
popSize = 300

''' Max number of generations to simulate. '''
maxGens = 150

''' Compatibility distance threshold, d_t in Stanley pg. 110. ''' 
compatThresh = 0.5

''' Enable extra output messages. This will be turned on automatically if running the testEnv.py file. '''
extraPrintEn = False

''' Threshold size of species, >= than which we will propagate the fittest organism into the next generation, unmodified. '''
propFittestUnmodThresh = 4

''' File defining the fitness metric. Each file has a 'fitness' function. This file will change
    depending on the problem being investigated. ''' 
fitnessFunc = 'fitness_1bitXOR'

initOrgFile = 'initOrg_1bitXOR'

''' Flag to use randSeed below to seed the RNG. '''
useFixedSeed = True

''' Random number seed used for actual runs (testEnv doesn't necessarily use this). '''
randSeed = 0

'''Compatibility coefficients'''
coefC1 = 1.0
coefC2 = 1.0
coefC3 = 0.4

''' Upper and lower limits for transfer function threshold. '''
tfThreshLow  = -5.0
tfThreshHigh =  5.0

''' Square sensor grid size, centered on organism. Should be an odd number so that organism occupies the center square. '''
sensorGridDim = 3

''' Number of input nodes. This count includes input grid squares (check for presence of obstacle/enemy/etc.)
    and output controls (angle adjust, velocity, etc.).
    
    Input Node Mapping:
        - sensorGridDim^2 values for the obstacle sensor grid (0 = no obstacle/wall, 1 = obstacle/wall)
        - 2 values for self x,y velocity
        - 2 values for enemy x,y location relative to organism location
        - 2 values for enemy x,y velocity
        
        = sensorGridDim^2 + 6 input nodes
        
    Output Node Mapping:
        - 1 value for speed adjust (slow down/speed up)
        - 1 value for heading adjust (modify velocity direction)
        
        = 2 output nodes
'''
#nInNodes = sensorGridDim*sensorGridDim + 6
#nOutNodes = 2        

''' For initial testing, just try to compute a 1-bit XOR '''
nInNodes = 3 #1 bit from each input, 1 bias node
nOutNodes = 1


''' Input/Output nodes. These will be common to all organisms, even if the i/o nodes
    end up unused for a particular organism. Stored as a list, so order is important (input nodes first, then out nodes,
    then anything else). '''
ioNodes = []

''' Common node -> index mapping for I/O node Genes. '''
ioNodeMap = {}

''' Initialize reverseGeneMap for input nodes. '''
revMapInit = {}

''' Counters to track node innovation numbers '''
lastNodeInnovation = -1
lastConnNodeInnovation = -1

''' Max Organism addConn() attempts before giving up. If we can't generate a valid connection after these many tries, just move on. '''
maxAddConnAttempts = 3

''' Max attempts to add a new node - could fail if we don't find an enabled connection. '''
maxAddNodeAttempts = 3

''' Probability of adding a new node during a mutation. '''
addNodeProb = 0.1

''' Probability of adding a new connection during a mutation. '''
addConnProb = 0.15

''' Probability of a genome having its connection weights mutated. '''
weightMutateProbGenomeConn = 0.8

''' Probability of assigning new random weight if connection weights are being mutated.
    This is the probability applied to each connection weight in the genome. '''
weightMutateProbConn = 0.1

''' Probability of a genome having its node weights/thresholds mutated. '''
weightMutateProbGenomeNode = 0.5

''' Probability of assigning new random weight/threshold if node weights are being mutated.
    This is the probability applied to each node weight/threshold in the genome. '''
weightMutateProbNode = 0.1

''' Percent of offspring resulting from mutation without crossover. '''
selfMutateRatio = 0.25

''' Chance an inherited gene is disabled if it was disabled in either parent. '''
stillDisProb = 0.75

''' Interspecies mating rate. '''
interSpecRate = 0.001 