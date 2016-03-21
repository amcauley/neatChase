''' A species is a set of organisms that are similar to each other as measured
    by Stanley pg. 110 Eq.(1), which is based on its compatDist from the species
    representative. '''
   
import random    
    
class Species:
    def __init__(self, orgs): 

        self.orgs = orgs
        
        ''' Current representative of the species - new candidate organisms for the species are
            compared against this one, which is randomly chosen from members of the previous generation
            of the species. For initialization, choose a random member from orgs. Or just pick the first one. '''
        self.representative = random.sample(orgs,1)[0]
        
        ''' Sum of adjusted fitness for this species - Eq. (2) of Stanley pg. 110. '''
        self.adjFitSum = 0.0
        
    ''' Add an organism to the species. '''
    def addOrg(self, newOrg):
        self.orgs.add(newOrg)   
        
    ''' Clear all organisms (but keep representative intact). '''    
    def clearOrgs(self):
        self.orgs.clear
        
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
            
            