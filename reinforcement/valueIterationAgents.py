# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            states = self.mdp.getStates()
            # d = self.values # reference, not copy
            d = util.Counter()  # new dictionary
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                if len(actions) == 0:
                    maxVal = 0 
                else:
                    maxVal = -float('inf')
                    for action in actions:
                        Q = self.computeQValueFromValues(state, action)
                        # print("State:", state)
                        # print("Action:", action)
                        # print("Q:", Q)
                        if Q > maxVal:
                            maxVal = Q
                d[state] = maxVal
            self.values = d

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        total = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # dd not add for 2 times, or use "else"
            # if self.mdp.isTerminal(nextState):
            #     total += prob * (self.discount * self.getValue(nextState))
            total += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return total
    
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        bestAction = None
        if len(actions) == 0:
            return bestAction
        maxVal = -float('inf')
        for action in actions:
            Q = self.computeQValueFromValues(state, action)
            if Q > maxVal:
                maxVal = Q
                bestAction = action
        return bestAction
                            

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        from util import PriorityQueue
        
        predecessors = {}
        heap = PriorityQueue()
        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue
            for a in self.mdp.getPossibleActions(s):    
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(s, a):
                    if nextState in predecessors:
                        predecessors[nextState].add(s)
                    else:
                        predecessors[nextState] = {s}
        
        for state, preds in predecessors.items():
            print(f"preedecessors of state {state}: {preds}")
        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue
            diff = abs(self.values[s] - self.getQValue(s, self.getAction(s)))
            heap.update(s, - diff)
        

        for i in range(self.iterations):
            if heap.isEmpty():
                # print(f"迭代 {i+1}: 堆为空，提前终止 / Iteration {i+1}: Heap is empty, stopping early.")
                break
            
            s = heap.pop()
            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                if actions:
                    self.values[s] = max([self.getQValue(s, a) for a in actions])
                
            # if i < 5:
            #     print(f"--- 迭代 {i+1} / Iteration {i+1} ---")
            #     print(f"弹出状态 / Popped state: {s}")
            #     print(f"新值 / New value V({s}): {self.values[s]:.4f}")

            for p in predecessors.get(s, set()):
                if self.mdp.isTerminal(p): continue
                
                p_actions = self.mdp.getPossibleActions(p)
                max_q = max([self.getQValue(p, a) for a in p_actions]) if p_actions else 0
                diff = abs(self.values[p] - max_q)
                
                if diff > self.theta:
                    heap.update(p, -diff)
                    # if i < 5:
                    #     print(f"  更新前驱 / Updated predecessor: {p}, diff: {diff:.4f}")
                    



