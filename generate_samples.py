import json
from scipy.stats import qmc


def generate_sobol_samples(space, base_data, n_samples=16384):
    # Define the dimension of the parameter space
    dim = len(space)
    # Create a Sobol sequence generator
    sobol = qmc.Sobol(d=dim, scramble=True)

    # Generate samples in the unit hypercube
    samples_unit_cube = sobol.random(n=n_samples)  # Get exactly n_samples points

    # Scale samples to the parameter range
    sobol_samples = []
    for sample in samples_unit_cube:
        new_sample = base_data.copy()
        for i, (key, value) in enumerate(space.items()):
            # Scale the ith dimension to the parameter range
            range_min, range_max = value['range']
            scaled_value = sample[i] * (range_max - range_min) + range_min
            new_sample[key] = scaled_value
        sobol_samples.append(new_sample)

    return sobol_samples


def save_samples_to_file(samples, file_path):
    with open(file_path, 'w') as f:
        for sample in samples:
            json.dump(sample, f)
            f.write('\n')


data = {
    "atom_number": 50000000,
    "oven_velocity_cap": 230,
    "oven_position_x_mm": -83,
    "oven_position_y_mm": 0,
    "oven_position_z_mm": 0,
    "phase_plot": False,
    "use_3d_quadrupole": True,
    "microchannel_radius": 0.2,
    "microchannel_length": 4.0,
    "diff_pump_radius_mm": 1.5,
    "diff_pump_offset_mm": 0,
    "cooling_intersection_offset_mm": 0.0,
    "zeeman_slower_radius_mm": 10.0,
    "zeeman_slower_detuning_mhz": -100.0,
    "zeeman_slower_power_mw": 50.0,
    "use_zeeman_slower": False,
    "use_field_grid": False
}

space = {
    'cooling_beam_detuning': {'range': (-300, 0), 'title': 'Cooling Beam Detuning'},
    'cooling_beam_radius': {'range': (7, 15), 'title': 'Cooling Beam Radius'},
    'cooling_beam_power_mw': {'range': (0, 250), 'title': 'Cooling Beam Power'},
    'push_beam_detuning': {'range': (-250, 0), 'title': 'Push Beam Detuning'},
    'push_beam_radius': {'range': (0.5, 1.5), 'title': 'Push Beam Radius'},
    'push_beam_power': {'range': (0, 10), 'title': 'Push Beam Power'},
    'push_beam_offset': {'range': (0, 5), 'title': 'Push Beam Offset'},
    'quadrupole_gradient': {'range': (0, 100), 'title': 'Quadrupole Gradient'},
    'vertical_bias_field': {'range': (-50, 50), 'title': 'Vertical Bias Field'}
}

samples = generate_sobol_samples(space, data)
file_path = 'samples.json'
save_samples_to_file(samples, file_path)