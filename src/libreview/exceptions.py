class TOUNotAcceptedError(Exception):
    "Raised when TOU needs to be accepted by the user"
    pass

class BadCredentialsError(Exception):
    "Raised when bad credentials are provided"
    pass