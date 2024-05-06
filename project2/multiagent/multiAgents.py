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
        newFood = successorGameState.getFood() # -> newFood.asList()
        newGhostStates = successorGameState.getGhostStates() # list -> ghost.getPosition()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #############################
        # Evaluation: Steps, Number of Food, Distance to the Ghost
        # 1. avoid the ghost
        # 1-1. don't have to avoid scared ghost
        # 1-2. alert danger if scared time is small
        # 1-2. consider nearest ghost OR gives larger consideration to nearer ghost
        # 2. eat the food
        #############################
        # import pdb; pdb.set_trace()
        
        # ghost distance:
        near_ghost = 1
        for ghost in newGhostStates:
            dist = manhattanDistance(ghost.getPosition(), newPos)
            scared = ghost.scaredTimer
            
            if dist == 0 and scared == 0:
                near_ghost = -100000
            elif dist == 0 and scared != 0:
                near_ghost = min(10, near_ghost)
            elif dist != 0 and scared == 0:
                near_ghost = min(-100/dist, near_ghost)
            elif dist != 0 and scared != 0:
                near_ghost = min(dist/scared, near_ghost)
                
        near_food = 0
        for food in newFood.asList():
            dist = manhattanDistance(food, newPos)
            if dist == 0:
                near_food = 100
            else:
                near_food = max(10/dist, near_food)
        
        numFood = successorGameState.getNumFood()
        if numFood == 0:
            numFood = 0.00000000001
        
        score = near_ghost + near_food + 100000/numFood# min(dist_ghost) + max(dist_food)
        
        return score # successorGameState.getScore()

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
        def value(state, depth, agent):
            if depth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if agent == 0:
                return maxi(state, depth, agent)
            else:
                return mini(state, depth, agent)
            
        def maxi(state, depth, agent):
            V = float('-inf')
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = max(V, value(successor, depth, 1))
            return V
        
        def mini(state, depth, agent):
            V = float('inf')
            
            next_agent = (agent+1)%state.getNumAgents()
            next_depth = depth+1 if next_agent==0 else depth
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = min(V, value(successor, next_depth, next_agent))
            return V
        
        best_action = None
        V = float('-inf')
        
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            temp = value(successor, 0, 1)
            if temp > V:
                V = temp
                best_action = action
                
        return best_action
        
        
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def value(state, depth, agent, alpha, beta):
            if depth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if agent == 0:
                return maxi(state, depth, agent, alpha, beta)
            else:
                return mini(state, depth, agent, alpha, beta)
            
        def maxi(state, depth, agent, alpha, beta):
            V = float('-inf')
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = max(V, value(successor, depth, 1, alpha, beta))
                if V > beta:
                    return V
                alpha = max(alpha, V)
            return V
        
        def mini(state, depth, agent, alpha, beta):
            V = float('inf')
            
            next_agent = (agent+1)%state.getNumAgents()
            next_depth = depth+1 if next_agent==0 else depth
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = min(V, value(successor, next_depth, next_agent, alpha, beta))
                if V < alpha:
                    return V
                beta = min(beta, V)
            return V
        
        best_action = None
        V = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            temp = value(successor, 0, 1, alpha, beta)
            if temp > V:
                V = temp
                best_action = action
                alpha = temp
                
        return best_action
    
    
        # util.raiseNotDefined()

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
        
        def value(state, depth, agent):
            if depth==self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if agent == 0:
                return maxi(state, depth, agent)
            else:
                return mini(state, depth, agent)
            
        def maxi(state, depth, agent):
            V = float('-inf')
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = max(V, value(successor, depth, 1))
            return V
        
        def mini(state, depth, agent):
            V = 0
            
            next_agent = (agent+1)%state.getNumAgents()
            next_depth = depth+1 if next_agent==0 else depth
            
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                V = V + value(successor, next_depth, next_agent)
            return V
        
        best_action = None
        V = float('-inf')
        
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            temp = value(successor, 0, 1)
            if temp > V:
                V = temp
                best_action = action
                
        return best_action
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    - Overall code is similar to before. Change the code to hunt ghost when the state of ghost is scared.
    
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    near_ghost = 1
    for ghost in newGhostStates:
        dist = manhattanDistance(ghost.getPosition(), newPos)
        scared = ghost.scaredTimer
            
        if dist == 0 and scared == 0:
            near_ghost = -10000
        elif dist == 0 and scared > 0:
            near_ghost = max(1000, near_ghost)
        elif dist > 0 and scared == 0:
            near_ghost = min(-100/dist, near_ghost)
        elif dist > 0 and scared > 0:
            near_ghost = max((25*scared)/dist, near_ghost)
                
    near_food = 0
    for food in newFood.asList():
        dist = manhattanDistance(food, newPos)
        if dist == 0:
            near_food = 10
        else:
            near_food = max(10/dist, near_food)
        
    numFood = currentGameState.getNumFood()
    if numFood == 0:
        numFood = 0.0001
        
    score = near_ghost + near_food + 10000/numFood# min(dist_ghost) + max(dist_food)
        
    return score 
    
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
