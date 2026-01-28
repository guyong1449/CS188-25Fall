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

    initialState = problem.getStartState()
    from util import Stack
    s = Stack()
    s.push((initialState, []))
    visit = {initialState: True}
    while not s.isEmpty():
        currentState, actions = s.pop()
        visit[currentState] = True # after pop mark it as traversed
        if(problem.isGoalState(currentState)):
            return actions
        
        for nextStep in problem.getSuccessors(currentState):
            nextState, nextAction, nextStepCost = nextStep
            if nextState in visit:
                continue
            
            # print(currentState, "->", nextState)
            s.push((nextState, actions + [nextAction]))
    
    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    initialState = problem.getStartState()
    from util import Queue
    q = Queue()
    q.push((initialState, []))
    visit = {initialState: True}
    while not q.isEmpty():
        currentState, actions = q.pop()
        if(problem.isGoalState(currentState)):
            return actions
        
        for nextStep in problem.getSuccessors(currentState):
            nextState, nextAction, nextStepCost = nextStep
            if nextState in visit:
                continue
            visit[nextState] = True
            q.push((nextState, actions + [nextAction]))


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # def print_heap(h):
    #     print("Current heap (list order):")
    #     for entry in h.heap:
    #         print(entry)
    #     print("-" * 40)

    initialState = problem.getStartState()
    from util import PriorityQueue
    h = PriorityQueue()
    h.push((initialState, [], 0), 0)
    visit = set()

    while not h.isEmpty():
        currentState, actions, cost = h.pop()
        if currentState in visit:
            continue
        visit.add(currentState)

        if(problem.isGoalState(currentState)):
            return actions
        
        for nextStep in problem.getSuccessors(currentState):
            nextState, nextAction, nextStepCost = nextStep
            # print(currentState, "->", nextState, " : ", cost, "->", cost + nextStepCost)

            if nextState not in visit:
                h.update((nextState, actions + [nextAction], cost + nextStepCost), cost + nextStepCost)
            else:
                continue

            # print_heap(h)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # def print_heap(h):
    #     print("Current heap (list order):")
    #     for entry in h.heap:
    #         print(entry)
    #     print("-" * 40)

    initialState = problem.getStartState()
    from util import PriorityQueue
    h = PriorityQueue()
    h.push((initialState, [], 0), 0)
    visit = set()

    while not h.isEmpty():
        currentState, actions, cost = h.pop()
        if currentState in visit:
            continue
        visit.add(currentState)

        if(problem.isGoalState(currentState)):
            return actions
        
        for nextStep in problem.getSuccessors(currentState):
            nextState, nextAction, nextStepCost = nextStep
            new_cost = cost + nextStepCost
            new_heuristic = heuristic(nextState, problem) + new_cost
            # print(currentState, "->", nextState, " : ", cost, "->", new_cost)

            if nextState not in visit:
                h.update((nextState, actions + [nextAction], new_cost), new_heuristic)
            else:
                continue

            # print_heap(h)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
