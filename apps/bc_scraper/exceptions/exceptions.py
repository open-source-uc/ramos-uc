class EmptyResponseError(Exception):
    """Exception thrown when a request returned an empty response.

    Attributes:
        url -- The URL that returned an empty response.
    """

    def __init__(self, url, message="The request returned an empty response."):
        self.url = url
        self.message = message
        super().__init__(self.message)
