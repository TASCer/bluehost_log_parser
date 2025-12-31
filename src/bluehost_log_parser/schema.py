from typing import Any
from pydantic import BaseModel, field_validator, IPvAnyAddress
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

    @field_validator("CLIENT")
    def remove_apostrophes(cls, value: str) -> str:
        return value.replace("'", "")

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

    # @field_validator('SOURCE', mode='before')
    # @classmethod
    # def extract_ip_from_string(cls, value: Any) -> str:
    #     """
    #     Validator to extract the IP address from the 'raw_input' field
    #     using a regex capture group.
    #     """
    #     if isinstance(value, IPvAnyAddress):
    #         return str(value)

    #     # raw_string = info.data.get('raw_input')
    #     else:
    #         raise ValueError("raw_input field is missing")
