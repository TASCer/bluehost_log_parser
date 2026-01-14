import pytest
from pathlib import Path

SAMPLE_LOG = Path(__file__).parent / "misc" / "sample_unzipped_logfile"

@pytest.fixture(scope="session")
def test_fetch_logs() -> list:
    print(SAMPLE_LOG.parts)
    print(SAMPLE_LOG.parent)
    print(SAMPLE_LOG.parent.parent.parent)
    with SAMPLE_LOG.open() as fh:
        logs = fh.readlines()
    # print(logs)
    return logs
