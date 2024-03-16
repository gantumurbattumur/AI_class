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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print ("successorGameState: ", successorGameState)
        "*** YOUR CODE HERE ***"
       

        

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

class MinimaxAgent(MultiAgentSearchAgent):
    """Your expectimax agent (question 2)"""
    def getAction(self, gameState):
        """
        Returns the best action for Pacman using the minimax algorithm with
        self.depth and self.evaluationFunction.

        Helper functions:
        gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
            Returns the next game state after an agent takes an action

        gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def minimax(gameState, depth, agentIndex):
            # If the game is over or the maximum depth is reached, return the evaluation score
            if gameState.isWin() or gameState.isLose() or depth == self.depth: return self.evaluationFunction(gameState)
            
            state = gameState.getLegalActions(agentIndex)
            numAgents = gameState.getNumAgents()

            # Initialize the max and min scores of (values)
            # Eventually changed over min or max
            maxValue = -100000
            miniValue = 100000

            for action in state:
                successor = gameState.generateSuccessor(agentIndex, action)

                # If it's Pacman's turn 
                if agentIndex == 0:
                    score = minimax(successor, depth, 1)
                    maxValue = max(maxValue, score)
                else:
                    if agentIndex == numAgents - 1:
                        # If the depth is reached
                        score = minimax(successor, depth + 1, 0)
                    else:
                        score = minimax(successor, depth, agentIndex + 1)
                    miniValue = min(miniValue, score)

            if agentIndex == 0:
                return maxValue
            else:
                return miniValue

        # Just some small number that will be checked minimax
        v = -100000
        
        pacmanOption = gameState.getLegalActions(0)
        for action in pacmanOption:
            successor = gameState.generateSuccessor(0, action)
            # First position of the game starting
            score = minimax(successor, 0, 1) 
            if score > v:
                v = score
                bestAction = action

        return bestAction        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def alphaBeta(gameState, depth, agentIndex, a, b):
            
            # If the game is over or the maximum depth is reached, return the evaluation score
            if gameState.isWin() or gameState.isLose() or depth == self.depth: return self.evaluationFunction(gameState)

            state = gameState.getLegalActions(agentIndex)
            numAgents = gameState.getNumAgents()

            # Initialize the max and min scores of (values)
            # Eventually changed over min or max
            maxValue = -100000
            miniValue = 100000

            for action in state:
                successor = gameState.generateSuccessor(agentIndex, action)

                # If it's Pacman's turn 
                if agentIndex == 0:
                    maxValue = max(maxValue, alphaBeta(successor, depth, 1, a, b))
                    if maxValue >= b: return maxValue
                    a = max(maxValue, a)
                else:
                    if agentIndex == numAgents - 1:
                        # If the depth is reached
                        score = alphaBeta(successor, depth + 1, 0, a, b)
                    else:
                        score = alphaBeta(successor, depth, agentIndex + 1, a, b)
                    miniValue = min(miniValue, score)
                    if miniValue <= a: return miniValue
                    b = min(miniValue, b)

            if agentIndex == 0:
                return maxValue
            else:
                return miniValue

        # Just some small number that will be checked alphaBeta
        a = float('-inf')
        b = float('inf')
        pacmanOption = gameState.getLegalActions(0)
        for action in pacmanOption:
            successor = gameState.generateSuccessor(0, action)
            # First position of the game starting
            score = alphaBeta(successor, 0, 1, a,b) 
            if score > a:
                a = score
                bestAction = action

        return bestAction      
        
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
        # Re-using the base code structure from the minimax function
        def expmax(gameState, depth, agentIndex):
            # If the game is over or the maximum depth is reached, return the evaluation score
            if gameState.isWin() or gameState.isLose() or depth == self.depth: return self.evaluationFunction(gameState)

            state = gameState.getLegalActions(agentIndex)
            numAgents = gameState.getNumAgents()

            # Initialize the max and min scores of (values)
            # Eventually changed over min or max
            maxValue = -100000
            expValue = 0

            #totalSuccessors = []
            for action in state:
                successor = gameState.generateSuccessor(agentIndex, action)
                # If it's Pacman's turn 
                if agentIndex == 0:
                    score = expmax(successor, depth, 1)
                    maxValue = max(maxValue, score)
                else:
                    if agentIndex == numAgents - 1:
                        # If the depth is reached
                        score = expmax(successor, depth + 1, 0) 
                    else:
                        score = expmax(successor, depth, agentIndex + 1) 
                    expValue += score / len(state)

            if agentIndex == 0:
                return maxValue
            else:
                return expValue  

        # Just some small number that will be checked minimax
        v = -100000
        
        pacmanOption = gameState.getLegalActions(0)
        for action in pacmanOption:
            successor = gameState.generateSuccessor(0, action)
            # First position of the game starting
            score = expmax(successor, 0, 1) 
            if score > v:
                v = score
                bestAction = action

        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

