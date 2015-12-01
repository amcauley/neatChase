''' Set up a test environment for some interactive testing. Run this script from within Python's cmd line.
    Ex) 1. 'C:\Python44\python.exe', 2. 'from testEnv import *' '''
import Common
import Genes
import Organism

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
o = Organism.Organism()
o.nodeGenes = list(Common.ioNodes)
o.nodeMap = dict(Common.ioNodeMap)
o.nodeMap[n4.nodeNum] = len(o.nodeGenes)
o.nodeGenes.append(n4)
o.connMap[(n0.nodeNum, n4.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c0)
o.connMap[(n4.nodeNum, n3.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c1)
o.connMap[(n0.nodeNum, n3.nodeNum)] = len(o.connGenes) #update connMap when adding new connection
o.connGenes.append(c2)

''' Update geneMap and revGeneMap. '''
o.revGeneMap[n0.nodeNum] = set([-1])
o.revGeneMap[n1.nodeNum] = set([-1])
o.revGeneMap[n2.nodeNum] = set([-1])
o.geneMap[n0.nodeNum] = set([n3.nodeNum, n4.nodeNum])
o.revGeneMap[n3.nodeNum] = set([n0.nodeNum])
o.revGeneMap[n4.nodeNum] = set([n0.nodeNum])
o.geneMap[n4.nodeNum] = set([n3.nodeNum])
o.revGeneMap[n3.nodeNum].add(n4.nodeNum)

''' Add a loop by adding connections n4 -> n3 -> n0 to the geneMap. Not actually creating connection genes
    for this test. '''
#o.geneMap[n4.nodeNum] = set([n3.nodeNum])
#o.geneMap[n3.nodeNum] = set([n0.nodeNum])