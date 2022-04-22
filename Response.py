from dimod.sampleset import SampleSet
from prettytable import PrettyTable


class Response:
    """A Response object is created for a response to a solving task (that is solved by QBSolv or a DWave solver).
    It contains the sampleset (solution vectors, energy and number of occurrences), a list of the sampled solution
    vectors (solutions), the energies and the number of occurrences of each solution vector.

    Attributes
    ----------
    sampleset
        Table with solution vectors, energy and number of occurrences
    solutions
        List of the sampled solution vectors
    energies
        List of the solution vectors energies
    num_occurrences
        List of number of occurrences of a solution vector

    Methods
    -------
    print_solutions(), print_energies(), print_num_occurrences()
        Print the solution vectors, the energies and the number of occurrences of the vectors.
    print_solutions_nice()
        Show the solution (solution vectors, energies and number of occurrences) in a well readable table format.
    """

    def __init__(self, sampleset):
        self.sampleset = sampleset
        self.solutions = list(self.sampleset.samples())
        self.energies = list(map(lambda x: x.energy, list(self.sampleset.data(fields=["energy"]))))
        self.num_occurrences = list(
            map(lambda x: x.num_occurrences, list(self.sampleset.data(fields=["num_occurrences"]))))

    def print_solutions(self):
        for solution in self.solutions:
            print(solution)

    def print_energies(self):
        for energy in self.energies:
            print(energy)

    def print_num_occurrences(self):
        for occurrence in self.num_occurrences:
            print(occurrence)

    def print_solutions_nice(self):
        """Show the solution (solution vectors, energies and number of occurrences) in a well readable table format. """
        t = PrettyTable(["Answer-Sample", "Energy", "Num-Occurrences"])

        for index, solution in enumerate(self.solutions):
            t.add_row([solution, self.energies[index], self.num_occurrences[index]])

        print(t)


class QBSolveResponse(Response):
    """Response that represents a reply from the QBSolv Solver. """

    def __init__(self, dimod_answer):
        solution = SampleSet.from_serializable(dimod_answer)
        Response.__init__(self, solution)


class DWaveResponse(Response):
    """Response that represents a reply from the DWave Solver. """

    def __init__(self, dwave_answer):
        sampleset = SampleSet.from_serializable(dwave_answer)
        Response.__init__(self, sampleset)
        self.timing = self.sampleset.info["timing"]


class FujitsuDAUResponse(Response):
    """Response that represents a reply from the DWave Solver. """

    def __init__(self, fujitsu_answer):
        sampleset = SampleSet.from_serializable(fujitsu_answer)
        Response.__init__(self, sampleset)
        self.timing = self.sampleset.info["timing"]


class TabuResponse(Response):
    """Response that represents a reply from the DWave Solver. """

    def __init__(self, dwave_answer):
        sampleset = SampleSet.from_serializable(dwave_answer)
        Response.__init__(self, sampleset)
