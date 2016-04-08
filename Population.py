''' Organize all organisms in the population into species. Contains methods for
    forming and updating species. '''

import Common    
import Species    
import random
import utils    
    
''' Import the specified file for initializing organisms. '''
initOrgModule = __import__(Common.initOrgFile)    
    
class Population:
    def __init__(self, orgs=None):
        if orgs is None:
            self.orgs = set()
        else:    
            self.orgs = orgs
        
        ''' By default, constructor won't split the population into species. Call the speciate
            method explicitly if needed. '''
        self.species = set()

        ''' Threshold compatibility distance that determines if an organism can be added to this species, and starting step size. '''
        self.targetNumSpecs = Common.targetNumSpecs
        self.compatThresh = Common.compatThresh
        self.compatStep = Common.compatStep
        
        ''' Fittest organism. '''
        self.fittestOrg = None
    
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
  
        self.fittestOrg = random.sample(self.orgs,1)[0]
        
        ''' New assignments. Also update fittest organism. '''
        for org in self.orgs:
            if (org.fitness > self.fittestOrg.fitness):
                self.fittestOrg = org
            foundSpec = False

            for spec in self.species:
                dist = org.compatDist(spec.representative)              
                if dist <= self.compatThresh:
                    spec.addOrg(org)                   
                    foundSpec = True
                    break
            if not foundSpec:
                self.species.add(Species.Species({org}))
            
        ''' Delete any dead (empty) species, and assign new representative to keep it up to date.
            Temporarily store removal species in a separate set, otherwise we'll get errors about
            self.species changing size in the middle of iterating over it. '''
        removalSet = set()
        
        for spec in self.species:
            if spec.isEmpty():
                removalSet.add(spec)
            else:
                spec.updateRep()
                                                  
        for spec in removalSet:
            self.species.remove(spec)
                    
    ''' Progress population into the next generation. We'll sort species by adjusted fitness and then
        provide grants for the next generation. After each species progresses to the next generation, we'll
        go through each species and remove and dead ones. Finally, we'll delete the old population list and
        replace it with the new generation. '''
    def nextGen(self):               
        specList = list(self.species)        
        
        fitSum = 0.0
        for spec in specList:
            spec.adjFitComp()
            fitSum = fitSum + spec.adjFitSum                            
            
        ''' In the rare event that there are no fit organisms, we'll rebuild the entire population. '''      
        if (fitSum == 0.0):
            if Common.extraPrintEnPopInfo:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print('Rebuilding Population')
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            self.orgs = set()
            self.specs = set()
            for n in range(Common.popSize):
                ''' Create new organism, then assign i/o nodes to it'''
                org = initOrgModule.initOrg()
                self.addOrg(org)
                org.compFitness() #Comp fitness for this starting organism
            
            ''' Initial speciation. '''
            self.speciate() 
            return
            
        ''' Sorting is based on adjusted fitness (see Species __lt__ method). Ascending fitness order. '''
        specList.sort(reverse=True) # rely on spec __lt__ method, ascending order
        
        ''' Figure out how many grants will be given. If it's less than desired population size, give some
            extra grants to the fittest species. This could happen due to rounding. If we want more than are
            available, the weakest species will just have to suffer. '''
        grantSum = 0
        extraGrant = 0
        for spec in specList:
            thisGrant = int(Common.popSize*spec.adjFitSum/fitSum)
            grantSum = grantSum + thisGrant
        if grantSum < Common.popSize:
            extraGrant = Common.popSize - grantSum            
            
        numNewOrgs = 0
        for spec in specList:
            if (numNewOrgs >= Common.popSize):
                thisGrant = 0
            else:    
                thisGrant = int(Common.popSize*spec.adjFitSum/fitSum)
                if (numNewOrgs + thisGrant > Common.popSize):
                    thisGrant = Common.popSize - numNewOrgs
                elif ((extraGrant > 0) and (spec == specList[0])): #Award any extraGrant to the first (fittest) species
                    thisGrant = thisGrant + extraGrant
                numNewOrgs += thisGrant

            if Common.extraPrintEnPopInfo:
                print('Spec UID ' + str(spec.uid) + ', adjFitSum ' + str(spec.adjFitSum) + ', grant: ' + str(thisGrant))
                
            ''' Give the species its new grant. If the grant is zero, it will just clear the species's population. '''    
            spec.nextGen(thisGrant)                 
             
        ''' Iterate through updated species to form updated population. Deleting any dead/empty species will happen later
            during the speciate() method. Don't kill them off now since even if the species is empty, it might pick up some
            new orgs during speciate, or a non-empty one could lose its organisms during the update. '''
        newPop = set()
        for spec in specList:
            if (len(spec.orgs) != 0):
                newPop.update(spec.orgs) # Union of current orgs set and new orgs from this species
                
        self.orgs = newPop        
        
        ''' Now that we have the updated population, recompute species assignments. '''
        self.speciate() 

        ''' Adjust compatibility threshold to try to maintain target number of species. '''
        specLen = len(self.species)
        ''' Modifier: If last correction wasn't sufficient, increase adjustment amount. If we overshot, decrease amount. Remember
            that if specLen is larger than target, we want to *increase* compatStep to reduce the number of species. '''
        if (utils.isGTZ(self.compatStep) == utils.isGTZ(specLen - self.targetNumSpecs)):
            stepScale = 1.1
        else:
            stepScale = 0.8
            
        if (specLen < self.targetNumSpecs):
            ''' Bump down thresh unless we're at limit. '''
            if (self.compatThresh > 0):
                self.compatStep = -abs(self.compatStep)*stepScale
                self.compatThresh = max(self.compatThresh + self.compatStep, 0)
        elif (specLen > self.targetNumSpecs):
            ''' Too many species, increase compatThresh unless at limit. '''
            if (self.compatThresh < Common.maxCompatThresh):
                self.compatStep = abs(self.compatStep)*stepScale
                self.compatThresh = min(self.compatThresh + self.compatStep, Common.maxCompatThresh)
        #else:
            ''' We hit our target. Don't touch anything. '''
        
        if Common.extraPrintEnPopInfo:
            print('compatThresh ' + str(self.compatThresh) + ', compatStep ' + str(self.compatStep) + ', scale ' + str(stepScale))