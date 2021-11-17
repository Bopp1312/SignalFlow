from mdp.interspace import InterSpace
from maxent_irl import *
from data.data_extraction import getting_data
from mdp.drawspace import DrawSpace

def main():
    drawSpace = DrawSpace()
    drawSpace.get_info()

    data_input = getting_data()
    letter_a = data_input['a']
    demonstrations = drawSpace.data_to_demonstration(letter_a)

    # A demonstration of some trajectories
    trajectory = demonstrations
    feat_map = np.eye(drawSpace.n_states)
    mat = drawSpace.transition_mat
    exit()
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