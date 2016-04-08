'''Population size'''
popSize = 500

''' Max number of generations to simulate. '''
maxGens = 100

''' Target number of species. '''
targetNumSpecs = 100

''' Max Fitness limit. In some fitness measures, like pred/prey, limit the max fitness / max number of iterations of the
    chase loop. The value here can be overridden in the initOrg commonInit() routine for the fitness measure. '''
maxFitness = 100

''' Starting compatibility distance threshold, d_t in Stanley pg. 110 and starting step size for control loop. ''' 
compatThresh = 1.0
compatStep = 0.2
maxCompatThresh = 10.0 #Maximum allowed threshold (0 is the minimum)

''' Threshold size of species, >= than which we will propagate the fittest organism into the next generation, unmodified. '''
propFittestUnmodThresh = 5

''' File defining the fitness metric. Each file has a 'fitness' function. This file will change
    depending on the problem being investigated. ''' 
fitnessFunc = 'fitness_prey'

initOrgFile = 'initOrg_prey'

'''Compatibility coefficients'''
coefC1 = 1.0
coefC2 = 1.0
coefC3 = 0.4

''' Upper and lower limits for transfer function threshold. '''
tfThreshLow  =  0.0
tfThreshHigh =  2.0      

''' Max Organism addConn() attempts before giving up. If we can't generate a valid connection after these many tries, just move on. '''
maxAddConnAttempts = 3

''' Max attempts to add a new node - could fail if we don't find an enabled connection. '''
maxAddNodeAttempts = 3

''' Number of generations after which a species won't be allowed to reproduce if it's shown no improvement in maximum fitness. '''
noImprovementGenLim = 20

''' Probability of adding a new node during a mutation. '''
addNodeProb = 0.03

''' Probability of adding a new connection during a mutation. '''
addConnProb = 0.3

''' Probability of a genome having its connection weights mutated. '''
weightMutateProbGenomeConn = 0.8

''' Probability of assigning new random weight if connection weights are being mutated.
    This is the probability applied to each connection weight in the genome. '''
weightMutateProbConn = 0.1

''' Probability of a genome having its node weights/thresholds mutated. '''
weightMutateProbGenomeNode = 0.2

''' Probability of assigning new random weight/threshold if node weights are being mutated.
    This is the probability applied to each node weight/threshold in the genome. '''
weightMutateProbNode = 0.1

''' Percent of offspring resulting from mutation without crossover. '''
selfMutateRatio = 0.25

''' Chance an inherited gene is disabled if it was disabled in either parent. '''
stillDisProb = 0.75

''' Chance of organism undergoing connection disable/enable flipping. '''
mutateDisFlipProbGenome = 0.05

''' Chance of flipping an individual connection's enabled/disable status during a mutation. '''
mutateDisFlipProb = 0.1

''' Interspecies mating rate. '''
interSpecRate = 0.001 

''' If an organism's genome size is less than this, just normalize by N=1 in compatibility distance
    computation. '''
useGenomeSizeOneThresh = 20

''' Parameter fed to random number generator for organism index selector - see utils.py orgSelectPdfRand(). '''
orgPdfOffset = 0.5

########## COMMON PARAMS - DO NOT TOUCH ##########
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

########## DEBUG PARAMS ##########

''' Basic prints. '''
basicPrintEn = True

''' Enable extra output messages. This will be turned on automatically if running the testEnv.py file. '''
extraPrintEnFitness = True
extraPrintEnCompat = False
extraPrintEnPopInfo = False

''' Provide the initial population with an optimum organism to start off with. '''
startWithOptOrg = False
