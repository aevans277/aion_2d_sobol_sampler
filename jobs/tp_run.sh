#!/bin/bash
#PBS -l select=1:ncpus=8:mem=100gb
#PBS -l walltime=24:00:00
#PBS -N run_array
#PBS -J 1-500

instances_dir="$PBS_O_WORKDIR/../instances"

cd $PBS_O_WORKDIR/..

source ~/miniconda3/etc/profile.d/conda.sh
conda activate aion

export OMP_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=8
export MKL_NUM_THREADS=8
export NUMEXPR_NUM_THREADS=8
export VECLIB_MAXIMUM_THREADS=8
export BLIS_NUM_THREADS=8
export RAYON_NUM_THREADS=8

cd instances

highest_instance=$(ls $instances_dir | grep 'instance' | sed 's/instance//' | sort -n | tail -1)

next_instance=$((highest_instance + 1))

new_instance_dir="$instances_dir/instance$next_instance"
mkdir $new_instance_dir

cp -r "$instances_dir/instance0/"* "$new_instance_dir/"

cd $new_instance_dir

python sampling.py

sleep 500
