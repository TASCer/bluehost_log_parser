from typing import NamedTuple


class LogEntry(NamedTuple):
    """
    Class represents a log entry from a webserver's logging system.

    :param NamedTuple:
    """

    server_timestamp: str
    SOURCE: str
    CLIENT: str
    AGENT: str
    METHOD: str
    REQUEST: str
    RESPONSE: str
    SIZE: str
    REFERRER: str
    HTTP: str
    SITE: str
