import Common
import Genes
import Organism

def runProg():
    ''' Form common I/O nodes that will be used in all organisms '''
    Common.ioNodes = []    
    for n in range(Common.nInNodes):
        newGene = Genes.NodeGene("In")
        Common.ioNodes.append(newGene.nodeNum : newGene)
    for n in range(Common.nOutNodes):
        newGene = Genes.NodeGene("Out")
        Common.ioNodes.append(newGene.nodeNum : newGene)    
    
    population = []
    for n in range(Common.popSize):
        ''' Create new organism, then assign i/o nodes to it'''
        org = Organism.Organism()
        org.nodeGenes = dict(Common.ioNodes) # Call dict to make a new copy of ioNodes instead of pointing to the same underlying object 
        population.append(org)
             
    ''' Launch program here '''
    
if __name__ == "__main__":
    runProg()
    
    