import mkl

mkl.set_num_threads(8)

import os
os.environ['OMP_NUM_THREADS'] = '8'
os.environ['OPENBLAS_NUM_THREADS'] = '8'
os.environ['MKL_NUM_THREADS'] = '8'
os.environ['NUMEXPR_NUM_THREADS'] = '8'
os.environ['VECLIB_MAXIMUM_THREADS'] = '8'
os.environ['BLIS_NUM_THREADS'] = '8'

import subprocess

def run_sim(exe_path, silent=True):
    if silent:
        result = subprocess.run([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    else:
        result = subprocess.run([exe_path], capture_output=True, text=True)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)



    return result
