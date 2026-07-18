from datetime import datetime

import pytest

from models.raw_log import RawLog


@pytest.fixture
def make_log():
    def _make_log(message: str):
        return RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message=message,
        )

    return _make_log