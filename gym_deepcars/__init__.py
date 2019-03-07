import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# Autonomous driving
# --------------------------------------------------

register(
    id='DeepCars-v0',
    entry_point='gym_deepcars.envs:DeepCarsEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic=True,
)
