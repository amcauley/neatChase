''' Set up a test environment for some interactive testing. Run this script from within Python's cmd line for interactive debugging.
    Ex) 1. 'C:\Python34\python.exe', 2. 'from testEnv import *' 
    To just run the script and print any output to console, just run 'C:\Python34\python.exe testEnv.py' directly. '''
import Common
import Genes
import Organism
import copy

''' Start by creating some nodes. '''
n0 = Genes.NodeGene('In')
n1 = Genes.NodeGene('In')
n2 = Genes.NodeGene('In')
n3 = Genes.NodeGene('Out')
n4 = Genes.NodeGene('Mid')


''' Update Common params since we're not using default for this simple testing. '''
Common.nInNodes = 3;
Common.nOutNodes = 1;
Common.ioNodeMap[n0.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n0)
Common.ioNodeMap[n1.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n1)
Common.ioNodeMap[n2.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n2)
Common.ioNodeMap[n3.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n3)

''' Connection Node from n0 -> n4. '''
c0 = Genes.ConnectionGene('Con')
c0.conn = (n0.nodeNum, n4.nodeNum)
c0.weight = 0.6

''' Connection from n4 -> n3. '''
c1 = Genes.ConnectionGene('Con')
c1.conn = (n4.nodeNum, n3.nodeNum)
c1.weight = 0.6

''' Connection from n0 -> n3. '''
c2 = Genes.ConnectionGene('Con')
c2.conn = (n0.nodeNum, n3.nodeNum)
c2.weight = 0.4

''' Put genes into an organism. '''
o0 = Organism.Organism()
o0.nodeGenes = list(Common.ioNodes)
o0.nodeMap = dict(Common.ioNodeMap)
o0.nodeMap[n4.nodeNum] = len(o0.nodeGenes)
o0.nodeGenes.append(n4)
o0.connMap[(n0.nodeNum, n4.nodeNum)] = len(o0.connGenes) #update connMap when adding new connection
o0.connGenes.append(c0)
o0.connMap[(n4.nodeNum, n3.nodeNum)] = len(o0.connGenes) #update connMap when adding new connection
o0.connGenes.append(c1)
o0.connMap[(n0.nodeNum, n3.nodeNum)] = len(o0.connGenes) #update connMap when adding new connection
o0.connGenes.append(c2)

''' Update geneMap and revGeneMap. '''
o0.revGeneMap[n0.nodeNum] = set([-1])
o0.revGeneMap[n1.nodeNum] = set([-1])
o0.revGeneMap[n2.nodeNum] = set([-1])
o0.geneMap[n0.nodeNum] = set([n3.nodeNum, n4.nodeNum])
o0.revGeneMap[n3.nodeNum] = set([n0.nodeNum])
o0.revGeneMap[n4.nodeNum] = set([n0.nodeNum])
o0.geneMap[n4.nodeNum] = set([n3.nodeNum])
o0.revGeneMap[n3.nodeNum].add(n4.nodeNum)

''' Add a loop by adding connections n4 -> n3 -> n0 to the geneMap. Not actually creating connection genes
    for this test. '''
#o0.geneMap[n4.nodeNum] = set([n3.nodeNum])
#o0.geneMap[n3.nodeNum] = set([n0.nodeNum])

''' First check that compatibility distance between an organism and itself is 0. '''
o0.compatDist(o0)

print("")

''' Second organism based on the first. Disable node 2, which happens to be an input. '''
o1 = copy.deepcopy(o0)
o1.connGenes[1].weight = 0.25   #modify c1 weight (in c0 this is .6)
o1.nodeGenes[2].disabled = True #disabled connection genes still contribute to weight mismatch
o1.connGenes[2].weight = .55    #in c0 this is .4. Total weight mismatch, including connGenes[1] mismatch, is .5
o1.addNode() #add 2 excess nodes (which creates 4 excess connections in the process)
o1.addNode()

''' Compatibility distance between o0 and o1. '''
o0.compatDist(o1)

print("")

''' Now add a new node to o0, which should change excess nodes to 1, disjoint nodes to 2,
    excess conn to 2, and disjoint conn to 4. '''
o0.addNode()
o0.compatDist(o1)