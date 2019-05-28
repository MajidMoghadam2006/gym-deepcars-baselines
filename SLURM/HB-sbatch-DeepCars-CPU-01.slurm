#!/bin/bash
#   Note - there can be no empty lines between #SBATCH directives.
#SBATCH --job-name=deepcars
#SBATCH --output=cpu_%j.out
#SBATCH --error=cpu_%j.err
#SBATCH --ntasks=1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=mamoghad@ucsc.edu
#SBATCH --partition=128x24

source /hb/home/mamoghad/Scripts/gym-deepcars-baselines/venv/bin/activate

export PYTHONPATH=/hb/home/mamoghad/Scripts/gym-deepcars-baselines/venv/lib/python3.6/site-packages:$PYTHONPATH

cd /hb/home/mamoghad/Scripts/gym-deepcars-baselines/

python -m baselines.run --alg=deepq --network=shallow_mlp --num_timesteps=1e5 --env=DeepCars-v3

