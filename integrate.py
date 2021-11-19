from maxent_irl import *
from mdp.drawspace import DrawSpace
import json

def main():

    # Grab the json file that contains all the demonstrations for letter_a
    # To save data to json file it must be in a dictionary object
    with open("data/dict_a.json") as f:
        data = f.read()
    js = json.loads(data)
    letter_a = js['a']

    # Instantiate the MDP object
    # During initialization certain MDP objects are generated such as transition probability
    drawspace = DrawSpace()
    drawspace.get_info()

    # Generate transition probabilities
    mat = drawspace.generate_transition_prob()
    print(mat.shape)

    # Generate demonstrations based on data
    trajectory = drawspace.data_to_demonstration(letter_a)
    print(trajectory)

    # Create basic feature map
    feat_map = np.eye(drawspace.n_states)

    # Hyperparameters
    gamma = 0.75
    iterations = 20
    learning_rate = 0.5

    # Calculate reward function
    rewards = maxent_irl(feat_map, mat, gamma, trajectory, learning_rate, iterations)
    print(rewards)

    # Calculate Policy
    values, policy = value_iteration.value_iteration(mat, rewards, gamma, error=0.01, deterministic=True)

    # Each cell in the policy corresponds to an action indicated by the id
    print(policy)

    # You can see that the policy is a array the size of the state space
    print(np.shape(policy))

    dict_policy = {"policy": list(policy)}
    jsob = json.dumps(dict_policy)
    file = open("data/dict_policy.json", "w")
    file.write(jsob)
    file.close()


if __name__ == '__main__':
    main()