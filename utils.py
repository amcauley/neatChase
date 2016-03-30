import math
import random

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x, offset = 0):
    return 1.0/(1.0 + math.exp(-4*(x-offset)))

def randTest():
    random.seed(0)
    print('rand: ' + str(random.random()))
    #print('pause')
    print('rand: ' + str(random.random()))
    
    return
    
if __name__ == "__main__":
    randTest()