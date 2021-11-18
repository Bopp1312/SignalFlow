from mdp.interspace import InterSpace
from maxent_irl import *
from mdp.drawspace import DrawSpace
import json

def main():

    with open("data/dict_a.json") as f:
        data = f.read()

    js = json.loads(data)
    letter_a = js['a']

    drawSpace = DrawSpace()
    drawSpace.get_info()

    # Generate transition probabilities
    mat = drawSpace.transition_mat
    print(mat.shape)

    # Generate demonstrations based on data
    demonstrations = drawSpace.data_to_demonstration(letter_a)

    # A demonstration of some trajectories
    trajectory = demonstrations
    feat_map = np.eye(drawSpace.n_states)

    # Hyperparameters
    gamma = 0.75
    iterations = 20
    learning_rate = 0.5
    rewards = maxent_irl(feat_map, mat, gamma, trajectory, learning_rate, iterations)
    print(rewards)

    values, policy = value_iteration.value_iteration(mat, rewards, gamma, error=0.01, deterministic=True)
    # Each cell in the policy corresponds to an action indicated by the id
    print(policy)
    # You can see that the policy is a array the size of the state space
    print(np.shape(policy))


if __name__ == '__main__':
    main()