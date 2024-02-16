import collections, util, math, random
############################################################
# Problem 4.1.1

def computeQ(mdp, V, state, action):
    """
    Return Q(state, action) based on V(state).  Use the properties of the
    provided MDP to access the discount, transition probabilities, etc.
    In particular, MDP.succAndProbReward() will be useful (see util.py for
    documentation).  Note that |V| is a dictionary.  
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    #(newState, prob, reward)
    map = mdp.succAndProbReward(state, action)
    result=0
    for elem in mdp.succAndProbReward(state, action):
        result += elem[1]*(elem[2]+mdp.discount()*V[elem[0]])
    return result
    
    # END_YOUR_CODE

############################################################
# Problem 4.1.2

def policyEvaluation(mdp, V, pi, epsilon=0.001):
    """
    Return the value of the policy |pi| up to error tolerance |epsilon|.
    Initialize the computation with |V|.  Note that |V| and |pi| are
    dictionaries.
    """

    # BEGIN_YOUR_CODE (around 7 lines of code expected)
    V_new = {} 
    cont = True
    while cont:
        V_new = {} 
        cont = False
        for state in mdp.states:
            V_new[state] = computeQ(mdp,V,state,pi[state])
            if (abs(V_new[state]-V[state]))>epsilon:
                cont = True
        V = V_new
    return V

    
        
   
    
    # END_YOUR_CODE

############################################################
# Problem 4.1.3

def computeOptimalPolicy(mdp, V):
    """
    Return the optimal policy based on V(state).
    You might find it handy to call computeQ().  Note that |V| is a
    dictionary.
    """
    # BEGIN_YOUR_CODE (around 4 lines of code expected)
    pi = {}
    for state in mdp.states:
        max = 0
        for action in mdp.actions(state):
            new = computeQ(mdp,V,state,action)
            if(new>=max):
                max = new
                best_action = action
        pi[state] = best_action
    return pi

    # END_YOUR_CODE

############################################################
# Problem 4.1.4

class PolicyIteration(util.MDPAlgorithm):
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        V = {}
        for state in mdp.states:
            V[state]=0
        cont = True
        pi = computeOptimalPolicy(mdp, V)
        while cont:
            old_pi =pi
            pi = computeOptimalPolicy(mdp, V)
            old_V = V
            V = policyEvaluation(mdp, V, pi, epsilon)
            if(old_pi == pi and old_V == V):
                cont = False

        self.V = V
        self.pi = pi
        return
        # END_YOUR_CODE
        

############################################################
# Problem 4.1.5

class ValueIteration(util.MDPAlgorithm):
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        V = {}
        for state in mdp.states:
            V[state]=0
        cont = True
        while cont:
            pi = computeOptimalPolicy(mdp, V)
            V_new = {} 
            cont = False
            for state in mdp.states:
                V_new[state] = computeQ(mdp,V,state,pi[state])
                if (abs(V_new[state]-V[state]))>epsilon:
                    cont = True
            V = V_new
        self.V = V
        self.pi = pi
        return

############################################################
# Problem 4.1.6

# If you decide 1f is true, prove it in writeup.pdf and put "return None" for
# the code blocks below.  If you decide that 1f is false, construct a
# counterexample by filling out this class and returning an alpha value in
# counterexampleAlpha().
class CounterexampleMDP(util.MDP):
    def __init__(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def startState(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (around 1 line of code expected)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

def counterexampleAlpha():
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4.2.1

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 50 lines of code expected)
        successor = []
        if state[2] != None:
            sumCards = sum(state[2])
        if action == 'Take':
            if state[2]==None:
                return []
            
            if state[1] == None:
                i=0
                for card in self.cardValues:
                    result = []
                    new_state = []
                    new_state.append(state[0]+card)
                    new_state.append(None)
                    new_cards = state[2]
                    new_cards = list(new_cards)
                    new_cards[i] = new_cards[i]-1
                    if new_cards[i]>=0:
                        new_state.append(new_cards)
                        result.append(new_state)
                        result.append(state[2][i]/sumCards)
                        result.append(0)
                        successor.append(result)
                    i+=1
            else:
                result = []
                new_state = state
                new_state = []
                new_state.append(state[0]+self.cardValues[state[1]])
                new_state.append(None)
                new_cards = state[2]
                new_cards = list(new_cards)
                new_cards[state[1]] = new_cards[state[1]] - 1
                new_state.append(new_cards)
                result.append(new_state)
                result.append(1)
                result.append(0)
                successor.append(result)
                
            if sumCards == 1:
                for val in successor:
                    val[0][2] = None
                    if val[0][0]>self.threshold:
                        val[0][2] = None
                    else:
                        val[2] = val[0][0]

            for val in successor:
                if val[0][0]>self.threshold:
                    val[2]=0
                    val[0][2] = None
                

                

        if action == 'Peek':
            if state[1] != None or state[2] == None:
                return []
            i=0
            for card in self.cardValues:
                result = []
                new_state = []
                new_state.append(state[0])
                if state[2][i]>0:
                    new_state.append(i)
                new_state.append(state[2])
                result.append(new_state)
                result.append(state[2][i]/sumCards)
                result.append(-1*self.peekCost)
                successor.append(result)
                i+=1
        if action == 'Quit':
            if state[2] == None or sumCards == 0:
                return []
            result = []
            new_state = state
            new_state = list(new_state)
            new_state[2] = None
            result.append(new_state)
            result.append(1)
            result.append(new_state[0])
            successor.append(result)
        
        new_successors = []
        for val in successor:
            if val[0][2] != None:
                val[0][2] = tuple(val[0][2])
            val[0] = tuple(val[0])
            new_successors.append(tuple(val))
        
        return successor



            

    def discount(self):
        return 1

############################################################
# Problem 4.2.2

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    return BlackjackMDP(cardValues=[2, 3, 4, 10, 19], multiplicity=15, threshold=20, peekCost=1)

    # END_YOUR_CODE

