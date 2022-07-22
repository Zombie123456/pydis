class PydisError(Exception):
    detail = 'An internal error occurred'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail

    def __str__(self):
        return str(self.detail)


class NotFound(PydisError):
    detail = 'Key : `%s` does not exists.'

    def __init__(self, key):
        self.detail = self.detail % key


class ExpiredError(NotFound):
    detail = 'Key : `%s` already expired and deleted.'
