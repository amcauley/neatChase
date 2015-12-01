import math

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x):
    return 1.0/(1.0 + math.exp(-4*x))