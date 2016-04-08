''' Fitness evaluation function for prey in pred/prey chase.

    INPUT:
        org = organism under evaluation
                        
    OUTPUT:
        fitness, calculated as how many rounds the organism lasts IN THE ARENA THIS SUNDAY.
    
    1 bias input.
    
    8 danger inputs (top left, top mid, top right, left, right, bot left, bot mid, bot right), which are
    binary values: 0 means safe, 1 means danger (either the predator or the edge of the arena).
    
    4 outputs - (move up, move down, move left, move right). If two contradictory directions, those cancel
    out.
'''

import Common

class Arena:
    def __init__(self, dimX, dimY, predSpawnXY, preySpawnXY):
        self.dimX = dimX
        self.dimY = dimY
        
        ''' Ensure spawn points are valid. '''
        assert(predSpawnXY != preySpawnXY)
        assert(self.isHazard(predSpawnXY) == False)
        assert(self.isHazard(preySpawnXY) == False)
        
        self.predSpawnXY = predSpawnXY
        self.preySpawnXY = preySpawnXY
        
        
    ''' Returns True if the (x,y) location is a hazard. Currently only hazards are on the boundaries of the arena,
        but future arenas could have more exotic designs. '''    
    def isHazard(self, xyTuple):
        (x, y) = xyTuple
        if ((x < 0) or (y < 0) or (x >= self.dimX) or (y >= self.dimY)):
            return True
        return False

''' Predator class. It's pretty stupid, just move roughly in the direction of the prey. '''        
class Pred:
    def __init__(self, xyLoc):
        self.loc = xyLoc
    
    def update(self, game):
        ''' Move towards prey, assuming that doesn't put us in a hazard. '''
        dx = game.prey.loc[0] - self.loc[0]
        dy = game.prey.loc[1] - self.loc[1]
        
        if (abs(dx) > abs(dy)):
            newLoc = (self.loc[0] + int(dx/abs(dx)), self.loc[1])
        else:
            newLoc = (self.loc[0], self.loc[1] + int(dy/abs(dy)))
            
        if not game.arena.isHazard(newLoc):
            self.loc = newLoc
        

''' Prey class. Input is a bias and the 8 surrounding squares. Output is 4 direction decisions. '''
class Prey:
    def __init__(self, xyLoc, org):
        self.loc = xyLoc
        self.org = org
        
    def update(self, game):
        ''' Form the input vector - bias node, then top left, top center, top right, left, right, bot left, bot center, bot right
            danger status. '''
        input = [1] # Bias
        
        testLoc = (self.loc[0]-1,self.loc[1]+1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]+0,self.loc[1]+1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]+1,self.loc[1]+1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]-1,self.loc[1]+0)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]+1,self.loc[1]+0)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]-1,self.loc[1]-1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]+0,self.loc[1]-1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)

        testLoc = (self.loc[0]+1,self.loc[1]-1)
        if (game.arena.isHazard(testLoc) or (testLoc == game.pred.loc)):
            input.append(1)
        else:
            input.append(0)
 
        output = self.org.compOutput(input)
        
        ''' Force binary decisions by thresholding the output. '''
        for k in range(len(output)):
            if output[k] >= 0.5:
                output[k] = 1
            else:
                output[k] = 0
        
        ''' Movement is determined by the output vector - (move up, move down, move left, move right). '''
        ''' Up/Down. '''
        if (output[0] != output[1]):
            if (output[0]):
                self.loc = (self.loc[0], min(self.loc[1]+1, game.arena.dimY-1)) 
            else:
                self.loc = (self.loc[0], max(self.loc[1]-1, 0))

        ''' Left/Right. '''
        if (output[2] != output[3]):
            if (output[2]):
                self.loc = (max(self.loc[0]-1, 0), self.loc[1]) 
            else:
                self.loc = (min(self.loc[0]+1, game.arena.dimX-1), self.loc[1])
        
class Game:
    def __init__(self, org):
        predXY = (7,5)
        preyXY = (2,4)
        self.arena = Arena(10, 10, predXY, preyXY)
        self.pred = Pred(predXY)
        self.prey = Prey(preyXY, org)
        self.round = 0
        
    def isDone(self):
        return ((self.pred.loc == self.prey.loc) or (self.round > Common.maxFitness))
        
    ''' Run the simulation by successively updating the prey then the predator. After each round, check if
        the simulation is over (as indicated by the isDone() method). When done, return the number of 
        rounds the simulation lasted. '''    
    def run(self):
        while (self.isDone() == False):
            self.round += 1
            self.pred.update(self)
            self.prey.update(self)
            
        #print('Round ' + str(self.round) + ', Pred ' + str(self.pred.loc) + ', Prey ' + str(self.prey.loc))

        return self.round
    
def fitness(org, indvTestPrint = False):
    assert(Common.initOrgFile == 'initOrg_prey')
    
    testGame = Game(org)
    return testGame.run() + 1.0 # Ensure fitness is non-zero 
    