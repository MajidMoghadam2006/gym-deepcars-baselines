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

cd /hb/home/mamoghad/Scripts/gym-deepcars-baselines/

python -m baselines.run --alg=deepq --network=mlp --total_timesteps=3e5 --env=DeepCars-v0
