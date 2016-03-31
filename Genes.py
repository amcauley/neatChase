import Common

class NodeGene:
    def __init__(self, type, skipInc = False):
        if not skipInc:
            Common.lastNodeInnovation += 1 # Bump up innovation counter
        self.nodeNum = Common.lastNodeInnovation # Node innovation number
        self.nodeType = type #In, Mid, Out    
        self.thresh = 0.0 #Threshold for outputting 0 or 1 (roughly speaking, since transfer function can be continuous, allowing numbers in between)
        
    ''' Return a new instance of this gene. '''    
    def clone(self):    
        newNode = NodeGene(self.nodeType, True)
        newNode.nodeNum = self.nodeNum
        newNode.thresh = self.thresh
        return newNode

    def __lt__(self, other):
        assert(self.nodeNum != other.nodeNum)
        return self.nodeNum < other.nodeNum
        
    def __str__(self):
        return 'num ' + str(self.nodeNum) + '\n' +\
               'type ' + str(self.nodeType) + '\n' +\
               'thresh ' + str(self.thresh) + '\n'
        
class ConnectionGene:
    def __init__(self, type, skipInc = False):
        if not skipInc:
            Common.lastConnNodeInnovation += 1 # Bump up innovation counter
        self.nodeNum = Common.lastConnNodeInnovation # Connection node innovation number
        self.nodeType = type
        self.disabled = False      
        self.conn = (-1, -1) # Tuple describing the start and end NodeGenes of this connection
        self.weight = 0.0    # Connection weight
        
    ''' Return a new instance of this gene. '''    
    def clone(self):    
        newConn = ConnectionGene(self.nodeType, True)
        newConn.nodeNum = self.nodeNum
        newConn.disabled = self.disabled
        newConn.conn = self.conn
        newConn.weight = self.weight
        return newConn        
        
    def __lt__(self, other):
        assert(self.nodeNum != other.nodeNum)
        return self.nodeNum < other.nodeNum
        
    def __str__(self):
        return 'num ' + str(self.nodeNum) + '\n' +\
               'type ' + str(self.nodeType) + '\n' +\
               'dis ' + str(self.disabled) + '\n' +\
               'conn ' + str(self.conn) + '\n' +\
               'weight ' + str(self.weight) + '\n'