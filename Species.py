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