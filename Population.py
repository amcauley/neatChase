''' Organize all organisms in the population into species. Contains methods for
    forming and updating species. '''

import Common    
import Species    
    
class Population:
    def __init__(self, orgs=None):
        if orgs is None:
            self.orgs = set()
        else:    
            self.orgs = orgs
        
        ''' By default, constructor won't split the population into species. Call the speciate
            method explicitly if needed. '''
        self.species = set()

        ''' Threshold compatibility distance that determines if an organism can be added to this species. '''
        self.compatThresh = Common.compatThresh
    
    ''' Add an organism to the population. '''
    def addOrg(self, newOrg):
        self.orgs.add(newOrg)
    
    ''' Sort organisms from the population into species. Create new species as needed. '''
    def speciate(self):
        ''' We'll iterate through all the organisms, and for each one, we'll iterate through each existing
            species. If we find a matching species for the organism (determined by the compatibility distance
            with the species's representative), add the organism to that species. If no match is found, form a
            new species.
            
            Before we start, clear all the existing organism assignments from each species (but leave the representative
            intact). After all new assignments are complete, delete any species that don't have any organisms assigned
            to it - that species is dead. '''
            
        ''' Clear old organism assignments. '''   
        for spec in self.species:
            spec.clearOrgs()
            
        ''' New assignments. '''
        for org in self.orgs:
            foundSpec = False
            for spec in self.species:
                dist = org.compatDist(spec.representative)
                if dist <= self.compatThresh:
                    spec.addOrg(org)
                    foundSpec = True
                    break
            if not foundSpec:
                self.species.add(Species.Species({org}))
                
        ''' Delete any dead (empty) species, and assign new representative to keep it up to date. '''
        for spec in self.species:
            if spec.isEmpty():
                self.species.remove(spec)
            else:
                spec.updateRep()
                    
        
            