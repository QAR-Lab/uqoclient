class UQOException(Exception):
    def __init__(self, message):
        Exception.__init__(self, "\n\n" + "-"*10 + message + "\n\n" + "-"*10)


# ------------ CLIENT - EXCEPTIONS ------------ #


class NotAQuboException(UQOException):
    def __init__(self):
        message = "\n\nThe specified Problem is not a uq.Problem.Qubo instance"
        UQOException.__init__(self, message)


# ------------ AUTH - EXCEPTIONS ------------ #


class MissingTaskException(UQOException):
    def __init__(self):
        message = "\n\nNo task specified"
        UQOException.__init__(self, message)


class InvalidTaskException(UQOException):
    def __init__(self, error_details):
        message = "\n\nInvalid task: '" + str(error_details["parameters_sent"]) + \
                  "'\nAvailable tasks are: " + str(list(map(lambda x: str(x), error_details["tasks_available"])))
        UQOException.__init__(self, message)


class InvalidAuthMethodException(UQOException):
    def __init__(self, error_details):
        message = "\n\nAuthentication failed\nInvalid authentication method: '" + str(error_details["parameters_sent"]) + \
                  "'\nAvailable authentication methods are: " + str(list(map(lambda x: str(x), error_details["auth_methods_available"])))
        UQOException.__init__(self, message)


class InvalidAuthCredentials(UQOException):
    def __init__(self):
        message = "\n\nAuthentication failed\nInvalid credentials"
        UQOException.__init__(self, message)


class AuthMessageMissingException(UQOException):
    def __init__(self):
        message = "\n\nAuthentication failed\nNo authentication information provided"
        UQOException.__init__(self, message)


class MalformedAuthMessageException(UQOException):
    def __init__(self):
        message = "\n\nAuthentication failed\nMalformed authentication message"
        UQOException.__init__(self, message)


class FastRetryException(UQOException):
    def __init__(self,answer_details):
        message = "\n\nYou sent too many QUBOs.\nYou are allowed to solve one QUBO every %d seconds" %(answer_details["interval"])
        UQOException.__init__(self, message)


class AuthAdminFailedException(UQOException):
    def __init__(self):
        message = "\n\nInvalid user or insufficient permissions"
        UQOException.__init__(self, message)

class GenericAuthException(UQOException):
    def __init__(self):
        message = "\n\nAn unexpected error occured\nPlease try again later!\n\nShould this problem still occur in some hours please contact the developer: sebastian.zielinski@ifi.lmu.de"
        UQOException.__init__(self, message)


# ------------  BACKEND - SERVER ------------ #

class GenericBackendException(UQOException):
    def __init__(self):
        message = "\n\nAn unexpected error occured\nPlease try again later"
        UQOException.__init__(self, message)


class SolverException(UQOException):
    def __init__(self, answer_details):
        message = "\n\nAn error occured while solving the problem\n\n"+answer_details["message"]
        UQOException.__init__(self, message)


class MissingTask(UQOException):
    def __init__(self):
        message = "\n\nNo task was specified"
        UQOException.__init__(self, message)


class InvalidTask(UQOException):
    def __init__(self, answer_details):
        message = "\n\nAn invalid task was submitted.\nSubmitted task: " + answer_details["value"]
        UQOException.__init__(self, message)


class QBSolveException(UQOException):
    def __init__(self, message):
        UQOException.__init__(self, message)


class InsufficientQuotaException(UQOException):
    def __init__(self):
        message = "\n\nYour quota is insufficient to perform this task."
        UQOException.__init__(self, message)


class InvalidSolverException(UQOException):
    def __init__(self, error_details):
        message = "\n\nThere is no solver named '" + error_details["parameters_sent"] + "' for the platform '" + error_details["platform"] +"'"
        UQOException.__init__(self, message)


class MissingPlatformException(UQOException):
    def __init__(self, error_details):
        message ="\n\nNo platform was specified.\n" \
                 "Valid platforms are: "
        for platform in error_details["available_platforms"]:
            message += "'" + platform + "'"
        UQOException.__init__(self, message)


class InvalidPlatformException(UQOException):
    def __init__(self):
        message ="\n\nThe platform you specified in your request is not valid.\n"
        UQOException.__init__(self, message)


class FujitsuException(UQOException):
    def __init__(self, answer_details):
        message = "\n\nError while accessing Fujitsu Solver:\n" + answer_details["message"]
        UQOException.__init__(self, message)


class TabuException(UQOException):
    def __init__(self, answer_details):
        message = "\n\nError while accessing Tabu Solver:\n" + answer_details["message"]
        UQOException.__init__(self, message)
