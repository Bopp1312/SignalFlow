import numpy as np
from collections import namedtuple

class InterSpace(object):

    def __init__(self):

        # Dimensions
        self.x_bins = 9
        self.y_bins = 9
        self.y_offset = (self.y_bins - 1) / 2
        self.x_offset = (self.x_bins - 1) / 2

        # Demonstration
        self.record = False
        self.this_demonstration = []
        self.demonstrations = []

        # States and Actions
        self.n_states = self.y_bins * self.x_bins
        self.states = self.get_states()
        self.actions = [(0, 0), (0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.n_actions = len(self.actions)
        self.current_state = (0, 0)

        self.transition_mat = self.generate_transition_prob()

        self.Step = namedtuple('Step', 'cur_state action next_state')

    def get_info(self):
        print("State space size: " + str(self.n_states))
        print(self.states)

    def get_states(self):
        states = []
        for i in range(self.x_bins):
            for j in range(self.y_bins):
                x = i - self.x_offset
                y = j - self.y_offset
                states.append((x, y))
        return states

    def generate_transition_prob(self):
        n_states = self.n_states
        n_actions = self.n_actions
        l_actions = self.actions
        l_states = self.states

        P_a = np.zeros((n_states,n_states,n_actions))
        for s_initial in range(n_states):
            for s_final in range(n_states):
                for action in range(n_actions):
                    if l_states[s_final] == self.next_state(l_states[s_initial], l_actions[action]):
                        P_a[s_initial,s_final,action] = 1
        return P_a

    def next_state(self, state_0, action):
        next_x = action[0] + state_0[0]
        next_y = action[1] + state_0[1]
        if next_x > self.x_offset or next_x < -self.x_offset:
            next_x = state_0[0]
        if next_y > self.y_offset or next_y < -self.y_offset:
            next_y = state_0[1]
        state_1 = (next_x, next_y)
        if self.record:
            state_0_idx = self.get_state_index(state_0)
            state_1_idx = self.get_state_index(state_1)
            action_idx = self.get_action_index(action)
            self.this_demonstration.append(self.Step(cur_state=state_0_idx, action=action_idx, next_state=state_1_idx))
        return state_1

    def step_f(self, action):
        # Functional implementation
        state_0 = self.current_state
        state_1 = self.next_state(state_0, action)
        print("State: " + str(state_1))
        self.current_state = state_1
        return state_1

    def step_t(self, action):
        # Lookup table implementation
        state_0 = self.current_state
        statei_0 = self.get_state_index(state_0)
        actioni = self.get_action_index(action)
        state_1 = state_0
        for s in range(self.n_states):
            if self.transition_mat[statei_0,s,actioni] == 1.0:
                state_1 = self.states[s]
                break
        print("State:" + str(state_1))
        self.current_state = state_1
        return state_1

    def get_state_index(self, state):
        return self.states.index(state)

    def get_action_index(self, action):
        return self.actions.index(action)

    def random_walk(self,iterations):
        for i in range(iterations):
            # pick a next action
            idx = np.random.randint(self.n_actions)
            print(idx)
            print("Action: " + str(self.actions[idx]))
            self.step_f(self.actions[idx])
            print("State: " + str(self.current_state))

    def square(self):
        self.current_state = (0,3)
        self.record = True
        while self.current_state != (3, 3):
            self.step_f((1, 0))

        while self.current_state != (3, -3):
            self.step_f((0, -1))

        while self.current_state != (-3, -3):
            self.step_f((-1, 0))
        '''
        while self.current_state != (-10, 10):
            self.step_f((0, 1))

        while self.current_state != (0, 10):
            self.step_f((1, 0))
        '''
        self.record = False

        self.end_demonstration()
        print("Done")

    def get_action(self, policy, state_0):
        state_0_idx = self.get_state_index(state_0)
        action_0_idx = int(policy[state_0_idx])
        action_0 = self.actions[action_0_idx]
        return action_0

    def walk(self, policy, steps, state_0):
        self.current_state = state_0
        for i in range(steps):
            state = self.current_state
            action = self.get_action(policy, state)
            self.step_f(action)



    def end_demonstration(self):
        self.record = False
        latest_demo = self.this_demonstration
        self.this_demonstration = []
        self.demonstrations.append(latest_demo)


