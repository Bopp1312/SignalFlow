import numpy as np
from collections import namedtuple
import sys


class PixelSpace(object):

    def __init__(self,
                 theta_bins=15,
                 length_bins=9,
                 length_max=500,
                 theta_max=3 * np.pi,
                 delta_theta_bins=11,
                 delta_length_bins=3,
                 delta_length_max=5
                 ):
        # Bins represents the number of discrete bins that the value will be represented
        # as in the respective space it relates to
        # For instance our system is deterministic and therefore can be described in discrete time via
        # Difference equations, the action space is comprised of the differences that can be applied to
        # to the state of the system at any point in time.

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

        # Define the named tuple STEP for compatibility with IRL algorithm
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
    def get_state_index_from_floats(self, state):
        """ Given a state described by floats
        find the closest state in the state space"""

        (length, theta) = state
        min_val = 10**6
        for i in range(self.n_states):
            dist_l = abs(length - self.states[i][0])
            dist_t = abs(theta - self.states[i][1])
            dist = dist_l + dist_t
            if dist < min_val:
                min_val = dist
                idx = i
        return idx

    # Get closest action index
    def get_action_index_from_floats(self, action):
        """ Given a action described in floats
        find the closest action in the action space"""

        (d_length, d_theta) = action
        min_val = 10**6
        for i in range(self.n_actions):
            dist_l = abs(d_length - self.actions[i][0])
            dist_t = abs(d_theta - self.actions[i][1])
            dist = dist_l + dist_t
            if dist < min_val:
                min_val = dist
                idx = i
        return idx

    def find_state(self, state):
        index = self.get_state_index_from_floats(state)

        return self.states[index]

    def generate_transition_prob(self):
        n_states = self.n_states
        n_actions = self.n_actions
        l_actions = self.actions
        l_states = self.states

        P_a = np.zeros((n_states, n_states, n_actions))
        for s_initial_id in range(n_states):
            for action_id in range(n_actions):
                for s_final_id in range(n_states):
                    state_0 = self.states[s_initial_id]
                    state_1 = self.states[s_final_id]
                    action = self.actions[action_id]
                    (next_state, next_id) = self.next_state(state_0, action)
                    if next_state == state_1:
                        P_a[s_initial_id, s_final_id, action_id] = 1.0

        # Need to determine how to generate transisiton matrix
        return P_a

    def next_state(self, state_0, action):
        next_length = action[0] + state_0[0]
        next_theta = action[1] + state_0[1]
        if next_length > self.length_max:
            next_length = state_0[0]
        if next_theta > self.theta_max or next_theta < -self.theta_max:
            next_theta = state_0[1]
        state_1 = self.find_state((next_length, next_theta))
        id = self.get_state_index_from_floats((next_length, next_theta))
        return (state_1, id)

    def get_state_index(self, state):
        return self.get_state_index_from_floats(state)

    def get_action_index(self, action):
        return self.actions.index(action)

    def get_action(self, policy, state_0):
        state_0_idx = self.get_state_index(state_0)
        action_0_idx = int(policy[state_0_idx])
        action_0 = self.actions[action_0_idx]
        return action_0

    def data_to_demonstration(self, data):
        # Process each demonstration
        demonstration = []
        for i in range(len(data)):
            episode = []
            for j in range(len(data[i])-1):
                event_0 = data[i][j]
                event_1 = data[i][j+1]
                f_state_0 = event_0[0]
                f_action_0 = event_0[1]
                f_state_1 = event_1[0]
                state_0_idx = self.get_state_index_from_floats(f_state_0)
                action_0_idx = self.get_action_index_from_floats(f_action_0)
                state_1_idx = self.get_state_index_from_floats(f_state_1)
                episode.append(self.Step(cur_state=state_0_idx, action=action_0_idx, next_state=state_1_idx))

            demonstration.append(episode)
        return demonstration

