import gym
import gym_deepcars
import numpy as np
from gym import error, spaces, utils

# env = gym.make('DeepCars-v0')
#
# obs = env.observation_space
#
# temp = obs.sample()
#
# print(obs.sample())
# print(np.shape(temp))

obs_space = spaces.MultiDiscrete(np.ones(5, dtype = int)*3)

temp = obs_space.sample()

print(temp)