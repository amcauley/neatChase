import Common
import Genes
import Organism

''' TODO:
         - Implement adjusted fitness measure (Stanley pg. 110) - should maybe implement a
           population class to keep track of which species organisms belong to. This class could
           maybe hold the adjusted fitness method.
         - The population and species classes mentioned above are a work in progress
'''         

def runProg():
    ''' Form common I/O nodes that will be used in all organisms.
        NOTE! Don't change order of populating ioNodes in input, then output, then any middle nodes,
        since other sections of code assume this ordering, ex. compOutput method in Organism.py. '''
    Common.ioNodes = []    
    for n in range(Common.nInNodes):
        newGene = Genes.NodeGene('In')
        Common.ioNodeMap[newGene.nodeNum] = len(Common.ioNodes)
        Common.ioNodes.append(newGene)
        Common.revMapInit[newGene.nodeNum] = set([-1])
    for n in range(Common.nOutNodes):
        newGene = Genes.NodeGene('Out')
        Common.ioNodeMap[newGene.nodeNum] = len(Common.ioNodes)
        Common.ioNodes.append(newGene)    
    
    population = []
    for n in range(Common.popSize):
        ''' Create new organism, then assign i/o nodes to it'''
        org = Organism.Organism()
        org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object
        org.nodeMap = dict(Common.ioNodeMap)
        org.revGeneMap = dict(Common.revMapInit)
        population.append(org)
             
    ''' Launch program here '''
    
if __name__ == "__main__":
    runProg()
    
    