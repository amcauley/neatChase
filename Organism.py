import Common
import random

def nodeHasLoop(org, nodeNum, visitedSet):
    if nodeNum in visitedSet:
        return True
    else:
        if nodeNum in org.geneMap:
            for nextNode in org.geneMap:
                nextNodeInLoop = nodeInLoop(org, nextNode, set(visitedSet).append(nodeNum))
                if nextNodeInLoop:
                    return True
    return False
    

class Organism:
    def __init__(self):
        self.fitness = -1
        self.species = -1
        self.nodeGenes = {}
        self.connGenes = {}
        
        ''' Dictionary where the key is a nodeGene number, and the value is a set of all nodes the input nodeGene connects to (from this node to other nodes, not
        vice versa). This only tracks active nodes, not disabled ones. '''
        self.geneMap = {}
        
    def containsLoop(self):
        ''' Check if this organism contains a loop in the nodes / directed graph. This is not currently supported.
            Return a boolean value - True if a loop exists, False if it doesn't. '''
        for each input node
            follow the connections, add new nodes to a queue, mark visited nodes in a dictionary/hash-set
            if we've already visited a node, return true
            
            if we have a branch at a node, we'll create a new visited set to search for duplicates for each branch.
            i.e. left branch will have [old visited set up to this node | new visited set for left branch] and one for
            right branch. This should keep us from marking A -> {B,C}, B -> D, C -> D as a loop (since D is visited twice, but only once per branch)
            
            note - use helper function nodeHasLoop

        
    def addNode(self):
        ''' Adds a node by splitting an existing connection. If no connection exists, don't do anything. '''
        if (len(self.connGenes) == 0):
            return
        else:
            
            newNode = Genes.NodeGene("Mid") #create the new node
            
            connGene = random.choice(tuple(self.connGenes)) #select which two (connected) nodes the new one will fall between
            startNodeNum = connGene.conn[0]
            oldDestNodeNum = connGene.conn[1]
            
            connGene.conn[1] = newNode.nodeNum
            geneMapStartEntry = self.geneMap{startNodeNum}
            geneMapStartEntry.remove(oldDestNodeNum)
            geneMapStartEntry.add(newNode.nodeNum)
            self.geneMap[newNode.nodeNum] = {oldDestNodeNum}
          
            ''' Disable the old connection gene - it will be replaced by two new ones (A->C becomes A->B and B->C, where B is the newly added node). '''
            connGene.disabled = True
            newConn1 = Genes.ConnectionGene("Con") #A->B
            newConn1.conn = (startNodeNum, newNode.nodeNum)
            newConn1.weight = connGene.weight
            newConn2 = Genes.ConnectionGene("Con") #B->C
            newConn2.conn = (newNode.nodeNum, oldDestNodeNum)
            newConn2.weight = 1 #to preserve original overall weight from A->C            
          
            ''' Update the organism with the new genes/connections. '''
            self.nodeGenes.add(newNode)
            self.connGenes.add(newConn1)
            self.connGenes.add(newConn2)
            
    
    def addConn(self):
        ''' Adds a connection gene. After adding, check if the new node results in a loop. If so, regenerate a connection to use as the new one. Repeat until
            a valid non-looping connection is created. '''
    
        
    def __str__(self):
        retStr = ""
        for node in self.nodeGenes:
            retStr += str(node) + "\n"
        
        return retStr