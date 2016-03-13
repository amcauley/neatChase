import Common
import Genes
import Organism
import Population

''' TODO:
         - (3/12/16) Add mutation/breeding algorithms
         - (3/12/16) Add population/species class testing to testEnv.py
'''         

''' This is global to help debugging - we can access pop from the interpreter after running runProg. '''
pop = Population.Population()

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
    
    for n in range(Common.popSize):
        ''' Create new organism, then assign i/o nodes to it'''
        org = Organism.Organism()
        org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object.
        org.nodeMap = dict(Common.ioNodeMap)
        org.revGeneMap = dict(Common.revMapInit)
        org.addConn()
        pop.addOrg(org)
             
    ''' Launch program here '''
    pop.speciate() # Since everything is the same at this point, everything will be grouped into a single species.
    
if __name__ == "__main__":
    runProg()
    
    