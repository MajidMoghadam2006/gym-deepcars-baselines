import gym
env = gym.make('DeepCars-v0')
env.reset()
for _ in range(1000):
    env.render()
    env.step(2)
    # env.step(env.action_space.sample()) # take a random action