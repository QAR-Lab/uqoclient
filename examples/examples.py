from ..client.connection import Connection
from . import graph_coloring_example as graphcoloring
from .. import Problem
from matplotlib import pyplot as plt
import numpy as np

# Example QUBO with some reward and penalty values
example_qubo = {(0, 0): -2, (1, 1): -2, (2, 2): -2, (3, 3): -2, (4, 4): -2, (5, 5): -2,
                (0, 1): 5, (0, 2): 5, (0, 4): 5,
                (1, 3): 5, (1, 5): 5,
                (2, 3): 5, (2, 4): 5,
                (3, 5): 5,
                (4, 5): 5}

# Ising problem with some example values for external magnetic field (example_ising_h) and interaction (example_ising_J)
example_ising_h, example_ising_J = {1: 1, 2: 2, 3: 3}, {(1, 2): 4, (1, 3): 5, (2, 3): 6}


def ping(config):
    """Send a ping message to the server.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """
    con = config.create_connection()
    print(con.ping())


def qbsolv_example_qubo(config):
    """Solve the QUBO example with QBSolv.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    test_dict = {"test_parameter": {(0, 1): 5, (1, 2): 3}}
    answer = Problem.Qubo(config, example_qubo).with_platform("qbsolv").with_params(**test_dict).solve(100)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def qbsolv_example_ising(config):
    """Solve the Ising example with QBSolv.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    # Create the Ising representation of a problem we want to solve

    answer = Problem.Ising(config, example_ising_h, example_ising_J).with_platform("qbsolv").solve(48)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def dwave_example_qubo(config):
    """Solve the QUBO example with the quantum solver 'DW_2000Q_6' from DWave.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    answer = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("DW_2000Q_6").solve(1)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def dwave_example_ising(config):
    """Solve the Ising example with the quantum solver 'DW_2000Q_6' from DWave.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    answer = Problem.Ising(config, example_ising_h, example_ising_J).with_platform("dwave") \
        .with_solver("DW_2000Q_6").solve(1)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()

    answer.print_solutions_nice()


def get_dwave_solvers(config):
    """Show all available solvers from DWave. """
    connection = config.create_connection()
    print(connection.get_available_dwave_solvers())


def show_quota(config):
    """Print the users remaining quota. """
    connection = config.create_connection()
    connection.show_quota()


def graph_coloring_example(config):
    """Process an example of the graph coloring problem as a QUBO by using QBSolv. """
    QUBO = graphcoloring.create_qubo()
    answer = Problem.Qubo(config, QUBO).with_platform("qbsolv").solve(2)

    for index, solution in enumerate(answer.solutions):
        graphcoloring.show_solution(solution, "graph_coloring_solution_" + str(index))


def find_chimera_embedding_example(config):
    """Find a possible Chimera embedding by calling the DW_2000Q_6 solver from DWaveand save it to embedding.pdf. """
    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("DW_2000Q_6")
    # Note: If you generate an embedding via problem.find_chimera_embedding(), the embedding will be saved in the
    #       variable problem.embedding - you can directly access, view and save it.
    problem.find_chimera_embedding()
    problem.draw_chimera_embedding("embedding.pdf")


def find_pegasus_embedding_example(config):
    """Find a possible Pegasus embedding by calling the Advantage_system4.1 solver from DWave and save it to
    embedding.pdf. """
    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("Advantage_system4.1")
    # Note: If you generate an embedding via problem.find_chimera_embedding(), the embedding will be saved in the
    #       variable problem.embedding - you can directly access, view and save it.
    problem.find_pegasus_embedding()
    problem.draw_pegasus_embedding("embedding_pegasus.pdf")


def dwave_example_qubo_with_custom_embedding(config):
    """Solve an example QUBO problem with a given embedding. """

    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("Advantage_system4.1")

    # Note: If you generate an embedding via problem.find_chimera_embedding(), the embedding will be saved in the
    #       variable problem.embedding - you can directly access, view and save it.
    problem.find_chimera_embedding()

    # This will automatically use the embedding generated with problem.find_chimera_embedding()
    # In general: if you have an embedding already - just assign this embedding to the problem.embedding variable
    # If you call problem.solve after, UQ will automatically use this embedding to solve the problem on the D-Wave
    answer = problem.solve(2)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()

    answer.print_solutions_nice()


def dwave_example_qubo_reverse_annealing(config):
    """ Solve a QUBO with reverse annealing (by optimizing a given solution).

    1. `initial_state` specifies the classical state at which the reverse anneal should start. An initial state could
        look like this: {0: 1, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0}
        2 possibilities:
        - define a known solution as an initial state
        - compute an initial state by using forward annealing
    2. `reinitialize_state` specifies whether or not the initial state should be used for every anneal in the request.
        If False, then after the first, each subsequent anneal starts where the previous finished.
    3. `anneal_schedule` defines the annealing schedule that should be followed. A schedule starts at s=1.0, reverses
        to s_target, pauses for hold_time μs and then anneals forward to s=1.0.
    """

    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("Advantage_system4.1")

    # 1. initial state:
    # define a known solution as the initial state:
    # initial = {0: 1, 2: 0, 1: 0, 3: 1, 4: 0, 5: 0}

    # or calculate an initial state
    initial = problem.find_initial_state(1)

    # 2. reinitialize_state:
    reinitialize_state = False

    # 3. data for the anneal schedule:
    s_target = 0.45
    hold_time = 80

    reverse_anneal_params = {'initial_state': initial, 'reinitialize_state': reinitialize_state, 's_target': s_target,
                             'hold_time': hold_time}

    answer = problem.with_params(**reverse_anneal_params).solve(10)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------

    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()

    answer.print_solutions_nice()


def dwave_example_ising_reverse_annealing(config):
    """ Solve an Ising with reverse annealing (by optimizing a given solution).

    1. `initial_state` specifies the classical state at which the reverse anneal should start. An initial state could
        look like this: {0: 1, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0}
        2 possibilities:
        - define a known solution as an initial state
        - compute an initial state by using forward annealing
    2. `reinitialize_state` specifies whether or not the initial state should be used for every anneal in the request.
        If False, then after the first, each subsequent anneal starts where the previous finished.
    3. `anneal_schedule` defines the annealing schedule that should be followed. A schedule starts at s=1.0, reverses
        to s_target, pauses for hold_time μs and then anneals forward to s=1.0.
    """

    problem = Problem.Ising(config, example_ising_h, example_ising_J).with_platform("dwave").with_solver("Advantage_system4.1")

    # 1. initial state:
    # define a known solution as the initial state:
    # initial = {0: 1, 2: 0, 1: 0, 3: 1, 4: 0, 5: 0}

    # or calculate an initial state
    initial = problem.find_initial_state(1)

    # 2. reinitialize_state:
    reinitialize_state = False

    # 3. data for the anneal schedule:
    s_target = 0.45
    hold_time = 80

    reverse_anneal_params = {'initial_state': initial, 'reinitialize_state': reinitialize_state, 's_target': s_target,
                             'hold_time': hold_time}

    answer = problem.with_params(**reverse_anneal_params).solve(10)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------

    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()

    answer.print_solutions_nice()


def fujistu_example_qubo(config):
    """ Solve the QUBO example with Fujitsu DAU.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    solver = "CPU"  # CPU or DAU
    number_runs = 16
    parameters = {
        # default parameters:
        "number_iterations": 500,           # total number of iterations per run
        "temperature_start": 1000.0,        # start temperature as float value
        "temperature_end": 1.0,             # end temperature as float value or None
        "temperature_mode": 0,              # 0, 1, or 2 to define the cooling curve
                                            # 0: reduce temperature by factor (1-temperature_decay) every temperature_interval steps
                                            # 1: reduce temperature by factor (1-temperature_decay*temperature) every temperature_interval steps
                                            # 2: reduce temperature by factor (1-temperature_decay*temperature^2) every temperature_interval steps
        "temperature_decay": 0.001,         # decay per step if temperature_end is None
        "temperature_interval": 100,        # number of iterations keeping temperature constant
        "offset_increase_rate": 0.0,        # increase of dynamic offset when no bit selected, set to 0.0 to switch off dynamic energy feature
        "solution_mode": "COMPLETE",        # COMPLETE returns all runs best configuration, QUICK returns overall best configuration only
        "optimization_method": "annealing",  # annealing or parallel tempering are supported methods
        "number_replicas": 26,              # number of replicas for parallel tempering mode
        "annealer_version": 2,              # Digital Annealer version
        "guidance_config": {},              # list of variable values that to be set for DA as a starting values of variables for annealing process for each run
        "auto_tuning": 0,                    # EXPERIMENTAL! options of automatic tuning the QUBO
        "bit_precision": 16,                 # bit precision (DAU version 2)
        "connection_mode": "CMODE_ASYNC"    # Mode can be CMODE_ASYNC (default) or CMODE_SYNC
        }
    answer = Problem.Qubo(config, example_qubo).with_platform("fujitsu").with_solver(solver).with_params(**parameters).solve(number_runs)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def fujistu_example_ising(config):
    """ Fujitsu DAU can only solve QUBOs. Translate Ising to QUBO and send the QUBO to the Fujitsu DAU. There may
    be an offset, that have to be applied to the energies to obtain the correct Ising energies.

    Parameters
    ----------
    config
        The config object that contains the users configuration data
    """

    solver = "CPU"  # CPU or DAU
    number_runs = 16  # number of stochastically independent runs
    parameters = {
        # default parameters:
        "number_iterations": 500,           # total number of iterations per run
        "temperature_start": 1000.0,        # start temperature as float value
        "temperature_end": 1.0,             # end temperature as float value or None
        "temperature_mode": 0,              # 0, 1, or 2 to define the cooling curve
                                            # 0: reduce temperature by factor (1-temperature_decay) every temperature_interval steps
                                            # 1: reduce temperature by factor (1-temperature_decay*temperature) every temperature_interval steps
                                            # 2: reduce temperature by factor (1-temperature_decay*temperature^2) every temperature_interval steps
        "temperature_decay": 0.001,         # decay per step if temperature_end is None
        "temperature_interval": 100,        # number of iterations keeping temperature constant
        "offset_increase_rate": 0.0,        # increase of dynamic offset when no bit selected, set to 0.0 to switch off dynamic energy feature
        "solution_mode": "COMPLETE",        # COMPLETE returns all runs best configuration, QUICK returns overall best configuration only
        "optimization_method": "annealing",  # annealing or parallel tempering are supported methods
        "number_replicas": 26,              # number of replicas for parallel tempering mode
        "annealer_version": 2,              # Digital Annealer version
        "guidance_config": {},              # list of variable values that to be set for DA as a starting values of variables for annealing process for each run
        "auto_tuning": 0,                    # EXPERIMENTAL! options of automatic tuning the QUBO
        "bit_precision": 16,                 # bit precision (DAU version 2)
        "connection_mode": "CMODE_ASYNC"    # Mode can be CMODE_ASYNC (default) or CMODE_SYNC
        }
    answer = Problem.Ising(config, example_ising_h, example_ising_J).with_platform("fujitsu").with_solver(solver).with_params(**parameters).solve(number_runs)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences
    # answer.apply_energy_offset(offset)
    # answer.print_energies()
    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def tabu_example_qubo(config):

    answer = Problem.Qubo(config, example_qubo).with_platform("tabu").solve(1)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()


def tabu_example_ising(config):

    answer = Problem.Ising(config, example_ising_h, example_ising_J).with_platform("tabu").solve(1)

    # -----------
    # These calls return arrays containing the raw information in lists
    # -----------
    # answer.solutions
    # answer.energies
    # answer.num_occurrences

    # -----------
    # These functions will print the received information in different ways
    # -----------
    # answer.print_solutions()
    # answer.print_energies()
    # answer.print_num_occurrences()
    answer.print_solutions_nice()