class AuthException(Exception):
    """
    Raise All Exceptions relating to authentication
    and authorization
    """

    def __init__(self, msg, code=None):
        self.msg = msg
        self.code = code