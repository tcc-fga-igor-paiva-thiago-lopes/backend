class ApplicationControllerException(Exception):
    """Base Application Controller Exception"""

    def __init__(self, message, response_code):
        self.message = message
        self.response_code = response_code


class RecordOwnershipException(ApplicationControllerException):
    """Raised when an request is sent for a record that does not belong to the authenticated user"""

    pass
