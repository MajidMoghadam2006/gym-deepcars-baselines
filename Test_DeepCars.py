# This script is used for testing the DeepCars environment by feeding random actions

import gym
import gym_deepcars

env = gym.make('DeepCars-v0')

obs = env.reset()
env.render()

for _ in range(50):
    a = env.action_space.sample()  # Take a random action
    ImageData, Reward, done, __ = env.step(a)
    # env.render()
    print(_)
