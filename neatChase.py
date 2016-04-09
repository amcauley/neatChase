import Common
import Genes
import Organism
import Population
import random

''' TODO:
         - (4/9/16)  Find a way to graphically represent the nodes/connections.
         - (3/31/16) Implement separate params for small vs. large species (mentioned in Stanley) (low prio).
         - (3/31/16) Interspecies mating (low prio)
         - (3/23/16) Add new connection map to Organism that maps connection "nodeNum" to index
                     within connGenes array (maybe). Also rename connection "nodeNum", since it's not a node (low prio).         
'''
                     
''' Import the specified file for initializing organisms. '''
initOrgModule = __import__(Common.initOrgFile) 


def runProg():
    if Common.basicPrintEn:
        print('====================Start_Simulation====================')
        
    pop = Population.Population()
        
    ''' Form common I/O nodes that will be used in all organisms.
        NOTE! Don't change order of populating ioNodes in input, then output, then any middle nodes,
        since other sections of code assume this ordering, ex. compOutput method in Organism.py.

        Can skip this initialization if these already exist, i.e. if we've already run runProg() before.
        Check this by seeing if Common.ioNodes has been populated already.
    '''
     
    initOrgModule.commonInit()
     
    if not Common.ioNodes:    
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
        org = initOrgModule.initOrg()
        pop.addOrg(org)
        org.compFitness() #Comp fitness for this starting organism
    
    ''' Initial speciation. '''
    pop.speciate()
    if Common.basicPrintEn:
        print('Gen 0')
        print('Max Fitness: ' + str(pop.fittestOrg.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
   
    fittestEver = pop.fittestOrg.clone()
   
    ''' Run the simulation for the specified number of generations. '''
    for gen in range(Common.maxGens):
        if Common.basicPrintEn:
            print('Gen ' + str(gen) + ' -> Gen ' + str(gen+1))

        pop.nextGen()
        thisGenFittest = pop.fittestOrg
        
        if Common.basicPrintEn:
            print('Max Fitness: ' + str(thisGenFittest.fitness) + ', Num Species: ' + str(len(pop.species)) + '\n')
        
        if (thisGenFittest.fitness > fittestEver.fitness):
            fittestEver = thisGenFittest.clone()
        
        ''' Sanity checks. '''
        assert(len(pop.orgs) == Common.popSize)
   
    if Common.basicPrintEn:
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
        fittestEver.compFitness(True)
        print('')
        print('Top Fitness: ' + str(fittestEver.fitness))
    
    return fittestEver.fitness
    
if __name__ == "__main__":
    Common.basicPrintEn = True
    runProg()
    
    