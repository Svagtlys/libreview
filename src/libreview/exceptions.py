class TOUNotAcceptedError(Exception):
    "Raised when TOU needs to be accepted by the user"
    pass

class BadCredentialsError(Exception):
    "Raised when bad credentials are provided"
    pass

class UnexpectedResponseError(Exception):
    """Raised when the response isn't otherwise incorrect but doesn't look like we expect"""
    pass