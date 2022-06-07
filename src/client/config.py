from .connection import Connection
import json


class Config:
    """A class that represents a config object containing the configuration data of the user. The config object is
    created at the beginning of execution (in main.py) either by a config file or by passed arguments specifying the
    configuration options.

    Attributes
    ----------
    endpoint
        endpoint (ip+port) to which the connection will be established
    method
        authentication method
    credentials
        personal token of the user

    The endpoint, method and credentials are specified in the config file or passed as a parameter to the config
    object in main.py.

    Methods
    ----------
    create_connection()
        Create a Connection object containing the configuration data of the user.
    """

    def __init__(self, **kwargs):
        """Create the config object and set the configuration data for the current user.

        Parameters
        ----------
        **kwargs
            **kwargs contains an unspecified number of arguments
            Either the arguments consist of the configuration data itself (endpoint, method, credentials)
            or the path to the config file containing the configuration data.
        """

        # authentication without config file
        if "endpoint" in kwargs:
            self.endpoint = kwargs["endpoint"]
        if "method" in kwargs and "credentials" in kwargs:
            self.method = kwargs["method"]
            self.credentials = kwargs["credentials"]
        if "private_key_file" in kwargs:
            self.private_key_file = kwargs["private_key_file"]
        elif "configpath" in kwargs:
            # authentication with config file
            with open(kwargs["configpath"]) as configfile:
                config = json.load(configfile)
                self.method = config["method"]
                self.credentials = config["credentials"]
                self.endpoint = config["endpoint"]
                self.private_key_file = config["private_key_file"]

    def create_connection(self):
        """Create a connection object containing the configuration data of the user. """
        return Connection(self.endpoint, self.method, self.credentials, self.private_key_file)
