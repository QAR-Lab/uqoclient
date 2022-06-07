import networkx as nx
import matplotlib.pyplot as plt
from . import util


def create_qubo():
    """Convert a problem instance (graph) into an equivalent QUBO representation.

    Returns
    -------
    QUBO
        Dictionary that represents the QUBO
    """

    # Creating the problem instance
    problem_instance = nx.Graph()
    problem_instance.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3)])

    # If you want to see the problem instance, uncomment the following lines
    # Note: networkx sometimes draws the graph kinda strange. just execute the drawing multiple times, to get different
    #       equivalent representations of the problem instance

    # The "names" of the nodes in the graph
    nodes = [0, 1, 2, 3]
    # Think of 0 = red, 1 = green, 2 = blue
    colors = [0, 1, 2]

    amount_of_colors = len(colors)

    QUBO = {}

    # Fill the QUBO
    for n_index, node in enumerate(nodes):
        for c_index, color in enumerate(colors):
            # Reward for assigning a color to a node
            QUBO[(amount_of_colors * n_index + c_index, amount_of_colors * n_index + c_index)] = -1
            # Penalty for assigning multiple colors to a node
            for color in range(1, amount_of_colors - (amount_of_colors * n_index + c_index) % amount_of_colors):
                QUBO[(amount_of_colors * n_index + c_index, amount_of_colors * n_index + c_index + color)] = 2
            # Penalty for assigning the same color to adjacent nodes
            for node2 in list(nx.neighbors(problem_instance, node)):
                n2_index = nodes.index(node2)
                if n_index >= n2_index:
                    continue
                else:
                    QUBO[(amount_of_colors * n_index + c_index, amount_of_colors * n2_index + c_index)] = 1

    # If you want to see the qubo - uncomment the following lines
    # util.display_qubo(QUBO)

    return QUBO


'''
Note: this function works, as we always find valid solutions with QBSolv on small enough problems.
If the problem gets bigger or you try to display a solution received with the D-Wave - you will need to customize the
drawing function here
'''


def show_solution(solution_dict, output_path):
    """Save the solution (the final coloured graph) to a file.

    Parameters
    ----------
    solution_dict
        Dictionary containing the solution
    output_path
        Specifies the path to the file where the solution will be saved
    """
    print(solution_dict)
    # Creating the problem instance
    problem_instance = nx.Graph()
    problem_instance.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3)])
    color_labels = ["red", "green", "blue"]

    node_colors = []

    for colored_node in solution_dict:
        if solution_dict[colored_node] == 0:
            continue
        else:
            node_colors.append(color_labels[colored_node % len(color_labels)])

    nx.draw(problem_instance, with_labels=True, node_color=node_colors, font_color="white")
    print("-----------------\nThe solution file has been created: look at " + output_path + ".pdf\n-----------------")
    plt.savefig(output_path + ".pdf")
