import math
import random

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x, offset = 0):
    return 1.0/(1.0 + math.exp(-4*(x-offset)))
