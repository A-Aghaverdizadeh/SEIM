from datetime import datetime
from unittest.mock import MagicMock, patch

from collectors.journal import JournalCollector
from models.raw_log import RawLog


class TestJournalCollector:

    @patch("collectors.journal.journal.Reader")
    def test_collect_returns_raw_logs(self, mock_reader):

        fake_reader = MagicMock()

        fake_reader.__iter__.return_value = [
            {
                "__REALTIME_TIMESTAMP": datetime.now(),
                "_HOSTNAME": "debian",
                "SYSLOG_IDENTIFIER": "sshd",
                "MESSAGE": "Failed password for linuxguy from 127.0.0.1 port 22 ssh2",
            }
        ]

        mock_reader.return_value = fake_reader

        collector = JournalCollector()

        logs = list(collector.collect())

        assert len(logs) == 1
        assert isinstance(logs[0], RawLog)
        assert logs[0].hostname == "debian"
        assert logs[0].identifier == "sshd"