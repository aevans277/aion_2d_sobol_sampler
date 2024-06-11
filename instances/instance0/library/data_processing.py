import mkl

mkl.set_num_threads(8)

import os
os.environ['OMP_NUM_THREADS'] = '8'
os.environ['OPENBLAS_NUM_THREADS'] = '8'
os.environ['MKL_NUM_THREADS'] = '8'
os.environ['NUMEXPR_NUM_THREADS'] = '8'
os.environ['VECLIB_MAXIMUM_THREADS'] = '8'
os.environ['BLIS_NUM_THREADS'] = '8'

import json
import pandas as pd
import os
import shutil

def read_data(file_path):
    rows = []  # initialise rows array

    # open file and read in line by line
    with open(file_path, 'r') as file:
        step = None
        for line in file:
            line = line.strip()
            if line.startswith("step"):
                # extract step
                step = int(line.split("-")[1].split(",")[0])
            else:
                # extract atom number and coordinates
                atom_data, coords = line.split(": ")
                _, atom_number = atom_data.split(",")
                x, y, z = eval(coords)  # convert string tuple into actual tuple

                # append processed row to list
                rows.append([step, int(atom_number), x, y, z])

    # create a dataframe from the list
    df = pd.DataFrame(rows, columns=["Step", "Atom Number", "X", "Y", "Z"])

    return df


def pipeline(pos_path, vel_path):
    pos_df = read_data(pos_path)
    vel_df = read_data(vel_path)

    pos_df['d'] = ((pos_df['X'] ** 2 + pos_df['Y'] ** 2 + pos_df['Z'] ** 2) ** 0.5)
    vel_df['Vm'] = ((vel_df['X'] ** 2 + vel_df['Y'] ** 2 + vel_df['X'] ** 2) ** 0.5)

    vel_df.rename(columns={'X': 'Vx', 'Y': 'Vy', 'Z': 'Vz'}, inplace=True)

    full_df = pd.merge(pos_df, vel_df, on=['Step', 'Atom Number'], how='inner')

    return full_df

def write_data(data, file_path = 'input.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def save_data(data, pos_path, vel_path, folder_path = './data'):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Find the next available file number
    existing_files = [f for f in os.listdir(folder_path) if f.startswith("input") and f.endswith(".json")]
    existing_numbers = [int(f.replace("input", "").replace(".json", "")) for f in existing_files if
                        f.replace("input", "").replace(".json", "").isdigit()]
    next_number = max(existing_numbers) + 1 if existing_numbers else 1

    # Define the new file paths
    new_json_path = os.path.join(folder_path, f"input{next_number}.json")
    new_pos_path = os.path.join(folder_path, f"pos{next_number}.txt")
    new_vel_path = os.path.join(folder_path, f"vel{next_number}.txt")

    # Save the data to the new JSON file
    with open(new_json_path, 'w') as file:
        json.dump(data, file)

    # Move and rename pos.txt and vel.txt
    shutil.copy(pos_path, new_pos_path)
    shutil.copy(vel_path, new_vel_path)

def json_to_df(folder_path):
    # List to hold DataFrames
    dfs = []

    # List all files in the directory
    for file_name in os.listdir(folder_path):
        # Check if the file is a JSON file
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            # Read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Convert the dictionary to a DataFrame and append to the list
                dfs.append(pd.DataFrame([data]))

    # Concatenate all DataFrames in the list into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)

    return final_df

