# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        # newFood: bool grid
        # newScaredTimes: list of a number
        # newGhostStates: (x, y)
        # newCapsules: list of (x, y) tuples

        # print(newFood)
        # print(newScaredTimes)
        # print(newPos)
        # print(newGhostStates)
        newCapsules = successorGameState.getCapsules()

        width = newFood.width
        height = newFood.height
        foodNum = sum(1 for i in range(width) for j in range(height) if newFood[i][j])
        
        numGhosts = successorGameState.getNumAgents() - 1
        ghostDistances = []
        for i in range(1, numGhosts + 1):
            ghostPos = successorGameState.getGhostPosition(i)
            if ghostPos:
                ghostDistances.append(manhattanDistance(newPos, ghostPos))
        
        minGhostDist = min(ghostDistances) if ghostDistances else float('inf')
        
        
        if newCapsules:
            minCapsuleDist = min(manhattanDistance(newPos, cap) for cap in newCapsules)
        else:
            minCapsuleDist = float('inf')

        def minFoodDis(newFood, newPos):
            foodList = newFood.asList()
            if not foodList:
                return 0, 0
            
            dist = []
            totalDist = 0
            for food in foodList:
                d = manhattanDistance(newPos, food)
                dist.append(d)
                totalDist += d
            
            return min(dist), totalDist
    
        foodDis, totalFoodDist = minFoodDis(newFood, newPos)
        
        
        if foodNum < 5:
            res = -foodDis * 2 - foodNum * 8 
        else:
            res = -foodDis - foodNum * 8
        
        maxScaredTime = max(newScaredTimes) if newScaredTimes else 0
        
        ghost_penalty = 0
        if maxScaredTime == 0:  
            if minGhostDist < 1: 
                ghost_penalty -= 10000
            elif minGhostDist < 2: 
                ghost_penalty -= 200 
            elif minGhostDist < 3:
                ghost_penalty -= 50
        else:
            ghost_penalty -= 10 / minGhostDist
        
        if maxScaredTime == 0 and minCapsuleDist < float('inf'):
            res += 5 / (minCapsuleDist + 1)  
        
        return res + maxScaredTime + ghost_penalty + random.random() * 2 + successorGameState.getScore() 
        

def scoreEvaluationFunction(currentGameState: GameState):
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def value(gameState, depth, agentIdx):
            # print("depth: ", depth, " ", "agentIdx: ", agentIdx)
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIdx == 0:
                return max(value(gameState.generateSuccessor(agentIdx, action), depth, (agentIdx + 1) % agentNum) for action in gameState.getLegalActions(agentIdx))
            elif (agentIdx + 1) % agentNum == 0:
                return min(value(gameState.generateSuccessor(agentIdx, action), depth-1, (agentIdx + 1) % agentNum) for action in gameState.getLegalActions(agentIdx))
            else:
                return min(value(gameState.generateSuccessor(agentIdx, action), depth, (agentIdx + 1) % agentNum) for action in gameState.getLegalActions(agentIdx))
       
        agentNum = gameState.getNumAgents()
        depth = self.depth       
        agentIdx = self.index
        maxValue = float('-inf')
        minValue = float('inf')
        bestAction = None
        actions = gameState.getLegalActions(agentIdx)

        for _ in actions:
            successor = gameState.generateSuccessor(agentIdx, _)
            val = value(successor, depth, (agentIdx + 1) % agentNum)
            if val > maxValue and agentIdx == 0:
                maxValue = val
                bestAction = _
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def value(gameState, depth, agentIdx, alpha, beta):
            # print("depth: ", depth, " ", "agentIdx: ", agentIdx)
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIdx == 0:
                v = float('-inf')
                for action in gameState.getLegalActions(agentIdx):
                    val = value(gameState.generateSuccessor(agentIdx, action), depth, (agentIdx + 1) % agentNum, alpha, beta)
                    v = max(v, val)
                    if val > beta:
                        return val
                    alpha = max(alpha, val)
                
            elif (agentIdx + 1) % agentNum == 0:
                v = float('inf')
                for action in gameState.getLegalActions(agentIdx):
                    val = value(gameState.generateSuccessor(agentIdx, action), depth-1, (agentIdx + 1) % agentNum, alpha, beta)
                    v = min(v, val)
                    if val < alpha:
                        return val
                    beta = min(beta, val)
                
            else:
                v = float('inf')
                for action in gameState.getLegalActions(agentIdx):
                    val = value(gameState.generateSuccessor(agentIdx, action), depth, (agentIdx + 1) % agentNum, alpha, beta)
                    v = min(v, val)
                    if val < alpha:
                        return val
                    beta = min(beta, val)

            return v
                
       
        agentNum = gameState.getNumAgents()
        depth = self.depth       
        agentIdx = self.index
        maxValue = float('-inf')
        bestAction = None
        actions = gameState.getLegalActions(agentIdx)
        alpha = float('-inf')
        beta = float('inf')

        for _ in actions:
            successor = gameState.generateSuccessor(agentIdx, _)
            val = value(successor, depth, (agentIdx + 1) % agentNum, alpha, beta)
            if val > maxValue and agentIdx == 0:
                maxValue = val
                alpha = max(alpha, val)
                bestAction = _
        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
