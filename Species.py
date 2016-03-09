''' A species is a set of organisms that are similar to each other as measured
    by Stanley pg. 110 Eq.(1), which is based on its compatDist from the species
    representative. '''

class Species:
    def __init__(self, orgs=None):
        if orgs is None:
            self.orgs = {}
        else:    
            self.orgs = orgs
        
        ''' Current representative of the species - new candidate organisms for the species are
            compared against this one, which is randomly chosen from members of the previous generation
            of the species. '''
        representative = None
        
    ''' Add an organism to the species. '''
    def addOrg(self, newOrg):
        self.orgs.add(newOrg)   
        