from mdp.drawspace import DrawSpace

def main():
    object = DrawSpace()
    object.get_info()
    object.states
    object.actions
    id = object.get_state_index_from_floats((30, 1.657))
    state = object.states[id]
    print(object.theta_space)
    print(state)
    print(id)



if __name__ == '__main__':
    main()