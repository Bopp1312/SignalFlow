from mdp.interspace import InterSpace
from maxent_irl import *

def main():
    object = InterSpace()
    object.get_info()
    #object.random_walk(10)
    object.states

    object.square()
    traj = object.demonstrations
    print(traj)
    feat_map = np.eye(object.n_states)
    mat = object.transition_mat
    gamma = 0.9
    iterations = 2
    learning_rate = 0.5
    rewards = maxent_irl(feat_map, mat, gamma, traj, learning_rate, iterations)
    print(rewards)
    values, policy = value_iteration.value_iteration(mat, rewards, gamma, error=0.01, deterministic=True)
    print(policy)
    print(np.shape(policy))
    object.walk(policy,10,(3,0))


if __name__ == '__main__':
    main()