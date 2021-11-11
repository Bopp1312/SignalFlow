import numpy as np

class InterSpace(object):

    def __init__(self):


        self.x_bins = 21
        self.y_bins = 21

        self.y_offset = (self.y_bins - 1) / 2
        self.x_offset = (self.x_bins - 1) / 2

        self.n_states = self.y_bins * self.x_bins

        self.states = self.get_states()
        self.actions = [(0, 0), (0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.n_actions = len(self.actions)
        self.current_state = (0, 0)

        self.P_a = self.generate_transition_prob()

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
        nStates = self.n_states
        nActions = self.n_actions
        lActions = self.actions
        lStates = self.states

        P_a = np.zeros((nStates,nStates,nActions))
        for s_initial in range(nStates):
            for s_final in range(nStates):
                for action in range(nActions):
                    if lStates[s_final] == self.next_state(lStates[s_initial], lActions[action]):
                        P_a[s_initial,s_final,action] = 1
        return P_a

    def next_state(self,state_t,action_t):
        next_x = action_t[0] + state_t[0]
        next_y = action_t[1] + state_t[1]
        if next_x > self.x_offset or next_x < -self.x_offset:
           next_x = state_t[0]
        if next_y > self.y_offset or next_y < -self.y_offset:
            next_y = state_t[1]
        next_state = (next_x, next_y)
        return next_state

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
            if self.P_a[statei_0,s,actioni] == 1.0:
                state_1 = self.states[s]
                break
        print("State:" + str(state_1))
        self.current_state = state_1
        return state_1

    def get_state_index(self,state):
        return self.states.index(state)

    def get_action_index(self,action):
        return self.actions.index(action)

    def random_walk(self,iterations):
        for i in range(iterations):
            # pick a next action
            idx = np.random.randint(self.n_actions)
            print(idx)
            print("Action: " + str(self.actions[idx]))
            self.curret_state = self.step_f(self.actions[idx])
            print("State: " + str(self.current_state))

    def square(self):
        self.current_state = (0,10)
        while self.current_state != (10, 10):
            self.step_t((1, 0))

        while self.current_state != (10, -10):
            self.step_t((0, -1))

        while self.current_state != (-10, -10):
            self.step_t((-1, 0))

        while self.current_state != (-10, 10):
            self.step_t((0, 1))

        while self.current_state != (0, 10):
            self.step_t((1, 0))
        print("Done")
