import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('/Users/Majid/Documents/GitHub/gym-deepcars-baselines/progress.csv')

mean100 = data['RL_Shallow']
steps = data['steps']

plt.figure()
plt.plot(steps, mean100, label='Shallow RL', zorder=1)  # on top
plt.title('100 episode rewards')
plt.show()
