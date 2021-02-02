from ..client.connection import Connection
from . import graph_coloring_example as graphcoloring
from .. import Problem

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
    """Find a possible Pegasus embedding by calling the Advantage_system1.1 solver from DWave and save it to
    embedding.pdf. """
    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("Advantage_system1.1")
    # Note: If you generate an embedding via problem.find_chimera_embedding(), the embedding will be saved in the
    #       variable problem.embedding - you can directly access, view and save it.
    problem.find_pegasus_embedding()
    problem.draw_pegasus_embedding("embedding_pegasus.pdf")


def dwave_example_qubo_with_custom_embedding(config):
    """Solve an example QUBO problem with a given embedding. """

    problem = Problem.Qubo(config, example_qubo).with_platform("dwave").with_solver("Advantage_system1.1")

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
