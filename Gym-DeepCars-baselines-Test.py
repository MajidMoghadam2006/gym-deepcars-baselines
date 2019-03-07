import gym
import gym_deepcars
from baselines import deepq

def callback(lcl, _glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved


def main():
    env = gym.make('DeepCars-v0')
    # env = gym.make("ElevatorAction-v0")
    env.reset()
    act = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=10,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback,
        load_path = '/deepcars_deepq_model',
        render=True
    )


if __name__ == '__main__':
    main()