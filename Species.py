''' A species is a set of organisms that are similar to each other as measured
    by Stanley pg. 110 Eq.(1), which is based on its compatDist from the species
    representative. '''
   
import Common   
import random    
import copy    
    
class Species:
    def __init__(self, orgs): 
        self.uid = random.randint(0, 2**31-1)   
        self.orgs = orgs
        
        ''' Current representative of the species - new candidate organisms for the species are
            compared against this one, which is randomly chosen from members of the previous generation
            of the species. For initialization, choose a random member from orgs. Or just pick the first one. '''  
        self.representative = random.sample(orgs,1)[0]
        
        ''' Sum of adjusted fitness for this species - Eq. (2) of Stanley pg. 110. '''
        self.adjFitSum = 0.0
        
        ''' Fittest organism in this species. '''
        self.fittestOrg = None
        
    ''' Add an organism to the species. '''
    def addOrg(self, newOrg):
        self.orgs.add(newOrg)   
        
    ''' Clear all organisms (but keep representative intact). '''    
    def clearOrgs(self):
        self.orgs.clear()
        
    ''' Check if the species is dead (empty). '''    
    def isEmpty(self):
        return (len(self.orgs) == 0)
        
    ''' Choose a new representative for this species. '''
    def updateRep(self):
        self.representative = random.sample(self.orgs,1)[0]
        
    ''' Compute the adjusted fitness sum - Eq. (2) of Stanley pg. 110. This is the sum of all fitnesses of this
        species's organisms, divided by the number of organisms in the species. This value will determine how many
        offspring this species is awarded. '''
    def adjFitComp(self):
        fitSum = 0.0
        numOrgs = len(self.orgs)
        
        if numOrgs == 0:
            self.adjFitSum = 0.0         
        else:
            for org in self.orgs:
                fitSum = fitSum + org.compFitness()
            self.adjFitSum = fitSum/numOrgs
            
        return self.adjFitSum
        
    ''' Create the next generation. Grant is now many organisms this species gets for the new generation. openSlots
        will track how many remaining organisms can fit in the next generation. '''  
    def nextGen(self, grant):
        openSlots = grant
        
        newPop = set()
        
        if ((openSlots >= Common.propFittestUnmodThresh) and (len(self.orgs) > 0)):
            ''' Find the current fittest and propagate to the next generation. '''
            openSlots = openSlots-1
            
            curFittest = random.sample(self.orgs,1)[0]            
            
            for org in self.orgs:
                if org.fitness > curFittest.fitness:
                    curFittest = org
            newPop.add(curFittest)
            
        ''' Handle portion of new generation formed from mutations without crossover. '''
        nSelfMutate = int(grant*Common.selfMutateRatio)
        while ((openSlots > 0) and (nSelfMutate > 0)):
            #print('nSelfMutate ' + str(nSelfMutate) + ' openSlots ' + str(openSlots) + ', newPop: ' + str(newPop))         
            mutOrg = random.sample(self.orgs,1)[0].clone()            
            mutOrg.mutate()          
            newPop.add(mutOrg)
            openSlots = openSlots-1
            nSelfMutate = nSelfMutate-1
            
        #print('newPop: ' + str(newPop))    
 
        ''' Offspring formed by mating two random organisms from the previous generation. Even if there is only 1 organism
            in the species, it can mate with itself. '''
        while (openSlots > 0):
            ''' Call sample twice instead of a single sample of 2 organisms in case there's only 1 org in the species. '''
            parent1 = random.sample(self.orgs,1)[0]          
            parent2 = random.sample(self.orgs,1)[0]

            newOrg = parent1.mateWith(parent2)
            newPop.add(newOrg)
            openSlots = openSlots-1          
        
        ''' Update the fittest organism for the new generation. '''    
        if (len(newPop) > 0):
            curFittest = random.sample(self.orgs,1)[0]            
            
            for org in self.orgs:
                if org.fitness > curFittest.fitness:
                    self.fittestOrg = org
                    
        ''' Delete old species population, replace with new one. Global population will update later after all species have
            undergone the nextGen routine. '''        
        self.orgs = newPop
            
            
    ''' Implement less than, which will allow us to call .sort() on an array of species. '''        
    def __lt__(self, other):   
        return self.adjFitSum < other.adjFitSum