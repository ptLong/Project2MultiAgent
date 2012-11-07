# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
#jackreading
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def distanceTo(foodList, pacmanPos):
  dist = [manhattanDistance(pacmanPos, foodxy) for foodxy in foodList]
  dist.sort()
  if len(dist) > 0:
      return dist
  else:
      return [0]
INF = 1000000000000
MINUS_INF = -100000000
class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.lastMove = []
    self.lastMove.append(Directions.STOP)
    self.lastMove.append(Directions.STOP)
    self.lastMove.append(Directions.STOP)


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]


          

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPacmanPos = successorGameState.getPacmanPosition()
    
    #a grid[x][y] return T if [x][y] has food F otherwise
    newFood = successorGameState.getFood()
    #number of food left
    newFoodCount = newFood.count()
    #return a list of (x, y) that currently has food on it
    newFoodList = newFood.asList()
    #return a list (x,y) of capsules
    newCapsules = successorGameState.getCapsules()    
    capsulesLeft =len(newCapsules) + 1
    newGhostStates = successorGameState.getGhostStates()
    newGhostPossitions = [s.getPosition() for s in newGhostStates]
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #check if next pos for ghost.. if there is ghost then never go that way
    if action == Directions.STOP:
        currentUtility = successorGameState.getScore() - 888
    else:
        currentUtility = 8*successorGameState.getScore()  
        
    currentUtility -= 1.0*distanceTo(newFoodList, newPacmanPos)[0]
    #currentUtility += 5.0/newFoodCount

    currentUtility += 88888.8/capsulesLeft

    if capsulesLeft >2:
        currentUtility -= 100.0*distanceTo(newCapsules, newPacmanPos)[0]
    #currentUtility += 10.0/distanceTo(newCapsules, newPacmanPos)[0]
    for ghostPos in newGhostPossitions:
        if manhattanDistance(newPacmanPos, ghostPos) <2:
            currentUtility = -1000000

    return currentUtility


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)
    self.lastMove = [Directions.STOP, Directions.STOP, Directions.STOP ]

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    numOfGhost = gameState.getNumAgents() - 1
    #pacmanLegalActions = gameState.getLegalActions(0)
    #pacmanLegalActions.remove(Directions.STOP)
    #nextPacmanStates = [gameState.generateSuccessor(0, action) for action in pacmanLegalActions]
    def getBestActionGhost(numGhost, evalFn, gameState, depth):
        if numGhost == 1:
            ghostLegalActions = gameState.getLegalActions(numGhost)
            v = INF
            for action in ghostLegalActions:
                successor = gameState.generateSuccessor(numGhost, action)
                if depth == 1:
                    value = evalFn(successor)
                else:
                    #check successor if paman alive
                    #if he's alive then call to get back value with depth-1
                    if len(successor.getLegalActions(0))!=0:
                        pAction, value = getBestActionPacman(depth - 1, evalFn, successor)
                    else:        #if he's dead then
                        value = -INF 
                v = min(v, value)
            return v
        else:
            ghostLegalActions = gameState.getLegalActions(numGhost)
            v = INF
            for action in ghostLegalActions:
                successor = gameState.generateSuccessor(numGhost, action)
                value = getBestActionGhost(numGhost -1, evalFn, successor, depth)
                v = min(v, value)
            return v
                
            
    def getBestActionPacman(depth, evalFn, gameState):
        pacmanLegalActions = gameState.getLegalActions(0)
        #pacmanLegalActions.remove(Directions.STOP)
        #print gameState
        v = -INF
        #print v
        bestPacmanAction = pacmanLegalActions[0]
        for action in pacmanLegalActions:
            successor = gameState.generateSuccessor(0, action)
            value = getBestActionGhost(numOfGhost, evalFn, successor, depth)
            if v < value:
                v = value
                bestPacmanAction = action
        #print v
        #raw_input("---")
        return (bestPacmanAction, v)
    
    
    returnPacmanAction, v = getBestActionPacman(self.depth, self.evaluationFunction, gameState)
    #raw_input("---")
    return returnPacmanAction
    
    
      
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    numOfGhost = gameState.getNumAgents() - 1
    """
    Max node will check beta if value >= beta then return value  (No need to check more)
    Min node will check alpha: if value <= alpha then return value (no need to check more
    """
    def getBestActionGhost(numGhost, evalFn, gameState, depth, alpha, beta):
        if numGhost == 1:
            ghostLegalActions = gameState.getLegalActions(numGhost)
            v = INF
            for action in ghostLegalActions:
                successor = gameState.generateSuccessor(numGhost, action)
                if depth == 1:
                    value = evalFn(successor)
                else:
                    #check successor if paman alive
                    #if he's alive then call to get back value with depth-1
                    if len(successor.getLegalActions(0))!=0:
                        value = getBestActionPacman(depth - 1, evalFn, successor, alpha, beta)[1]
                    else:        #if he's dead then
                        value = -INF 
                v = min(v, value)
                if v<= alpha:
                    return v
                beta = min(beta, v)
            return v
        else:
            ghostLegalActions = gameState.getLegalActions(numGhost)
            v = INF
            for action in ghostLegalActions:
                successor = gameState.generateSuccessor(numGhost, action)
                value = getBestActionGhost(numGhost -1, evalFn, successor, depth, alpha, beta)
                v = min(v, value)
                if v<= alpha:
                    return v
                beta = min(beta, v)
            return v
                
            
    def getBestActionPacman(depth, evalFn, gameState, alpha, beta):
        pacmanLegalActions = gameState.getLegalActions(0)
        v = -INF
        bestPacmanAction = pacmanLegalActions[0]
        for action in pacmanLegalActions:
            successor = gameState.generateSuccessor(0, action)
            value = getBestActionGhost(numOfGhost, evalFn, successor, depth, alpha, beta)
            if v < value:
                v = value
                bestPacmanAction = action
            if v >= beta:
                return (bestPacmanAction, v)
            alpha = max(alpha, v)
        return (bestPacmanAction, v)
    
    
    returnPacmanAction, v = getBestActionPacman(self.depth, self.evaluationFunction, gameState, -INF, INF)
    #raw_input("---")
    return returnPacmanAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    
    numOfGhost = gameState.getNumAgents() - 1 
    def getBestActionGhost(numGhost, evalFn, gameState, depth):
        if numGhost == 1:
            if gameState.isWin():
                return INF
            elif gameState.isLose():
                return -INF
            else:
                ghostLegalActions = gameState.getLegalActions(numGhost)
                v = 0
                for action in ghostLegalActions:
                    successor = gameState.generateSuccessor(numGhost, action)
                    if depth == 1:
                        value = evalFn(successor)
                    else:
                        pAction, value = getBestActionPacman(depth - 1, evalFn, successor) 
                    v += value
                return (v/len(ghostLegalActions))
        else:
            if gameState.isWin():
                return INF
            elif gameState.isLose():
                return -INF
            else:
                ghostLegalActions = gameState.getLegalActions(numGhost)
                v = 0
                for action in ghostLegalActions:
                    successor = gameState.generateSuccessor(numGhost, action)
                    value = getBestActionGhost(numGhost -1, evalFn, successor, depth)
                    v += value
                
                return (v/len(ghostLegalActions))
            
    def getBestActionPacman(depth, evalFn, gameState):
        if gameState.isLose():
            return (Directions.STOP, -INF)
        elif gameState.isWin():
            return (Directions.STOP, INF)
        else:
            successors = [(gameState.generateSuccessor(0, action), action) for action in gameState.getLegalActions(0)]
            values = []
            for successor, action in successors:
                if successor.isWin():
                    values.append((INF, action)) #return this is the best action with max value
                elif successor.isLose():
                    values.append((-INF, action))  #skip this action; or may return this action with -INF
                else:
                    value = getBestActionGhost(numOfGhost, evalFn, successor, depth)
                    values.append((value, action))
            bestValue = max(values)
            bestIndices = [index for index in range(len(values)) if values[index][0] == bestValue[0]]
            
            if self.evaluationFunction == betterEvaluationFunction:
                chosenIndex = random.choice(bestIndices) #Pick randomly among the best for Q5
            else:
                chosenIndex = bestIndices[0]  #Pick the 1st one for Q4
    
            v, bestPacmanAction = values[chosenIndex]
            return (bestPacmanAction, v)
        
    returnPacmanAction, v = getBestActionPacman(self.depth, self.evaluationFunction, gameState)
    #raw_input("---")
    #####print "----------",returnPacmanAction, v
    return returnPacmanAction

    



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
    
      DESCRIPTION: 
      
          currentUtility = 8.0*currentGameState.getScore()  
          --> gameScore is important. It encourage Pacman to eat scared ghost, avoid ghost...
          
          currentUtility -= 188.0*foodCount   
          --> emphasize on the number of food left
          
          currentUtility -= 1.0*distanceToFoods[0]
          --> if next moves do not eat any food then pacman should go to the nearest food.

          currentUtility += 88888.8/capsulesLeft
          --> should eat capsule if there's a capsule near

            if capsulesLeft >2:
                currentUtility -= 100.0*distanceToCapsules[0]
            --> encourage pacman to go to the nearest capsule
    """
    "*** YOUR CODE HERE ***"

    #a grid[x][y] return T if [x][y] has food F otherwise
    foodGrid = currentGameState.getFood()
    #number of food left
    foodCount = foodGrid.count()
    #return a list of (x, y) that currently has food on it
    foodList = foodGrid.asList()
    if len(foodList) == 0:
        foodCount = -1
    
    #return a list (x,y) of capsules
    capsules = currentGameState.getCapsules()
    capsulesLeft = 1 + len(capsules)    
    
    ghostStates = currentGameState.getGhostStates()
    ghostPossitions = [s.getPosition() for s in ghostStates]
    scaredTimes = [gs.scaredTimer for gs in ghostStates]
    #newPacmanPos = successorGameState.getPacmanPosition()
    pacmanPos = currentGameState.getPacmanPosition()
    
    "*** YOUR CODE HERE ***"

    distanceToFoods = [d for d in distanceTo(foodList, pacmanPos)]
    distanceToCapsules = [d for d in distanceTo(capsules, pacmanPos)]

    currentUtility = 88.8*currentGameState.getScore()  
    currentUtility -= 8.8*foodCount   
    currentUtility -= 1.8*distanceToFoods[0]

    currentUtility += 88888.8/capsulesLeft

    if capsulesLeft ==3:
        currentUtility -= 1.8*distanceToCapsules[0]

    return currentUtility

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()





