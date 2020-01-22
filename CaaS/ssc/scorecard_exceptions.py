class InvalidAPIKeyError(ValueError):
    pass


class ResourceNotFoundError(ValueError):
    pass


class NoDataError(ValueError):
    pass


class InvalidJSONError(ValueError):
    pass


class ServerError(ValueError):
    pass
