class TriageRequestFailedError(BaseException):
    """Triage responded with something other than a normal 200 response"""

    def __init__(self, status_code, message):
        super().__init__(self, status_code, message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"Call to Cofense Triage failed ({self.status_code}): {self.message}"
