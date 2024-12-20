# MINIMAX ALGORITHM
import math
def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    if (curDepth == targetDepth):
        return scores[nodeIndex]
    if (maxTurn):
        return max(minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth))
    else:
        return min(minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth))
scores = [3, 5, 19, 9, 34, 5, 6, 23]
treeDepth = int(math.log(len(scores), 2))
print("The optimal value is : ", end="")
print(minimax(0, 0, True, scores, treeDepth))

""":::"""

# ALPHA BETA PRUNING
MAX, MIN = 1000, -1000
def minimax(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
    if depth == 3:
        return values[nodeInd ex]
    if maximizingPlayer:
        best = MIN
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = MAX
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
if __name__ == "__main__":
    values = [3, 8, 19, 16, 1, 2, 0, -1]
    print("The optimal value is :", minimax(0, 0, True, values, MIN, MAX))

# BAYESIAN NETWORK

!pip install pgmpy
import pgmpy.models
import pgmpy.factors.discrete

# Define the Bayesian Model
model = pgmpy.models.BayesianModel([('Burglary', 'Alarm'),
                                    ('Earthquake', 'Alarm'),
                                    ('Alarm', 'JohnCalls'),
                                    ('Alarm', 'MaryCalls')])

# Define the CPDs (Conditional Probability Distributions)
cpd_burglary = pgmpy.factors.discrete.TabularCPD('Burglary', 2, [[0.001], [0.999]])
cpd_earthquake = pgmpy.factors.discrete.TabularCPD('Earthquake', 2, [[0.002], [0.998]])
cpd_alarm = pgmpy.factors.discrete.TabularCPD('Alarm', 2, [[0.95, 0.94, 0.29, 0.001],
                                                           [0.05, 0.06, 0.71, 0.999]],
                                               evidence=['Burglary', 'Earthquake'],
                                               evidence_card=[2, 2])
cpd_john = pgmpy.factors.discrete.TabularCPD('JohnCalls', 2, [[0.90, 0.05],
                                                              [0.10, 0.95]],
                                              evidence=['Alarm'],
                                              evidence_card=[2])
cpd_mary = pgmpy.factors.discrete.TabularCPD('MaryCalls', 2, [[0.70, 0.01],
                                                              [0.30, 0.99]],
                                              evidence=['Alarm'],
                                              evidence_card=[2])

# Add the CPDs to the model
model.add_cpds(cpd_burglary, cpd_earthquake, cpd_alarm, cpd_john, cpd_mary)

# Check if the model is correctly defined
model.check_model()

# Print the probability distributions
print('Probability distribution, P(Burglary)')
print(cpd_burglary)
print()
print('Probability distribution, P(Earthquake)')
print(cpd_earthquake)
print()
print('Joint probability distribution, P(Alarm | Burglary, Earthquake)')
print(cpd_alarm)
print()
print('Joint probability distribution, P(JohnCalls | Alarm)')
print(cpd_john)
print()
print('Joint probability distribution, P(MaryCalls | Alarm)')
print(cpd_mary)
print()

# Hidden Markov Model
!pip install hmmlearn

import numpy as np
from hmmlearn import hmm

# Define the state space
states = ["Sunny", "Rainy"]
n_states = len(states)
print('Number of hidden states:', n_states)

# Define the observation space
observations = ["Dry", "Wet"]
n_observations = len(observations)
print('Number of observations:', n_observations)

# Define the initial state distribution
state_probability = np.array([0.6, 0.4])
print("State probability:", state_probability)

# Define the state transition probabilities
transition_probability = np.array([[0.7, 0.3], [0.3, 0.7]])
print("\nTransition probability:\n", transition_probability)

# Define the observation likelihoods
emission_probability = np.array([[0.9, 0.1], [0.2, 0.8]])
print("\nEmission probability:\n", emission_probability)

# Initialize the model
model = hmm.CategoricalHMM(n_components=n_states)
model.startprob_ = state_probability
model.transmat_ = transition_probability
model.emissionprob_ = emission_probability

# Define the sequence of observations
observations_sequence = np.array([0, 1, 0, 1, 0, 0]).reshape(-1, 1)

# Predict the most likely sequence of hidden states
hidden_states = model.predict(observations_sequence)
print("Most likely hidden states:", hidden_states)

# Compute the log probability and most likely hidden states using the Viterbi algorithm
log_probability, hidden_states = model.decode(observations_sequence, lengths=[len(observations_sequence)], algorithm='viterbi')

print('Log Probability:', log_probability)
print("Most likely hidden states:", hidden_states)

# MARKOV DECISION PROCESS
import numpy as np

class MDP:
    def __init__(self, states, actions, transition_prob, rewards, gamma):
        self.states = states
        self.actions = actions
        self.transition_prob = transition_prob  # P(s' | s, a)
        self.rewards = rewards  # R(s, a, s')
        self.gamma = gamma

    def value_iteration(self, epsilon=1e-6):
        V = np.zeros(len(self.states))
        while True:
            delta = 0
            for s in self.states:
                v = V[s]
                V[s] = max(
                    sum(
                        self.transition_prob[s][a].get(s_next, 0) *
                        (self.rewards[s][a].get(s_next, 0) + self.gamma * V[s_next])
                        for s_next in self.states
                    ) for a in self.actions
                )
                delta = max(delta, abs(v - V[s]))
            if delta < epsilon:
                break
        return V

    def policy_iteration(self):
        policy = np.zeros(len(self.states), dtype=int)
        V = np.zeros(len(self.states))

        def one_step_lookahead(s, V):
            A = np.zeros(len(self.actions))
            for a in self.actions:
                A[a] = sum(
                    self.transition_prob[s][a].get(s_next, 0) *
                    (self.rewards[s][a].get(s_next, 0) + self.gamma * V[s_next])
                    for s_next in self.states
                )
            return A

        while True:
            # Policy Evaluation
            while True:
                delta = 0
                for s in self.states:
                    v = V[s]
                    V[s] = sum(
                        self.transition_prob[s][policy[s]].get(s_next, 0) *
                        (self.rewards[s][policy[s]].get(s_next, 0) + self.gamma * V[s_next])
                        for s_next in self.states
                    )
                    delta = max(delta, abs(v - V[s]))
                if delta < 1e-6:
                    break

            # Policy Improvement
            policy_stable = True
            for s in self.states:
                old_action = policy[s]
                policy[s] = np.argmax(one_step_lookahead(s, V))
                if old_action != policy[s]:
                    policy_stable = False

            if policy_stable:
                return policy, V

# Example usage
states = [0, 1, 2]
actions = [0, 1]
transition_prob = {
    0: {
        0: {0: 0.8, 1: 0.2},
        1: {0: 0.1, 1: 0.9}
    },
    1: {
        0: {0: 0.7, 1: 0.0, 2: 0.3},
        1: {0: 0.4, 1: 0.0, 2: 0.6}
    },
    2: {
        0: {1: 0.5, 2: 0.5},
        1: {0: 0.6, 1: 0.4}
    }
}
rewards = {
    0: {0: {0: 5, 1: 10}, 1: {0: -1, 1: 2}},
    1: {0: {0: -1, 2: 1}, 1: {0: 1, 2: 3}},
    2: {0: {1: -2, 2: 0}, 1: {0: 0, 1: 1}}
}
gamma = 0.9

mdp = MDP(states, actions, transition_prob, rewards, gamma)

# Value Iteration
optimal_values = mdp.value_iteration()
print("Optimal Values from Value Iteration:", optimal_values)

# Policy Iteration
optimal_policy, optimal_values = mdp.policy_iteration()
print("Optimal Policy from Policy Iteration:", optimal_policy)
print("Optimal Values from Policy Iteration:", optimal_values)
