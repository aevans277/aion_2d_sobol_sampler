import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from library.data_processing import pipeline, write_data
from library.run_sim import run_sim
from numpy import linspace
import seaborn as sns

def plot_3d(step_number, df):
    step_df = df[df['Step'] == step_number]  # filter for specific step

    # normalise the velocity magnitudes
    norm = plt.Normalize(0, 300)
    colors = plt.cm.viridis(norm(step_df['Vm']))  # map to colours

    # setup figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # quiver used to draw arrows with mapped colours
    ax.quiver(step_df['Z'], step_df['X'], step_df['Y'],
              step_df['Vz'], step_df['Vx'], step_df['Vy'],
              length=0.01, normalize=True, color=colors)

    # set title and axes labels
    ax.set_title(f'3D Atom Positions at Step {step_number}')
    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')

    # set axis limits
    ax.set_xlim([-0.1, 0.1])
    ax.set_ylim([-0.1, 0.1])
    ax.set_zlim([-0.1, 0.1])

    # adjust viewing angle
    ax.view_init(elev=20, azim=165)

    # create legend for velocity magnitudes
    mappable = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.viridis)
    mappable.set_array([])
    cbar = plt.colorbar(mappable, ax=ax, fraction=0.02, pad=0.1)
    cbar.set_label('Velocity Magnitude')

    plt.show()

def setup_3d_animate(df):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-0.1, 0.1])
    ax.set_ylim([-0.1, 0.1])
    ax.set_zlim([-0.1, 0.1])
    ax.set_xlabel('Z')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')

    def update(step):
        ax.clear()
        step_df = df[df['Step'] == step]
        norm = plt.Normalize(0, 300)
        colors = plt.cm.viridis(norm(step_df['Vm']))
        ax.quiver(step_df['Z'], step_df['X'], step_df['Y'],
                  step_df['Vz'], step_df['Vx'], step_df['Vy'],
                  length=0.01, normalize=True, color=colors)
        ax.set_xlim([-0.1, 0.1])
        ax.set_ylim([-0.1, 0.1])
        ax.set_zlim([-0.1, 0.1])
        ax.set_xlabel('Z')
        ax.set_ylabel('X')
        ax.set_zlabel('Y')
        ax.set_title(f'Step: {step}')

    steps = df['Step'].unique()

    return fig, update, steps


def generate_pdp(data, parameter_name, param_range, num_points, visualise = True, exe_path = './mot', pos_path = 'pos.txt', vel_path = 'vel.txt'):
    """
    Generates a Partial Dependent Plot for a specific parameter.

    :param data: The original data dictionary to use for the simulation.
    :param parameter_name: The name of the parameter to vary.
    :param param_range: A tuple (min, max) defining the range over which to vary the parameter.
    :param num_points: Number of points to simulate within the range.
    """

    def count_obj(df, z_threshold=0.075):
        filtered_df = df[df['Z'] >= z_threshold]

        unique_atoms = filtered_df['Atom Number'].unique()

        unique_count = len(unique_atoms)

        return unique_count

    # Create a range of values for the parameter
    values = linspace(param_range[0], param_range[1], num_points)

    # Initialise a list to hold the results
    results = []

    for value in values:
        # Update the parameter in the data dictionary
        data[parameter_name] = value

        # Write the modified data to file
        write_data(data)

        # Run the simulation
        run_sim(exe_path, False)

        # Process the output into a dataframe
        df = pipeline(pos_path, vel_path)

        # Count the target Y value
        obj = count_obj(df)

        # Append the result
        results.append(obj)

    if visualise:

        plt.figure(figsize=(10, 6))
        plt.plot(values, results, '-o')
        plt.title(f'Partial Dependent Plot for {parameter_name}')
        plt.xlabel(parameter_name)
        plt.ylabel('Objective Value')
        plt.grid(True)
        plt.show()

    return results

def plot_loss(trials):
    trial_losses = [x['result']['loss'] for x in trials.trials]
    plt.figure(figsize=(10, 5))
    plt.plot(trial_losses, label='Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.title('Loss Curve over Iterations')
    plt.legend()
    plt.grid(True, which='major', linestyle='--', linewidth=0.5)
    plt.savefig('Loss Curve', format='png', bbox_inches='tight')
    plt.show()


def plot_hyperparams_distributions(trials, space_keys, titles):
    num_plots = len(space_keys)
    num_cols = 3
    num_rows = num_plots // num_cols + (num_plots % num_cols > 0)
    plt.figure(figsize=(15, num_rows * 3))

    for i, key in enumerate(space_keys, 1):
        values = [x['misc']['vals'][key][0] for x in trials.trials if x['misc']['vals'][key]]
        plt.subplot(num_rows, num_cols, i)
        sns.histplot(values, kde=True, bins=20)
        plt.xlabel(titles[key]['title'])
        plt.ylabel('Frequency')
        plt.title(titles[key]['title'])
        plt.xlim(titles[key]['range'])
        plt.grid(True)  # Add grid

    plt.tight_layout()
    plt.savefig('hyperparams_distributions.png')  # Save the figure
    plt.show()



