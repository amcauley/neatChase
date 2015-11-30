''' Set up a test environment for some interactive testing. Run this script from within Python's cmd line.
    Ex) 1. 'C:\Python34\python.exe', 2. 'from testEnv import *' '''
import Common
import Genes
import Organism

''' Start by creating some nodes. '''
n0 = Genes.NodeGene('In')
n1 = Genes.NodeGene('Out')
n2 = Genes.NodeGene('Mid')

''' Update Common params since we're not using default for this simple testing. '''
Common.nInNodes = 1;
Common.nOutNodes = 1;
Common.ioNodeMap[n0.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n0)
Common.ioNodeMap[n1.nodeNum] = len(Common.ioNodes)
Common.ioNodes.append(n1)

''' Connection Node from n0 -> n2. '''
c0 = Genes.ConnectionGene('Con')
c0.conn = (n0.nodeNum, n2.nodeNum)
c0.weight = 0.6

''' Connection from n2 -> n1. '''
c1 = Genes.ConnectionGene('Con')
c1.conn = (n2.nodeNum, n1.nodeNum)
c1.weight = 0.6

''' Connection from n0 -> n1. '''
c2 = Genes.ConnectionGene('Con')
c2.conn = (n0.nodeNum, n1.nodeNum)
c2.weight = 4

''' Put genes into an organism. '''
o = Organism.Organism()
o.nodeGenes = list(Common.ioNodes)
o.nodeMap = dict(Common.ioNodeMap)
o.nodeMap[n2.nodeNum] = len(o.nodeGenes)
o.nodeGenes.append(n2)
o.connMap[(n0.nodeNum, n2.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c0)
o.connMap[(n2.nodeNum, n1.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c1)
o.connMap[(n0.nodeNum, n1.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c2)

''' Update geneMap. '''
o.geneMap[n0.nodeNum] = set([n1.nodeNum, n2.nodeNum])
o.geneMap[n2.nodeNum] = set([n1.nodeNum])

''' Add a loop by adding connections n2 -> n1 -> n0 to the geneMap. Not actually creating connection genes
    for this test. '''
#o.geneMap[n2.nodeNum] = set([n1.nodeNum])
#o.geneMap[n1.nodeNum] = set([n0.nodeNum])