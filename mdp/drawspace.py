import numpy as np
from collections import namedtuple


class DrawSpace(object):

    def __init__(self,
                 theta_bins=15,
                 length_bins=9,
                 length_max=300,
                 theta_max=3 * np.pi,
                 delta_theta_bins=11,
                 delta_length_bins=3,
                 delta_length_max=5
                 ):

        # Dimensions
        self.theta_bins = theta_bins
        self.length_bins = length_bins

        self.length_max = length_max
        self.theta_max = theta_max

        self.delta_theta_bins = delta_theta_bins
        self.delta_length_bins = delta_length_bins

        self.delta_length_max = delta_length_max

        self.theta_offset = (self.theta_bins - 1) / 2

        # Demonstration
        self.record = False
        self.this_demonstration = []
        self.demonstrations = []

        # States and Actions
        self.theta_space = np.linspace(-1 * self.theta_max, self.theta_max, self.theta_bins)
        self.length_space = np.linspace(0, self.length_max, self.length_bins)

        self.delta_theta_space = np.linspace(-1 * np.pi, np.pi, self.delta_theta_bins)
        self.delta_length_space = np.linspace(0, self.delta_length_max, self.delta_length_bins)

        self.n_states = self.theta_bins * self.length_bins
        self.states = self.get_states()

        self.actions = self.get_actions()
        self.n_actions = len(self.actions)
        self.current_state = (0, 0)

        self.transition_mat = self.generate_transition_prob()

        self.Step = namedtuple('Step', 'cur_state action next_state')

    def get_info(self):
        print("State space size: " + str(self.n_states))
        print(self.states)

    def get_states(self):
        states = []
        for i in range(self.theta_bins):
            for j in range(self.length_bins):
                theta = self.theta_space[i]
                length = self.length_space[j]
                states.append((length, theta))
        return states

    def get_actions(self):
        actions = []
        for i in range(self.delta_theta_bins):
            for j in range(self.delta_length_bins):
                delta_theta = self.delta_theta_space[i]
                delta_length = self.delta_length_space[j]
                actions.append((delta_length, delta_theta))
        return actions

    # Get closest state index
    def get_state_index_from_floats(self, (length, theta)):
        min_val = 100.0
        for i in range(self.n_states):
            dist_l = abs(length - self.states[i][0])
            dist_t = abs(theta - self.states[i][1])
            dist = dist_l + dist_t
            if dist < min_val:
                min_val = dist
                idx = i
        return (idx)

    def find_state(self,(length, theta)):
        index = self.get_state_index_from_floats((length, theta))

        return self.states[index]

    def generate_transition_prob(self):
        n_states = self.n_states
        n_actions = self.n_actions
        l_actions = self.actions
        l_states = self.states

        P_a = np.zeros((n_states, n_states, n_actions))
        for s_initial in range(n_states):
            for s_final in range(n_states):
                for action in range(n_actions):
                    if l_states[s_final] == self.next_state(l_states[s_initial], l_actions[action]):
                        P_a[s_initial, s_final, action] = 1
        return P_a

    def next_state(self, state_0, action):
        next_length = action[0] + state_0[0]
        next_theta = action[1] + state_0[1]
        if next_length > self.length_max:
            next_length = state_0[0]
        if next_theta > self.theta_max or next_theta < -self.theta_max:
            next_theta = state_0[1]
        state_1 = self.find_state((next_length, next_theta))
        return state_1

    def get_state_index(self, state):
        return self.states.index(state)

    def get_action_index(self, action):
        return self.actions.index(action)

    def get_action(self, policy, state_0):
        state_0_idx = self.get_state_index(state_0)
        action_0_idx = int(policy[state_0_idx])
        action_0 = self.actions[action_0_idx]
        return action_0

