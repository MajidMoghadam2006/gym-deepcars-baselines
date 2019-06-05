# This script is used for testing the DeepCars environment by feeding random actions

import gym
import gym_deepcars
import time
import numpy as np

env = gym.make('DeepCars-v0')

obs = env.reset()
# time.sleep(5)

for _ in range(1000):
    a = env.action_space.sample()  # Take a random action
    obs, Reward, done, __ = env.step(a)
    obs2 = env.observation_space.sample()
    print(obs, obs2, env.action_space.n, env.action_space.sample())
    env.render()
    time.sleep(.2)
    if done:
        env.reset()

