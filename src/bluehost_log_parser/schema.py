from pydantic import BaseModel, field_validator  # , IPvAnyAddress
from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3


class LogEntry(BaseModel):
    """
    Class represents a log entry from a webserver's logging system.

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

    @field_validator("AGENT", "REFERRER")
    def remove_btyes(cls, value: str) -> str:
        if value.startswith("b'"):
            value = value.replace("b'", "")
            if value[-1] == "'":
                value = value[:-2]
        return value

    @field_validator("CLIENT", "REQUEST")
    def remove_apostrophes(cls, value: str) -> str:
        return value.replace("'", "")

    @field_validator("REQUEST")
    def escape_colon(cls, value: str) -> str:
        if value.startswith("/:"):
            value = value.replace("/:", "")
            return value

        return value


class SourceEntry(BaseModel):
    """
    Class represents a log entry's source from a webserver's logging system.

    """

    SOURCE: str
    COUNTRY: str
    ALPHA2: CountryAlpha2
    ALPHA3: CountryAlpha3
    DESCRIPTION: str
