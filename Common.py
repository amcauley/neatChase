'''Population size'''
popSize = 1

'''Compatibility coefficients'''
coefC1 = 1.0
coefC2 = 1.0
coefC3 = 0.4

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

''' Compatibility distance threshold, d_t in Stanley pg. 110. ''' 
compatThresh = 3.0
