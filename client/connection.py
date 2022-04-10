import zmq
import zmq.auth
import os
from .. import Problem
from .. import Response
from .. UQOExceptions import *


class Connection:
    """ This class contains methods for the communication handling with the server, e.g. assembling the request message
    with all relevant data, creating a connection and sending requests to the server. A Connection object contains
    the configuration data of the user (url, auth_method and credentials) and additional data referring to the task
    that will be sent to the server. The configuration data is set by initialization as it is passed in the
    create_connection() method in the Config class.


    Attributes
    ----------
    url
        ip+port to which the connection will be established (endpoint)
    auth_method
        authentication method
    credentials
        personal token of the user
    preferred_solver
        Specifies which solver should be used. Available solvers can be displayed by calling the method
        get_available_dwave_solvers().
    preferred_platform
        Specifies which platform should be used. Platforms can be "dwave", "qbsolv" or "uq".
    task
        Specifies the type of task the server should execute.
        Tasks can be "solve", "ping", "dwave_info", "uq_info", "show_quota" or "util".
    solver
        Specifies which solver should be used.
    context
        ZeroMQ-Context

    Methods
    -------
    ping()
        Send a ping message for testing the connection to the server
    find_chimera_embedding(problem)
        Return a chimera embedding for a given problem
    find_pegasus_embedding(problem)
        Return a pegasus embedding for a given problem
    solve_qubo(problem)
        Solve a QUBO problem either with QBsolv or a DWave-Solver
    solve_ising(problem)
        Solve an Ising problem either with QBsolv or a DWave-Solver
    get_available_dwave_solvers()
        Return a list of available solvers from DWave
    get_available_platforms()
        Return a list of available platforms
    get_authentication_message()
        Returns a dictionary that contains the authentication method and the credentials of the user
    get_task_details_message()
        Returns a dictionary that contains information referring to the task
    set_preferred_solver(), set_preferred_platform(), set_task()
        Setter methods for the attributes preferred_solver, preferred_platform and task
    available_tasks()
    send_message(message)
        Create a request socket and connect to the endpoint specified in url. Send the message and return the reply.
    to_json()
    check_errors()
        Check if the message from the server contains an authentication or backend exception
    show_quota()
        Print the time a user has left for computation on a d-wave platform.
    """

    def __init__(self, url, auth_method, credentials, private_key_file):
        """Initialize the connection object. Fill the config data (url, auth_method and credentials) by using the
        passed arguments.

        Parameters
        ----------
        url
            ip+port to which the connection will be established (endpoint)
        auth_method
            authentication method
        credentials
            personal token of the user
        """
        self.url = url
        self.credentials = credentials
        self.auth_method = auth_method
        self.preferred_solver = None
        self.preferred_platform = None
        self.task = None
        self.solver = None
        self.private_key_file = private_key_file
        self.context = zmq.Context().instance()

    # ----------------------- PING MESSAGE ----------------------- #
    def ping(self):
        """Send a ping message to the server. Server should answer with message {"status": "success", "type": "pong"}.

        Returns
        -------
        answer["type"]
            The "pong" from the server
        """
        ping_message = {
            "task": "ping",
            "authentication": self.get_authentication_message()
        }
        answer = self.send_message(ping_message)
        return answer["type"]

    # ----------------------- FIND EMBEDDING MESSAGE ----------------------- #

    def find_chimera_embedding(self, problem):
        """Send a request to the server to find a chimera embedding for a given problem.

        Parameters
        ----------
        problem
            A QUBO or Ising representation of a problem

        Returns
        -------
        embedding
            The Chimera embedding the server sent back
        """

        # Check if problem has a valid format (QUBO or Ising).
        if isinstance(problem, Problem.Qubo) or isinstance(problem, Problem.Ising):
            problem_dict = problem.to_json()
        else:
            raise Exception

        # Create the message that will be sent to the server
        find_embedding_message = {
            "authentication": self.get_authentication_message(),
            "task": "util",
            "task_details": {
                "platform": "dwave",
                "params": {
                    "pref_solver": problem.solver,
                },
                "type": "find_chimera_embedding",
                "problem": problem_dict,
            }
        }

        # Send message to server and save the response in answer
        answer = self.send_message(find_embedding_message)

        # Extract the embedding from the response.
        embedding_stringed = answer["solver_details"]["embedding"]
        embedding = {}
        for key in embedding_stringed:
            embedding[int(key)] = embedding_stringed[key]

        return embedding

    def find_pegasus_embedding(self, problem):
        """Sends a request to the server to find a pegasus embedding for a given problem.

        Parameters
        ----------
        problem
            A QUBO or Ising representation of a problem

        Returns
        -------
        embedding
            Pegasus embedding
        """
        if isinstance(problem, Problem.Qubo) or isinstance(problem, Problem.Ising):
            problem_dict = problem.to_json()
        else:
            raise Exception

        find_embedding_message = {
            "authentication": self.get_authentication_message(),
            "task": "util",
            "task_details": {
                "platform": "dwave",
                "params": {
                    "pref_solver": problem.solver,
                },
                "type": "find_pegasus_embedding",
                "problem": problem_dict,
            }
        }

        answer = self.send_message(find_embedding_message)
        embedding_stringed = answer["solver_details"]["embedding"]

        embedding = {}
        for key in embedding_stringed:
            embedding[int(key)] = embedding_stringed[key]

        return embedding

    # --------------- FIND INITIAL STATE MESSAGE ---------------- #

    def find_initial_state(self, problem):
        """ Execute the solve method for finding an initial state for the reverse annealing process.
        To not get stuck in a local minimum, take a solution which is 5% distant from lowest-energy solution as
        the initial state for the following reverse annealing call. """

        answer = Response.DWaveResponse
        if isinstance(problem, Problem.Qubo):
            answer = self.solve_qubo(problem)
        elif isinstance(problem, Problem.Ising):
            answer = self.solve_ising(problem)

        # take the solution with the lowest energy
        initial = dict(answer.solutions[0])

        initial_parsed = {}
        for key in initial:
            initial_parsed[int(key)] = int(initial[key])

        print("Calculated initial state: " + str(initial_parsed))

        return initial_parsed

    # ----------------------- SOLVE QUBOS ----------------------- #

    def solve_qubo(self, problem):
        """Solve a QUBO problem with either QBsolv or a DWave-Solver.

        Returns
        -------
        answer
            The response of type QBSolveResponse or DWaveResponse with the answer from the solver
        """

        # check if problem is in valid QUBO form
        if not isinstance(problem, Problem.Qubo):
            raise NotAQuboException
        else:

            solve_message = {
                "authentication": self.get_authentication_message(),
                "task_details": self.get_task_details_message(problem),
                "task": "solve" if self.task is None else self.task,
            }

            answer = self.send_message(solve_message)

            if answer["status"] == "success":
                if answer["solver"] == "QBsolvSolver":
                    answer = Response.QBSolveResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "DWaveSolver":
                    answer = Response.DWaveResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "FujitsuDAUSolver":
                    answer = Response.FujitsuDAUResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "TabuSolver":
                    answer = Response.TabuResponse(answer["solver_details"]["answer"])
                return answer
            else:
                self.check_errors(answer)
                print(answer["status"])
                print(answer)
                if answer["type"] == "MissingTask":
                    print("Task Fehlt!")
                elif answer["type"] == "InvalidTask":
                    print("UngültigerTask")
                else:
                    raise QBSolveException(answer["message"])

    # ----------------------- SOLVE ISING ----------------------- #

    def solve_ising(self, problem):
        """Solve an Ising problem with either QBsolv or a DWave-Solver.

        Returns
        -------
        answer
            The response of type QBSolveResponse or DWaveResponse with the answer from the solver
        """

        # check if problem is in valid Ising form
        if not isinstance(problem, Problem.Ising):
            raise NotAQuboException
        else:

            solve_message = {
                "authentication": self.get_authentication_message(),
                "task_details": self.get_task_details_message(problem),
                "task": "solve" if self.task is None else self.task,
            }

            answer = self.send_message(solve_message)

            if answer["status"] == "success":
                if answer["solver"] == "QBsolvSolver":
                    answer = Response.QBSolveResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "DWaveSolver":
                    answer = Response.DWaveResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "FujitsuDAUSolver":
                    answer = Response.FujitsuDAUResponse(answer["solver_details"]["answer"])
                elif answer["solver"] == "TabuSolver":
                    answer = Response.TabuResponse(answer["solver_details"]["answer"])
                return answer
            else:
                print(answer["status"])
                print(answer)
                raise QBSolveException(answer["message"])

    # ----------------------- GET DWAVE SOLVERS ----------------------- #

    def get_available_dwave_solvers(self):
        """Return a list of all currently available solvers from DWave. """
        solve_message = {}
        solve_message["authentication"] = self.get_authentication_message()
        solve_message["task"] = "dwave_info"
        solve_message["task_details"] = {"platform": "dwave", "type": "available_solvers"}

        answer = self.send_message(solve_message)
        return list(map(lambda x: str(x), answer["solver_details"]["details"]))

    # ----------------------- GET AVAILABLE PLATFORMS ----------------------- #

    def get_available_platforms(self):
        """Return a list of all currently available platforms. """
        message = {}
        message["authentication"] = self.get_authentication_message()
        message["task"] = "uq_info"
        message["task_details"] = {"type": "available_platforms"}

        answer = self.send_message(message)
        return list(map(lambda x: str(x), answer["details"]))

    # ----------------------------------------  HELPER FUNCTIONS ---------------------------------------- #

    def get_authentication_message(self):
        """Return a dictionary that contains the authentication method and the credentials of the user. """
        return {
            "method": self.auth_method,
            "credentials": self.credentials
        }

    def get_task_details_message(self, problem):
        """Return a dictionary that contains information referring to the task. """
        params = {
            "uq_params": problem.uq_params,
            "solver_params": problem.solver_params
        }

        # if a preferred solver is specified
        if self.preferred_solver is not None:
            params["pref_solver"] = self.preferred_solver

        type = "qubo" if isinstance(problem, Problem.Qubo) else "ising"
        task_details_message = {
            "type": type,
            "task": "solve" if self.task is None else self.task,
            "platform": problem.platform,
            "value": problem.to_json(),
            "params": params
        }
        if self.preferred_platform is not None:
            task_details_message["pref_platform"] = self.preferred_platform

        if problem.embedding is not None:
            task_details_message["embedding"] = problem.embedding

        return task_details_message

    # ----------- setter methods for preferred_solver, preferred_platform and task ----------- #
    def set_preferred_solver(self, preferred_solver):
        self.preferred_solver = preferred_solver

    def set_preferred_platform(self, preferred_platform):
        self.preferred_platform = preferred_platform

    def set_task(self, task):
        self.task = task

    def available_tasks(self):
        return ["solve"]

    def send_message(self, message):
        """Create a request socket and connect to the endpoint specified in url. Send the message and wait for a response message.

        Parameters
        ----------
        message
            The message containing information about the task the server should execute and about authentication data of
            the user.

        Returns
        -------
        answer
            Reply from the server
        """

        socket = self.context.socket(zmq.REQ)  # establish socket

        client_public, client_secret = zmq.auth.load_certificate(self.private_key_file)
        socket.curve_secretkey = client_secret
        socket.curve_publickey = client_public

        # The client must know the server's public key to make a CURVE connection.
        server_public_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uqo_public.key")
        server_public, _ = zmq.auth.load_certificate(server_public_file)
        socket.curve_serverkey = server_public

        socket.connect("tcp://" + self.url)

        json_message = self.to_json(message)  # convert message into json object
        socket.send_json(json_message)  # send message

        answer = socket.recv_json()  # wait for response
        self.check_errors(answer)
        return answer

    def to_json(self, message):
        json_message = dict()
        for key in message:
            if type(message[key]) == dict:
                jsonfyed_message = self.to_json(message[key])
                json_message[key] = jsonfyed_message
            elif type(key) == tuple:
                json_message[str(key)] = message[key]
            else:
                json_message[key] = message[key]
        return json_message

    def check_errors(self, answer):
        """Check if the message from the server contains an authentication or backend exception. If there occurs an
        exception, raise an appropriate Exception. For further details about a specific Exception see the collection of
        all exceptions in UQOExceptions.py.

        Parameters
        ----------
        answer
            Response message from the server
        """

        # Check the status of the response. The "type" entry of the response specifies which exception occurred.
        if answer["status"] == "error":
            error_type = answer["type"]

            # Auth-Errors
            if error_type == "InvalidTask":
                raise InvalidTaskException(answer["error_details"])
            elif error_type == "MissingAuthenticationMethod":
                raise AuthMessageMissingException()
            elif error_type == "InvalidAuthenticationMethod":
                raise InvalidAuthMethodException(answer["error_details"])
            elif error_type == "InvalidCredentials":
                raise InvalidAuthCredentials()
            elif error_type == "MissingAuthenticationCredentials":
                raise MalformedAuthMessageException()
            elif error_type == "MissingTask":
                raise MissingTaskException()
            elif error_type == "generic_auth_error":
                raise GenericAuthException()
            elif error_type == "fast_retry_exception":
                raise FastRetryException(answer["error_details"])
            elif error_type == "auth_admin_failed":
                raise AuthAdminFailedException()
            elif error_type == "InsufficientQuota":
                raise InsufficientQuotaException()

            # Backend-Errors

            elif error_type == "generic_backend_error":
                raise GenericBackendException

            elif error_type == "solver_error":
                raise SolverException(answer["error_details"])
            elif error_type == "MissingTask":
                raise MissingTask()
            elif error_type == "InvalidTask":
                raise InvalidTask(answer["error_details"])
            elif error_type == "InvalidSolver":
                raise InvalidSolverException(answer["error_details"])
            elif error_type == "MissingPlatform":
                raise MissingPlatformException(answer["error_details"])
            elif error_type == "InvalidPlatform":
                raise InvalidPlatformException()
            elif error_type == "FujitsuException":
                raise FujitsuException(answer["error_details"])
            elif error_type == "TabuException":
                raise TabuException(answer["error_details"])

    def show_quota(self):
        """Print the remaining quota (the time you can spend on a DWave platform in microseconds). """

        show_coins_message = {
            "authentication": self.get_authentication_message(),
            "task": "show_quota",
        }

        # send message to server
        answer = self.send_message(show_coins_message)
        print(answer["quota"])
