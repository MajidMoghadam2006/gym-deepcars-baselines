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

low = np.ones(5, dtype = int)*0
high = np.ones(5, dtype = int)*2
obs_space = spaces.Box(low, high, dtype = int)

temp = obs_space.sample()

print(temp)