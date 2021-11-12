from mdp.interspace import InterSpace
from maxent_irl import *

def main():
    object = InterSpace()
    object.get_info()
    object.states

    # A demonstration of some trajectories
    print("Walking in a square as a demonstration")
    object.square()
    traj = object.demonstrations
    feat_map = np.eye(object.n_states)
    mat = object.transition_mat

    # Hyperparameters
    gamma = 0.75
    iterations = 20
    learning_rate = 0.5
    rewards = maxent_irl(feat_map, mat, gamma, traj, learning_rate, iterations)
    print(rewards)

    values, policy = value_iteration.value_iteration(mat, rewards, gamma, error=0.01, deterministic=True)
    # Each cell in the policy corresponds to an action indicated by the id
    print(policy)
    # You can see that the policy is a array the size of the state space
    print(np.shape(policy))

    # Test out the trained policy to see what happens
    object.walk(policy,10,(0,0))

if __name__ == '__main__':
    main()