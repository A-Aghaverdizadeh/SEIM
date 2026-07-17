from systemd import journal

from models.raw_log import RawLog
from .base import BaseCollector


class JournalCollector(BaseCollector):

    def collect(self):

        reader = journal.Reader()

        reader.this_boot()

        reader.add_match(_SYSTEMD_UNIT="ssh.service")

        for entry in reader:

            yield RawLog(
                timestamp=entry["__REALTIME_TIMESTAMP"],
                hostname=entry["_HOSTNAME"],
                identifier=entry["SYSLOG_IDENTIFIER"],
                message=entry["MESSAGE"],
            )