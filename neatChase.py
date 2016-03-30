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
                     within connGenes array (maybe). Also rename connection "nodeNum", since it's not a node.         
         - (3/25/16) Random seed doesn't seem to be working - still seeing run-to-run variation. Why?
                     May be related to: http://stackoverflow.com/questions/6614447/python-random-seed-not-working-with-genetic-programming-example-code
                     try using random.choice(sorted(...)) after modifying Organism __lt__ the compare based on a random ID we assign to organism at time
                     of creation (this will help prevent organisms with same fitness preventing a unique sorting order).
                     UPDATE (3/30) - Seem to have achieved deterministic results, but code is now very slow from sorting everything constantly. Maybe move to
                     using lists by default instead of sets, and only convert to sets as needed. Or, only enable deterministic code with a param for debugging,
                     leave disabled by default. Also clean up debug code.
         - (3/28/16) Add 'perfect' XOR organism to testEnv to check that it has top fitness. Also try adding it
                     to initialization seed to see if it survives (if it doesn't, then nextGen() has some issues).
'''
                     
''' Import the specified file for initializing organisms. '''
initOrgModule = __import__(Common.initOrgFile) 

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
        org = initOrgModule.initOrg()
        pop.addOrg(org)
        org.compFitness()
    
    ''' Initial speciation. '''
    pop.speciate() # Since everything is the same at this point, everything will be grouped into a single species.
    print('Gen 0')
    print('Max Fitness: ' + str(pop.fittestOrg.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
   
    fittestEver = pop.fittestOrg
   
    ''' Run the simulation for the specified number of generations. '''
    for gen in range(Common.maxGens):
        print('Gen ' + str(gen) + ' -> Gen ' + str(gen+1))

        pop.nextGen()
        thisGenFittest = pop.fittestOrg
        print('Max Fitness: ' + str(thisGenFittest.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
        
        if (thisGenFittest.fitness > fittestEver.fitness):
            fittestEver = thisGenFittest
        
        ''' Sanity checks. '''
        assert(len(pop.orgs) == Common.popSize)
   
    if True:
        print('____________End_Simulation____________')
        print('Top Nodes:')
        for node in fittestEver.nodeGenes:
            print(node)
        print('____________')
        print('Top Conns:')
        disConnCnt = 0
        for conn in fittestEver.connGenes:
            if (conn.disabled):
                disConnCnt += 1
            else:    
                print(conn)
        print('+ ' + str(disConnCnt) + ' disabled')        
        print('____________')
        print('Top Fitness: ' + str(fittestEver.fitness))
    
    if True: #Common.dbgEnRandCheckPrints:
        print('rand end: ' + str(random.random()))
    
if __name__ == "__main__":
    runProg()
    
    