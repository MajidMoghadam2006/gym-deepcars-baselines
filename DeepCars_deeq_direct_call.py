# This script is used for training baselines in DeepCars environment

import  os
import gym
import gym_deepcars
from baselines import deepq
import numpy as np


def callback(lcl, _glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved

def main():
    # os.environ['SDL_AUDIODRIVER'] = "dummy"  # Create a AUDIO DRIVER to not produce the pygame sound
    # os.environ["SDL_VIDEODRIVER"] = "dummy"  # Create a dummy window to not show the pygame window
    env = gym.make('DeepCars-v0')
    # env = gym.make("ElevatorAction-v0")
    env.reset()
    model = deepq.learn(
        env,
        network='cnn_small',
        lr=1e-3,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=100,
        callback=callback,
        gamma=1.0,
        render=True
    )
    env.close()
    print("Saving model to deepcars_deepq_model.pkl")
    model.save("deepcars_deepq_model.pkl")


if __name__ == '__main__':
    main()
