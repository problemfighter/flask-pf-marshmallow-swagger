from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse


class PfMsException(Exception):
    messageResponse: MessageResponse = None
    errorResponse: ErrorResponse = None
    message: str = None

    def __init__(self, message: str = None, messageResponse: MessageResponse = None, errorResponse: ErrorResponse = None):
        self.message = message
        self.errorResponse = errorResponse
        self.messageResponse = messageResponse
        super().__init__(message)
