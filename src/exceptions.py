"""Custom exceptions for the poster evaluation system"""


class OpenAIAPIError(Exception):
    """Exception raised when OpenAI API fails.
    
    This includes authentication failures, rate limiting, timeouts,
    and other critical API errors that should stop evaluation.
    """
    pass
