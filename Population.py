''' Organize all organisms in the population into species. Contains methods for
    forming and updating species. '''

class Population:
    def __init__(self, orgs=None):
        if orgs is None:
            self.orgs = {}
        else:    
            self.orgs = orgs
        
        ''' By default, constructor won't split the population into species. Call the speciate
            method explicitly if needed. '''
        self.species = {}

        ''' Threshold compatibility distance that determines if an organism can be added to this species. '''
        self.compatThresh = Common.compatThresh
    
    ''' Add an organism to the population. '''
    def addOrg(self, newOrg):
        self.orgs.add(newOrg)
    
    ''' Sort organisms from the population into species. Create new species as needed. '''
    def speciate(self):
    