# This script is used for testing the DeepCars environment by feeding random actions

import gym
import gym_deepcars
import time

env = gym.make('DeepCars-v0')

obs = env.reset()
# time.sleep(5)

for _ in range(10000):
    a = env.action_space.sample()  # Take a random action
    ImageData, Reward, done, __ = env.step(a)
    print(_)
    time.sleep(.2)

