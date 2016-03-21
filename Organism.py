import Common
import Genes
import random
import collections
import utils
import copy

''' See http://stackoverflow.com/questions/6677424/how-do-i-import-variable-packages-in-python-like-using-variable-variables-i '''
fitnessModule = __import__(Common.fitnessFunc) 

def nodeHasLoop(org, nodeNum, visitedSet):
    ''' check if organism (org) has a loop containing nodeNum, using visitedSet to track which nodes
        have been visited. 
        
        If we have a branch at a node, we'll create a new visited set to search for duplicates for each branch.
        i.e. left branch will have [old visited set up to this node | new visited set for left branch] and one for
        right branch. This should keep us from marking A -> {B,C}, B -> D, C -> D as a loop (since D is visited twice, but only once per branch) '''
        
    if nodeNum in visitedSet:
        return True
    else:
        if nodeNum in org.geneMap:
            for nextNode in org.geneMap[nodeNum]:
                newSet = set(visitedSet)
                newSet.add(nodeNum)
                nextNodeInLoop = nodeHasLoop(org, nextNode, newSet)
                if nextNodeInLoop:
                    return True
    return False
    

class Organism:
    def __init__(self):
        self.fitness = -1
        self.species = -1
        self.nodeGenes = []
        self.connGenes = []
        
        ''' Dictionary mapping nodeGene nodeNum (key) to that node's index within self.nodeGenes. '''
        self.nodeMap = {}
        
        ''' Dictionary where the key is a pair of (start node, dest. node) numbers, and the output is the index within the self.connGenes list corresponding to that
            particular connection. Expected use steps are 1) look up genes connected to input node by using self.geneMap, 2) look up the connection gene index using
            self.connMap, 3) retrieve the connection node from self.connGenes. '''
        self.connMap = {}        
        
        ''' Also track any disabled connections. Connections can move between connMap and disConnMap as they become enabled or disabled. '''
        self.disConnMap = {}
        
        ''' Dictionary where the key is a nodeGene number, and the value is a set of all nodes the input nodeGene connects to (from this node to other nodes, not
        vice versa). This only tracks active connections, not disabled ones. '''
        self.geneMap = {}
        
        ''' Reverse of the geneMap dictionary: key is a node number, and output is the set of all nodes feeding into that key node via non-disabled connections. Input from node 
            number -1 means this is an input node. '''
        self.revGeneMap = {}
        
    def containsLoop(self):
        ''' Check if this organism contains a loop in the nodes / directed graph. This is not currently supported.
            Return a boolean value - True if a loop exists, False if it doesn't. '''
        for inputNodeIdx in range(Common.nInNodes):
            if nodeHasLoop(self, self.nodeGenes[inputNodeIdx].nodeNum, set()): #start with an empty visitedSet - faster (on average) than initializing with inputNode, and a loop will still be detected anyway.
                return True
        return False

        
    def addNode(self, newNode = None):
        ''' If newNode has a value, add that node into this organism and return. '''
        if newNode is not None:
            newIdx = len(self.nodeGenes)
            self.nodeGenes.append(copy.deepcopy(newNode))
            self.nodeMap[newNode.nodeNum] = newIdx
            return
    
        ''' Adds a node by splitting an existing connection. If no connection exists, don't do anything. '''
        if (len(self.connGenes) == 0):
            return
        else:
            
            newNode = Genes.NodeGene("Mid") #create the new node
            
            connGene = random.choice(tuple(self.connGenes)) #select which two (connected) nodes the new one will fall between
            while (connGene.disabled): #keep trying until we get a non-disabled connection. Shouldn't be infinite loop since if connGenes is non-empty, at least one valid conn exists.
                connGene = random.choice(tuple(self.connGenes))
                
            startNodeNum = connGene.conn[0]
            oldDestNodeNum = connGene.conn[1]
            
            #print('startNodeNum ' + str(startNodeNum) + ', oldDestNodeNum ' + str(oldDestNodeNum) + '\n')
            
            geneMapStartEntry = self.geneMap[startNodeNum]
            geneMapStartEntry.remove(oldDestNodeNum)
            geneMapStartEntry.add(newNode.nodeNum)
            self.geneMap[newNode.nodeNum] = set([oldDestNodeNum]) #syntax trickery to form set out of integer
            
            ''' Update revGeneMap. '''
            self.revGeneMap[oldDestNodeNum].remove(startNodeNum) 
            self.revGeneMap[oldDestNodeNum].add(newNode.nodeNum)
            self.revGeneMap[newNode.nodeNum] = set([startNodeNum])
        
            ''' Move old connection to disConnMap. '''
            self.disConnMap[(startNodeNum, oldDestNodeNum)] = self.connMap[(startNodeNum, oldDestNodeNum)]
            del self.connMap[(startNodeNum, oldDestNodeNum)]
        
            ''' Disable the old connection gene - it will be replaced by two new ones (A->C becomes A->B and B->C, where B is the newly added node). '''
            connGene.disabled = True
            newConn1 = Genes.ConnectionGene("Con") #A->B
            newConn1.conn = (startNodeNum, newNode.nodeNum)
            newConn1.weight = connGene.weight
            newConn2 = Genes.ConnectionGene("Con") #B->C
            newConn2.conn = (newNode.nodeNum, oldDestNodeNum)
            newConn2.weight = 1 #to preserve original overall weight from A->C            
          
            ''' Update the organism with the new genes/connections. '''
            newIdx = len(self.nodeGenes)
            self.nodeGenes.append(newNode)
            self.nodeMap[newNode.nodeNum] = newIdx
            
            self.connMap[(startNodeNum, newNode.nodeNum)] = len(self.connGenes)            
            self.connGenes.append(newConn1)
            
            self.connMap[(newNode.nodeNum, oldDestNodeNum)] = len(self.connGenes)            
            self.connGenes.append(newConn2) 
            
    
    def addConn(self, newConn = None, refOrg = None):
        ''' Adds a connection gene. After adding, check if the new node results in a loop. If so, regenerate a connection to use as the new one. Repeat until
            a valid non-looping connection is created. If newConn and refOrg are not None, then we'll add newConn into this organism, and also add the starting and
            ending node genes from refOrg into this organism if suitable nodes don't already exist. '''
         
        if newConn is not None:
            
            if refOrg is None:
                assert(False) #if newConn is provided (indicating we're adding an existing connection to this organism), a refOrg should also have been provided
            
            ''' Add the existing connection to this organism, and set up start/stop nodes if needed. '''
            newIdx = len(self.connGenes)
            self.connGenes.append(copy.deepcopy(newConn))
            
            (startNodeNum, endNodeNum) = newConn.conn
            
            if (newConn.disabled):
                self.disConnMap[newConn.conn] = newIdx
            else:
                self.connMap[newConn.conn] = newIdx
                if (startNodeNum in self.geneMap):
                    self.geneMap[startNodeNum].add(endNodeNum) 
                else:
                    self.geneMap[startNodeNum] = set([endNodeNum])                    
            
                if (endNodeNum in self.revGeneMap):
                    self.revGeneMap[endNodeNum].add(startNodeNum)
                else:
                    self.revGeneMap[endNodeNum] = set([startNodeNum])
            
            if startNodeNum not in self.nodeMap:
                self.addNode(refOrg.nodeGenes[refOrg.nodeMap[startNodeNum]])
        
            if endNodeNum not in self.nodeMap:
                self.addNode(refOrg.nodeGenes[refOrg.nodeMap[endNodeNum]])
                
            return
        
        ''' We're not adding an existing connection, so proceed with adding a newly created one: '''
        success = 0
        for k in range(Common.maxAddConnAttempts):
            firstNode = random.choice(tuple(self.nodeGenes))
            secondNode = random.choice(tuple(self.nodeGenes))
            
            ''' If we selected the same node twice, continue to next attempt. '''
            if (firstNode == secondNode):
                continue
                
            ''' Tentatively add connection to geneMap and check for a cycle. If no cycle, accept the new connection. If there is a cycle, remove the tentative
                entry from geneMap and continue to a new attempt. '''
            # Probably a better way to add an element to a set while creating a set if one didn't already exist. Look into this later. Also, maybe default to placing
            # an empty set by default in geneMap when adding new nodes, so we can always assume some set exists, even if empty.
            if (firstNode.nodeNum not in self.geneMap):
                self.geneMap[firstNode.nodeNum] = set([secondNode.nodeNum])
            else:
                ''' If there's already a connection between first and second node, try generating a new combo. '''
                if (secondNode.nodeNum in self.geneMap[firstNode.nodeNum]):
                    continue
                else:    
                    ''' New connection - continue on to check for loops. '''
                    self.geneMap[firstNode.nodeNum].add(secondNode.nodeNum)    
                
            if self.containsLoop():
                ''' New connection creates a loop. Remove tentative entry from geneLoop and try again. '''
                self.geneMap[firstNode.nodeNum].remove(secondNode.nodeNum)
                continue
            else:
                ''' No loop. We already have the new connection in geneMap, just need to create a new connectionGene and add to self.connGenes. '''
                if (secondNode.nodeNum in self.revGeneMap):
                    self.revGeneMap[secondNode.nodeNum].add(firstNode.nodeNum)
                else:
                    self.revGeneMap[secondNode.nodeNum] = set([firstNode.nodeNum])
                newGene = Genes.ConnectionGene("Con")
                newGene.conn = (firstNode.nodeNum, secondNode.nodeNum)
                newGene.weight = 0 #default to no weight, i.e. useless connection. Evolution will later (probably) change this to nonzero.
                self.connMap[(firstNode.nodeNum, secondNode.nodeNum)] = len(self.connGenes) 
                self.connGenes.append(newGene)
                success = 1
                break
                
        print('addConn took ' + str(k+1) + ' attempts, success = ' + str(success)) 
        return
        
        
    def compOutput(self, inputValList):
        ''' Take input list (one value per input node) and propagate those values through the neural network. The return value should be outputValTuple,
            which is a list of values, where index i corresponds to the ith output node, i ranges from 0 to Common.nOutNodes-1. 
            
            The plan is to breadth first search through geneMap using a queue of tuples/pairs: (nodeNum, inputVal). We'll initialize the queue of nodes to visit with
            values from inputValList. outputValList is initialized to all zeros, and each time we read an output node from the queue, we add the value fed to it to
            the sum in the corresponding index. Once the queue is empty, we've visited all needed nodes and propagated all values, and our processing is done.

            In order to support non-linear transfer functions of the node inputs, we need to sum all inputs before feeding into the transfer function (instead of feeding each
            input into the transfer function and then summing the outputs). To do this, we keep a list of all inputs received into a node, and once all inputs have been
            received (according to self.revGeneMap), then we can export this node's value to other nodes. '''
            
        q = collections.deque()
        outputValList = [0 for x in range(Common.nOutNodes)]
        
        ''' Make sure the inputValList is a valid length. '''
        assert(len(inputValList) == Common.nInNodes)
        
        nodeInputs = {} #dictionary: key = node number, value is set input values. Once set size equals total number of inputs, node is ready for propagation
        
        ''' Initialize processing queue to input nodes and their input vals. '''
        for idx in range(Common.nInNodes):
            num = Common.ioNodes[idx].nodeNum
            q.append((num, inputValList[idx])) #add tuple of (nodeNum, inputVal) to processing queue
            
        while q:
            (currNodeNum, currVal) = q.popleft()
            
            ''' Add input to node. '''
            if (currNodeNum in nodeInputs):
                nodeInputs[currNodeNum].add(currVal)
            else:
                nodeInputs[currNodeNum] = set([currVal])
            
            #print('(currNodeNum, inputVal) = ' + str((currNodeNum, currVal)))
            
            ''' If node has received all inputs, propagate values to next nodes. '''
            if (len(nodeInputs[currNodeNum]) == len(self.revGeneMap[currNodeNum])):
                
                outputVal = utils.nodeTransferFunc(sum(nodeInputs[currNodeNum]))
                
                #print('(currNodeNum, outputVal) = ' + str((currNodeNum, outputVal)))
                
                if (self.nodeGenes[self.nodeMap[currNodeNum]].nodeType == 'Out'):
                    ''' This is an output node. Due to how we initially populate output nodes, if this is nodeNum i, then it's the (i - Common.nInNodes)th output node. '''
                    outputValList[currNodeNum - Common.nInNodes] = outputVal
                    
                if (currNodeNum in self.geneMap): #TODO: if we add a null set to geneMap whenever we add a new node, we won't have to check if currNodeNum is a valid geneMap key
                    for nextNodeNum in self.geneMap[currNodeNum]:
                        #print('nextNodeNum ' + str(nextNodeNum))
                        q.append((nextNodeNum, outputVal*self.connGenes[self.connMap[(currNodeNum, nextNodeNum)]].weight))
            
        print('outputValList = ' + str(outputValList))    
        return outputValList
        
    ''' Measure distance to otherOrg as defined by Stanley pg.110 eq. 1. '''    
    def compatDist(self, otherOrg):
        ''' First count number of disjoint node genes, that is genes that could have conceivably matched between
            organisms but don't. For example, if one organism has genes 1 2 3 and 5, and the other has 1 2 4 5 and 6,
            genes 3 and 4 are disjoint since they are within the overlapping range of genes (as given by innovation number)
            but aren't shared. Gene 6 isn't shared, but it would count as an excess gene, since it's out of the range of what
            the other organism has available. Excess is just sort of a different flavor of disjoint.

            Since nodes are added to organisms in ascending order, just look at the last node to get the highest number.
            All organisms should at least have the common input nodes, so there isn't a problem trying to index into an
            empty list. '''
        minMaxNodeNum = min(self.nodeGenes[-1].nodeNum, otherOrg.nodeGenes[-1].nodeNum)
        print('minMaxNodeNum: ' + str(minMaxNodeNum))
        
        if (minMaxNodeNum == self.nodeGenes[-1].nodeNum):
            longNodeOrg = otherOrg
            print('longNode (o) len: ' + str(longNodeOrg.nodeGenes[-1].nodeNum) + ', shortNode len: ' + str(self.nodeGenes[-1].nodeNum))
        else:
            longNodeOrg = self
            print('longNode (s) len: ' + str(longNodeOrg.nodeGenes[-1].nodeNum) + ', shortNode len: ' + str(otherOrg.nodeGenes[-1].nodeNum))
            
        ''' The plan for finding disjoint nodes is to add all nodes <= minMaxNodeNum from one organism into a set. Then
            we'll go through the second organism for its nodes <= minMaxNodeNum and do the following:
                1) If the nodeNum is already in the set (from the first organism), remove it.
                2) Else, add the node to the set.
            At the end of this process, the set should contain all disjoint nodes. '''
        disjointSet = set()
        
        for node in self.nodeGenes:
            if (node.nodeNum > minMaxNodeNum):
                break
            else:
                disjointSet.add(node.nodeNum)
                
        for node in otherOrg.nodeGenes:
            if (node.nodeNum > minMaxNodeNum):
                break
            elif node.nodeNum not in disjointSet:
                disjointSet.add(node.nodeNum)
            else:
                disjointSet.remove(node.nodeNum)
                
        disjointNode = len(disjointSet)
        print('node disjointCount: ' + str(disjointNode))
        print('node disjointSet: ' + str(disjointSet))
        
        ''' To find excess genes, count from end of the longer gene until nodeNum <= minMaxNodeNum. '''
        excessNode = 0
        ind = len(longNodeOrg.nodeGenes) - 1
        while (longNodeOrg.nodeGenes[ind].nodeNum > minMaxNodeNum):
            excessNode = excessNode + 1
            ind = ind - 1
            if (ind <= 0):
                break
                
        print('node excessNode: ' + str(excessNode))
        
        ''' Next: do the same for connection genes, with one modification. When a matching gene is found
            and removed form the disjointSet, add the weight difference to a running total. This total will be
            used to calculate W hat in Eq. (1) of Stanley pg. 110. If one or both of the organisms have no
            connections (for example, if they're new), everything in the other organism is excess. '''
            
        excessConn = 0
        disjointConn = 0
        weightSum = 0
        numMatches = 0
           
        if ((len(self.connGenes) == 0) or (len(otherOrg.connGenes) == 0)):
            excessConn = max(len(self.connGenes), len(otherOrg.connGenes))
        else:
            minMaxConnNum = min(self.connGenes[-1].nodeNum, otherOrg.connGenes[-1].nodeNum)
            print('minMaxConnNum: ' + str(minMaxConnNum))
            
            if (minMaxConnNum == self.connGenes[-1].nodeNum):
                longConnOrg = otherOrg
                print('longConn (o) len: ' + str(longConnOrg.connGenes[-1].nodeNum) + ', shortConn len: ' + str(self.connGenes[-1].nodeNum))
            else:
                longConnOrg = self
                print('longConn (s) len: ' + str(longConnOrg.connGenes[-1].nodeNum) + ', shortConn len: ' + str(otherOrg.connGenes[-1].nodeNum))
                
            ''' The plan for finding disjoint connections is to add all connections <= minMaxConnNum from one organism into a set. Then
                we'll go through the second organism for its nodes <= minMaxConnNum and do the following:
                    1) If the nodeNum is already in the set (from the first organism), add difference in weight to running sum, then remove connection.
                    2) Else, add the connection to the set.
                At the end of this process, the set should contain all disjoint nodes. '''
            disjointSet = set()
            
            weightSum = 0.0 # Sum of weight mismatches.
            numMatches = 0  # Number of matching genes (even if the weights don't actually match)
            
            for conn in self.connGenes:
                if (conn.nodeNum > minMaxConnNum):
                    break
                else:
                    disjointSet.add(conn.nodeNum)
                    
            for conn in otherOrg.connGenes:
                if (conn.nodeNum > minMaxConnNum):
                    break
                elif conn.nodeNum not in disjointSet:
                    disjointSet.add(conn.nodeNum)
                else:
                    ''' Normally to find the corresponding index of the connection gene in self.connGenes, we could use connMap like so:
                        self.connGenes[self.connMap[conn.conn]]. However, in this case, conn could be for a disabled gene, which won't be
                        in connMap (connMap only tracks enabled genes), but rather in disConnMap. '''
                    if conn.conn in self.connMap:
                        connGene = self.connGenes[self.connMap[conn.conn]]
                    else:
                        connGene = self.connGenes[self.disConnMap[conn.conn]]
                        
                    weightSum = weightSum + abs(connGene.weight - conn.weight)
                    numMatches = numMatches + 1
                    disjointSet.remove(conn.nodeNum)
                    
            disjointConn = len(disjointSet)
            print('conn disjointCount: ' + str(disjointConn))
            print('conn disjointSet: ' + str(disjointSet))
            
            ''' To find excess genes, count from end of the longer gene until nodeNum <= minMaxConnNum. '''
            ind = len(longConnOrg.connGenes) - 1
            while (longConnOrg.connGenes[ind].nodeNum > minMaxConnNum):
                excessConn = excessConn + 1
                ind = ind - 1
                if (ind <= 0):
                    break
                
        print('conn excessConn: ' + str(excessConn))    
        print('weightSum: ' + str(weightSum))
        print('numMatches: ' + str(numMatches))
     
        maxGenomeSize = max(len(self.nodeGenes) + len(self.connGenes), len(otherOrg.nodeGenes) + len(otherOrg.connGenes))
        print('maxGenomeSize: ' + str(maxGenomeSize))
     
        ''' This is the actual Eq. (1) computing the compatibility distance. '''
        dist = (Common.coefC1*(excessNode + excessConn) + Common.coefC2*(disjointNode + disjointConn))/maxGenomeSize
        if numMatches > 0:
            dist = dist + Common.coefC3*weightSum/numMatches
                    
        print('compat dist: ' + str(dist))
        return dist
        
    ''' Compute the fitness for this organism. '''    
    def compFitness(self):
        self.fitness = fitnessModule.fitness(self)
        return self.fitness
        
    ''' Run organism mutation, which can happen whether or not an organism is formed via mating. '''
    def mutate(self):
        if (random.random() < Common.addNodeProb):
            self.addNode()
            
        if (random.random() < Common.addConnProb):
            self.addConn()
            
        if (random.random() < Common.weightMutateProbGenome):
            for conn in self.connGenes:
                if (random.random() < Common.weightMutateProb):
                    conn.weight = random.uniform(-1.0, 1.0)
    
    ''' Mate with another organism to produce an offspring. For matching genes between organisms, the
        offspring will inherit randomly from either parent. For any disjoint or excess genes, the offspring
        will inherit from the fitter parent. If fitnesses are equal, disjoint/excess genes are inherited
        with equal probability from each parent (equal probability per gene). '''            
    def mateWith(self, partner):
    
        ''' This is the offspring, which is the output/return value of this function. '''
        offspring = Organism()
    
        ''' Start with the matching genes. We find the matching and disjoint genes in a similar way as used in
            the compatDist method, which contains more notes on the code logic. '''
        disjointSet = set()
    
        ''' First we'll handle nodes, then connections. '''
    
        ''' Equal fitnesses: '''
        if (self.fitness == partner.fitness):
            minMaxNodeNum = min(self.nodeGenes[-1].nodeNum, partner.nodeGenes[-1].nodeNum) #indexing won't fail, since there is at least num_input + num_output nodes 
            
            for node in self.nodeGenes:
                if (node.nodeNum > minMaxNodeNum):
                    break
                else:
                    disjointSet.add(node.nodeNum)
                    
            for node in partner.nodeGenes:
                if (node.nodeNum > minMaxNodeNum):
                    break
                elif node.nodeNum not in disjointSet:
                    disjointSet.add(node.nodeNum)
                else:
                    ''' Randomly add one of the matching nodes to the offspring and remove it from the disjoint set. Since nodes don't actually have distinguishing features
                        other than the innovation number (which we just found to be matching between organisms), we can add a copy of either to the offspring. Make a copy
                        instead of just copying the reference because conceptually the offspring has its own version, even though the values are the same. '''
                    #disjointSet.remove(node.nodeNum) #No need to remove, since we don't actually use the remaining elements for anything.
                    offspring.addNode(node)
                             
            ''' For the remaining disjoint/excess nodes, we could add them now, but the might not do anything by themselves. Instead, they'll have a chance to get added
                when adding connection genes as part of the addConn method. '''
            disjointSet = set()
            
            ''' For connections, if one of the parents has no connections, we'll randomly choose connections from the other parent. If both parents have connections,
                for shared connections we'll randomly select which parent we inherit from for shared genes, and for disjoint genes, we'll randomly choose if we even pick
                up that gene. '''
            if len(self.connGenes) == 0:
                for conn in partner.connGenes:
                    if random.choice([True, False]):
                        offspring.addConn(conn)
            elif len(self.connGenes) == 0:
                for conn in self.connGenes:
                    if random.choice([True, False]):
                        offspring.addConn(conn)                        
            else:
                for conn in partner.connGenes:
                        disjointSet.add(conn.nodeNum)
                        
                for conn in self.connGenes:
                    if conn.nodeNum not in disjointSet:
                        ''' This is a disjoint/excess connection. Randomly decide if we want to inherit it or not. No need to add to disjointSet. '''
                        if random.choice([True, False]):
                            offspring.addConn(conn, self)
                    else:
                        ''' This connection gene is present in both parents. Randomly inherit it from either parent. '''
                        if random.choice([True, False]):
                            offspring.addConn(conn, self)
                        else:
                            if conn.conn in partner.connMap:
                                newConn = partner.connGenes[partner.connMap[conn.conn]]
                            else:
                                newConn = partner.connGenes[partner.disConnMap[conn.conn]]
                            
                            offspring.addConn(newConn, partner)       
                            
                ''' The remaining connections are disjoint connections from partner. Randomly choose if we want to inherit it. '''
                for conn in disjointSet:
                    if random.choice([True, False]):
                        offspring.addConn(conn, partner)
        
        else:
            ''' One parent is more fit than the other: '''
            if (self.fitness > partner.fitness):
                fitOrg = self
                weakOrg = partner
            else:
                fitOrg = partner
                weakOrg = self
            
            ''' We're supposed to randomly select from parents any matching nodes, and disjoint/excess nodes will come from the fitter parent. Since node genes
                don't have distinguishing features between organisms (other than node number, which makes them matching in the first place), we can just take
                all nodes from the fitter parent. Since we also take all disjoint/excess nodes from the fitter parent, this simplifies to just taking all of the
                fitter parent's node genes. Connection genes will need to actually select randomly since weights can differentiate otherwise matching genes. '''
            for node in fitOrg.nodeGenes:
                offspring.addNode(node)
                               
            for conn in weakOrg.connGenes:
                    disjointSet.add(conn.nodeNum)
                    
            for conn in fitOrg.connGenes:
                if conn.nodeNum not in disjointSet:
                    ''' This is a disjoint or excess connection in the fitter parent. Offspring inherits it. '''
                    offspring.addConn(conn, fitOrg)
                else:
                    ''' This connection gene is present in both parents. Randomly inherit it from either parent. '''
                    #disjointSet.remove(node.nodeNum) #No need to remove - we won't use the disjointSet for anything after this.
                    if random.choice([True, False]):
                        offspring.addConn(conn, fitOrg)
                    else:
                        if conn.conn in weakOrg.connMap:
                            weakConn = weakOrg.connGenes[weakOrg.connMap[conn.conn]]
                        else:
                            weakConn = weakOrg.connGenes[weakOrg.disConnMap[conn.conn]]
                        
                        offspring.addConn(weakConn, weakOrg)
     
        return offspring
    
    def __str__(self):
        retStr = ""
        for node in self.nodeGenes:
            retStr += str(node) + '\n'
        
        return retStr