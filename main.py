from mdp.drawspace import DrawSpace

def main():
    object = DrawSpace()
    object.get_info()

    print(object.actions)
    print(object.states)

    # Lets say you want to find the state index corresponding to a
    floating_state = (30.2, 1.625)
    id = object.get_state_index_from_floats(floating_state)
    state = object.states[id]
    print(state)
    print(id)

if __name__ == '__main__':
    main()