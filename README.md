# Baselines for DeepCars

This is the registered version of [DeepCars](https://github.com/MajidMoghadam2006/gym-deepcars) for the [OpenAI Gym](https://github.com/openai/gym) [environments](https://github.com/openai/gym/tree/master/gym/envs). DeepCars is a simple highway traffic simulator for training Reinforcement Learning agents to perform the high-level decision making on self-driving cars.

Here we exploited the OpenAI baselines framework to train the agent in DeepCars in order to perform the high-level decision making of a self-driving cars in a highway driving setup.

```ruby
pip install -r requirements.txt
cd gym-deepcars-baselines
pip install -e .  
cd baselines  
pip install -e .  
cd ..
```

Training:
```ruby
python -m baselines.run --alg=deepq --network=mlp --num_timesteps=3e5 --env=DeepCars-v0
```

Evaluation:
```ruby
python -m baselines.run --alg=deepq --network=mlp --num_timesteps=0 --env=DeepCars-v0 --load_path=./model.pkl --play
```
