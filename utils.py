import math
import random

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x, offset = 0):
    return 1.0/(1.0 + math.exp(-10*(x-offset)))

''' Greater Than Zero test. '''
def isGTZ(x):
    return x > 0