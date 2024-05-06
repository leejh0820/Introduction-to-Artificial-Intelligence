# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # get start state
    # state: (x, y)
    # problem.getSuccesors(state): list [((x1, y1), 'Direction', cost), ((x2, y2), 'Dirction', cost) ....]
    # problem.isGoalState: True / False
    
    # start = goal?
    """
    cur_state = problem.getStartState()
    prev_states, directions = util.Stack(), util.Stack()
    directions.push(None)
    searched = []
    
    while not directions.isEmpty():
        
        if problem.isGoalState(cur_state):
            nevigate = []
            while not directions.isEmpty():
                nevigate.append(directions.pop())
            # import pdb; pdb.set_trace()
            return nevigate[-2::-1]
        searched.append(cur_state)
        
        next_nodes = problem.getSuccessors(cur_state)
        
        if all([bool(node[0] in searched) for node in next_nodes]):
            cur_state = prev_states.pop()
            directions.pop()
        else:
            for node in next_nodes:
                state, direction, cost = node

                if state in searched:
                    pass
                else:
                    directions.push(direction)
                    prev_states.push(cur_state)
                    cur_state = state
                    break
    return []
    """
    class Node:
        def __init__(self, state, direction=None, prev_node=None):
            self.state = state
            self.direction = direction
            self.prev_node = prev_node
    
    cur_node = Node(problem.getStartState())
    nodes = util.Stack()
    nodes.push(cur_node)
    # states.push(Node(cur_state, direction, prev_state))
    # prev_states, directions = util.Stack(), util.Stack()
    searched = []
    
    while not nodes.isEmpty():
        cur_node = nodes.pop()
        
        if problem.isGoalState(cur_node.state):
            directions = []
            # while cur_node.prev_node != None:
            while cur_node.direction != None:
            
                directions.append(cur_node.direction)
                cur_node = cur_node.prev_node
            # import pdb; pdb.set_trace()
            
            return directions[-1::-1]
        
        if cur_node.state not in searched:
            searched.append(cur_node.state)
            
            for node in problem.getSuccessors(cur_node.state):
                state, direction, cost = node
                nodes.push(Node(state, direction, cur_node))
        # else: 
            # directions.pop()        
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    class Node:
        def __init__(self, state, direction=None, prev_node=None):
            self.state = state
            self.direction = direction
            self.prev_node = prev_node
            
    cur_node = Node(problem.getStartState())
    nodes = util.Queue()
    nodes.push(cur_node)
    searched = []
    
    while not nodes.isEmpty():
        cur_node = nodes.pop()
        
        if problem.isGoalState(cur_node.state):
            directions = []
            # while cur_node.prev_node != None:
            # import pdb; pdb.set_trace()
            while cur_node.direction != None:
                directions.append(cur_node.direction)
                cur_node = cur_node.prev_node
            # print(directions[-1::-1])
            return directions[-1::-1]
        
        if cur_node.state not in searched:
            searched.append(cur_node.state)
            
            for node in problem.getSuccessors(cur_node.state):
                # state, direction, cost = node
                state, direction, cost = node
                # import pdb; pdb.set_trace()
                
                nodes.push(Node(state, direction, cur_node))

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    
    class Node:
        def __init__(self, state, direction=None, prev_node=None, cost=0):
            self.state = state
            self.direction = direction
            self.prev_node = prev_node
            self.cost = cost

    cur_node = Node(problem.getStartState())
    nodes = util.PriorityQueue()
    nodes.push(cur_node, 0)
    searched = []
    
    while not nodes.isEmpty():
        cur_node = nodes.pop()
        
        if problem.isGoalState(cur_node.state):
            directions = []
            # while cur_node.prev_node != None:
            while cur_node.direction != None:
                directions.append(cur_node.direction)
                cur_node = cur_node.prev_node
            return directions[-1::-1]
        
        if cur_node.state not in searched:
            searched.append(cur_node.state)
            
            for node in problem.getSuccessors(cur_node.state):
                state, direction, cost = node
                nodes.push(Node(state, direction, cur_node, cur_node.cost+cost), cur_node.cost+cost)
                
    return []

    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    
    class Node:
        def __init__(self, state, direction=None, prev_node=None, cost=0):
            self.state = state
            self.direction = direction
            self.prev_node = prev_node
            self.cost = cost

    cur_node = Node(problem.getStartState())
    nodes = util.PriorityQueue()
    nodes.push(cur_node, heuristic(cur_node.state, problem))
    searched = []
    
    while not nodes.isEmpty():
        cur_node = nodes.pop()
        
        if problem.isGoalState(cur_node.state):
            directions = []
            # while cur_node.prev_node != None:
            while cur_node.direction != None:
                directions.append(cur_node.direction)
                cur_node = cur_node.prev_node
            return directions[-1::-1]
        
        if cur_node.state not in searched:
            searched.append(cur_node.state)
            
            for node in problem.getSuccessors(cur_node.state):
                state, direction, cost = node
                nodes.push(Node(state, direction, cur_node, cur_node.cost+cost),
                           cur_node.cost + cost + heuristic(state, problem))# , state) #+cost)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
