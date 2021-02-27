from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse


class PfMsException(Exception):
    message_response: MessageResponse = None
    error_response: ErrorResponse = None
    message: str = None

    def __init__(self, message: str = None, message_response: MessageResponse = None, error_response: ErrorResponse = None):
        self.message = message
        self.message_response = message_response
        self.error_response = error_response
        super().__init__(message)
