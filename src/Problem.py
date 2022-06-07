from dimod.binary_quadratic_model import BinaryQuadraticModel
import dimod
import dwave_networkx as dnx
import matplotlib.pyplot as plt


class Problem:
    """Class representing a problem in Ising or QUBO format. This class provides function for setting solving
    parameters and specific solvers and functions that belong to problems, e.g. find embeddings for this problem or
    solve the problem.

    Attributes
    ----------
    solver_params: dict
    uq_params: dict
        Dictionary that contains the key "num_repeats", which specifies the number of samplings the solver will process
    config
        Contains the users configuration data
    solver
        Specifies which solver should be used
    platform
        Specifies which platform should be used
    embedding
        Chimera or Pegasus embedding for the problem
    connection
        Connection object containing the configuration data of the user

    Methods
    -------
    with_solver(solver)
        Set the solver attribute to solver
    with_platform(platform)
        Set the platform attribute to platform
    with_params(**kw_params)
        Update the dictionary solver_params with the elements from kw_params
    with_uq_params(**kw_params)
        Update the dictionary uq_params with the elements from kw_params
    find_chimera_embedding()
        Call the connections find_chimera_embedding method to make a server request for finding a chimera
        embedding
    draw_chimera_embedding()
        Save the chimera embedding to a file.
    find_pegasus_embedding()
        Call the connections find_chimera_embedding method to make a server request for finding a pegasus
        embedding
    draw_pegasus_embedding()
        Save the pegasus embedding to a file.
    solve(times)
        Solve a problem by either calling the connections solve_qubo or solve_ising function.
    """

    def __init__(self, config):
        self.solver_params = {}
        self.uq_params = {}
        self.config = config
        self.solver = None
        self.platform = None
        self.embedding = None
        self.connection = config.create_connection()

    # ------------------ Set attributes ------------------ #

    def with_solver(self, solver):
        """Set the solver attribute"""
        self.solver = solver
        return self

    def with_platform(self, platform):
        """Set the platform attribute"""
        self.platform = platform
        return self

    def with_params(self, **kw_params):
        """Update the solver_params dictionary with the elements from kw_params"""
        self.solver_params.update(kw_params)
        return self

    def with_uq_params(self, **kw_params):
        """Update the uq_params dictionary with the elements from kw_params"""
        self.uq_params.update(kw_params)
        return self

    # ------------------ find embeddings ------------------ #

    def find_chimera_embedding(self):
        """Call the connections find_chimera_embedding method to make a server request for finding a chimera
        embedding """
        self.embedding = self.connection.find_chimera_embedding(self)
        return self.embedding

    def draw_chimera_embedding(self, output_path):
        """Save the chimera embedding to a file.

        Parameters
        ----------
        output_path
            Specifies the path to the file where to save the embedding
        """
        dnx.draw_chimera_embedding(dnx.chimera_graph(16, 16, 4), emb=self.embedding, node_size=3, width=.3)
        plt.savefig(output_path)

    def find_pegasus_embedding(self):
        """Call the connections find_chimera_embedding method to make a server request for finding a pegasus
        embedding """
        self.embedding = self.connection.find_pegasus_embedding(self)
        return self.embedding

    def draw_pegasus_embedding(self, output_path):
        """Save the pegasus embedding to a file.

        Parameters
        ----------
        output_path
            Specifies the path to the file where to save the embedding
        """
        dnx.draw_pegasus_embedding(dnx.pegasus_graph(11), emb=self.embedding, node_size=3, width=.3)
        plt.savefig(output_path)

    # ---------------- find initial state ---------------- #

    def find_initial_state(self, times=1):
        """Call the connections find_initial_state method for reverse annealing process. """
        self.uq_params.update({"num_repeats": times})
        return self.connection.find_initial_state(self)

    # ------------------ Solve problems ------------------ #

    def solve(self, times=1):
        """Solve a problem by either calling the connections solve_qubo or solve_ising function.

        Parameters
        ----------
        times: int
            Specifies the count of iterations. If no parameter is passed, the default value is 1.
        """

        self.uq_params.update({"num_repeats": times})
        if self.solver is not None:
            self.connection.set_preferred_solver(self.solver)
        if self.platform is not None:
            self.connection.set_preferred_platform(self.platform)

        if isinstance(self, Qubo):
            return self.connection.solve_qubo(self)
        if isinstance(self, Ising):
            return self.connection.solve_ising(self)


class Qubo(Problem):
    """Represents a problem in QUBO format.

    Attributes
    ----------
    problem_dict: dict
        QUBO represantation of a problem

    Methods
    -------
    to_json()
        Transform a QUBO dictionary into a dimod.BinaryQuadraticModel (BQM) and return the serialized BQM
    """
    def __init__(self, config, qubo_dict):
        Problem.__init__(self, config)
        self.problem_dict = qubo_dict

    def to_json(self):
        """Transform a QUBO dictionary into a dimod.BinaryQuadraticModel (BQM) and return the serialized BQM.

        Returns
        -------
        bqm.to_serializable(): dict
            The serialized BQM
        """
        linear = {}
        quadratic = {}
        for (a, b) in self.problem_dict.keys():
            if a == b:
                linear[a] = self.problem_dict[(a, b)]
            else:
                quadratic[(a, b)] = self.problem_dict[(a, b)]

        bqm = BinaryQuadraticModel(linear, quadratic, 0.0, dimod.BINARY)
        return bqm.to_serializable()


class Ising(Problem):
    """Represents a problem in Ising format.

    Attributes
    ----------
    linear_dict: dict
        external magnetic field values
    quadratic_dict: dict
        interaction values

    Methods
    -------
    to_json()
        Transform an Ising representation of a problem into a dimod.BinaryQuadraticModel (BQM) and return the serialized
        BQM
    """
    def __init__(self, config, linear_dict, quadratic_dict):
        Problem.__init__(self, config)
        self.linear_dict = linear_dict
        self.quadratic_dict = quadratic_dict

    def to_json(self):
        """
        Transform an Ising representation of a problem into a dimod.BinaryQuadraticModel (BQM) and return the serialized
        BQM.

        Returns
        -------
        bqm.to_serializable(): dict
            The serialized BQM
        """
        bqm = BinaryQuadraticModel(self.linear_dict, self.quadratic_dict, 0.0, dimod.SPIN)
        return bqm.to_serializable()
