import mkl
import os
import random
import pandas as pd
import subprocess
import time
import json
from library.data_processing import write_data, pipeline, save_data
from library.run_sim import run_sim

# Set number of threads for various libraries
mkl.set_num_threads(8)
os.environ['OMP_NUM_THREADS'] = '8'
os.environ['OPENBLAS_NUM_THREADS'] = '8'
os.environ['MKL_NUM_THREADS'] = '8'
os.environ['NUMEXPR_NUM_THREADS'] = '8'
os.environ['VECLIB_MAXIMUM_THREADS'] = '8'
os.environ['BLIS_NUM_THREADS'] = '8'

def count_obj(df, z_threshold=0.075):
    filtered_df = df[df['Z'] >= z_threshold]
    unique_atoms = filtered_df['Atom Number'].unique()
    unique_count = len(unique_atoms)
    return unique_count

def read_sample(file_path='../../samples.json'):
    # Temporarily hold the lines to rewrite them back to the file
    all_lines = []
    data = None

    with open(file_path, 'r') as file:
        all_lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in all_lines:
            if data is None:  # Only look for a new line if we haven't found our sample yet
                try:
                    sample = json.loads(line.strip())
                    if sample['atom_number'] != 0:
                        # Save original data to return
                        data = sample.copy()
                        # Modify the atom_number to 0 for the file update
                        sample['atom_number'] = 0
                        line = json.dumps(sample) + '\n'  # Update the line to write back to the file
                except json.JSONDecodeError:
                    continue  # Skip any lines that are not valid JSON

            file.write(line)  # Write the original or modified line back to the file

    return data

file_path = 'input.json'  # file path to JSON
exe_path = './mot'  # path to 2D MOT
pos_path = 'pos.txt'
vel_path = 'vel.txt'
save_path = '../../data/5e7_sobol'

samples = 1000

for i in range(samples):
    print('1')

    params = read_sample()

    print('2')

    write_data(params, file_path='input.json')

    print('3')

    run_sim(exe_path, False)

    print('4')

    twomot_df = pipeline(pos_path='pos.txt', vel_path='vel.txt')
    obj = count_obj(twomot_df, z_threshold=0.075)
    obj_params = {**params, "objective": obj}

    save_data(obj_params, pos_path, vel_path, save_path)

    print('5')
