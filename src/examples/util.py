
def display_qubo(qubo_dict):
    """Save a QUBO in a well readable format to a txt file.

    Parameters
    ----------
    qubo_dict
        Dictionary that represents the QUBO
    """

    print(qubo_dict)
    max_1 = max(list(map(lambda x: x[0], qubo_dict.keys())))
    max_2 = max(list(map(lambda x: x[1], qubo_dict.keys())))

    amount_of_vars = max_1 if max_1 >= max_2 else max_2

    max_val = -100000000

    for i in range(0, amount_of_vars+1):
        for j in range(0, amount_of_vars + 1):
            if (i, j) in qubo_dict and abs(qubo_dict[(i, j)]) >= max_val:
                max_val = qubo_dict[(i, j)]

    space_per_number = len(str(max_val))
    empty_space = 3

    with open("qubo.txt", "w") as file:
        for i in range(0, amount_of_vars + 1):
            line = ""
            for j in range(0, amount_of_vars + 1):
                if (i, j) in qubo_dict:
                    str_val = str(qubo_dict[(i, j)])
                    line += str_val + " " * (space_per_number - len(str_val) + empty_space)
                else:
                    line += "0" + " " * (space_per_number - 1 + empty_space)

            file.write(line + "\n")
