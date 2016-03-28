import Common
import Genes
import Organism
import Population
import random

''' TODO:
         - (3/20/16) Need to add a disable/enable method for organisms to dis/enable connections,
                     and then use this method to implement flipping disable state in offspring
                     (per Stanley, there's a chance state will change).
         - (3/23/16) Add new connection map to Organism that maps connection "nodeNum" to index
                     within connGenes array. Also rename connection "nodeNum", since it's not a node.         
         - (3/25/16) Random seed doesn't seem to be working - still seeing run-to-run variation. Why?
         - (3/27/16) Add phenotype initialization routine to implement figure 5(a) (Stanley pg. 113).
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
    
    ''' Seed the RNG. '''
    if Common.useFixedSeed:
        random.seed(Common.randSeed)
        print('RNG seed: ' + str(Common.randSeed))
    
    for n in range(Common.popSize):
        ''' Create new organism, then assign i/o nodes to it'''
        org = Organism.Organism()
        org.nodeGenes = list(Common.ioNodes) # Call list to make a new copy of ioNodes instead of pointing to the same underlying object.
        org.nodeMap = dict(Common.ioNodeMap)
        org.revGeneMap = dict(Common.revMapInit)
        org.addConn()
        pop.addOrg(org)
        
        org.compFitness()
             
    ''' Launch program here: '''
    
    ''' Initial speciation. '''
    pop.speciate() # Since everything is the same at this point, everything will be grouped into a single species.
    print('Gen 0')
    print('Max Fitness: ' + str(pop.fittestOrg.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
   
    ''' Run the simulation for the specified number of generations. '''
    for gen in range(Common.maxGens):
        print('Gen ' + str(gen) + ' -> Gen ' + str(gen+1))
        pop.nextGen()
        print('Max Fitness: ' + str(pop.fittestOrg.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
        
        ''' Sanity checks. '''
        assert(len(pop.orgs) == Common.popSize)
   
if __name__ == "__main__":
    runProg()
    
    