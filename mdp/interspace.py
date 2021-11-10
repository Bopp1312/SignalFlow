import numpy as np

class InterSpace(object):

    def __init__(self):
        print("test")
        x_bins = 30
        y_bins = 30

        self.x_axis = x_bins
        self.y_axis = y_bins

        self.height = y_bins / 2
        self.width = x_bins / 2

        self.n_states = self.height * self.width

        self.states = self.get_states()
        self.actions = [(0, 0), (0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.n_actions = len(self.actions)
        self.current_state = (0, 0)

    def get_info(self):
        print("State space size: " + str(self.n_states))
        print(self.states)

    def get_states(self):
        states = []
        for i in range(self.x_axis):
            for j in range(self.y_axis):
                states.append((i, j))
        return states

    def step(self, action):
        state_t = self.current_state
        next_x = action[0] + state_t[0]
        next_y = action[1] + state_t[1]
        if next_x > self.width or next_x < -self.width:
            next_x = state_t[0]
        if next_y > self.height or next_y < -self.height:
            next_y = state_t[1]

        state_next = (next_x, next_y)
        print("State: " + str(state_next))
        self.current_state = state_next
        return state_next

    def random_walk(self,iterations):
        for i in range(iterations):
            # pick a next action
            idx = np.random.randint(self.n_actions)
            print(idx)
            print("Action: " + str(self.actions[idx]))
            self.curret_state = self.step(self.actions[idx])
            print("State: " + str(self.current_state))

    def square(self):
        self.current_state = (0,10)
        while self.current_state != (10, 10):
            self.step((1, 0))

        while self.current_state != (10, -10):
            self.step((0, -1))

        while self.current_state != (-10, -10):
            self.step((-1, 0))

        while self.current_state != (-10, 10):
            self.step((0, 1))

        while self.current_state != (0, 10):
            self.step((1, 0))
