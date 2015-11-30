import Common

class NodeGene:
    def __init__(self, type):
        Common.lastNodeInnovation += 1 # Bump up innovation counter
        self.nodeNum = Common.lastNodeInnovation # Node innovation number
        self.nodeType = type
        self.disabled = False
        self.species = -1
        
    def __str__(self):
        return 'num ' + str(self.nodeNum) + '\n' +\
               'type ' + str(self.nodeType) + '\n' +\
               'dis ' + str(self.disabled) + '\n' +\
               'spec ' + str(self.species) + '\n'
        
class ConnectionGene:
    def __init__(self, type):
        Common.lastConnNodeInnovation += 1 # Bump up innovation counter
        self.nodeNum = Common.lastConnNodeInnovation # Connection node innovation number
        self.nodeType = type
        self.disabled = False
        self.species = -1        
        self.conn = (-1, -1) # Tuple describing the start and end NodeGenes of this connection
        self.weight = 0     # Connection weight
        
    def __str__(self):
        return 'num ' + str(self.nodeNum) + '\n' +\
               'type ' + str(self.nodeType) + '\n' +\
               'dis ' + str(self.disabled) + '\n' +\
               'spec ' + str(self.species) + '\n' +\
               'conn ' + str(self.conn) + '\n' +\
               'weight ' + str(self.weight) + '\n'