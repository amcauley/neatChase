import Common
import collections

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
        vice versa). '''
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

    for n in range(Common.nInNodes):          
        nodeQ = collections.deque() # New queue to track loops in this path from starting node
        nodeQ.appendleft(self.nodeGenes[n])
        while nodeQ: # While the queue isn't empty, follow the graph and check for nodes visited 
        
        
    def __str__(self):
        retStr = ""
        for node in self.nodeGenes:
            retStr += str(node) + "\n"
        
        return retStr