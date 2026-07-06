from PySide6.QtCore import (
    QObject,
    Signal
)

from core.pac_reporting import full_process


class ReportWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(
        self,
        reports,
        pac_staff,
        exclude_minor
    ):
        super().__init__()

        self.reports = reports
        self.pac_staff = pac_staff
        self.exclude_minor = exclude_minor

    def run(self):

        try:

            dfs = full_process(
                reports=self.reports,
                pac_staff=self.pac_staff,
                exclude_minor_intervention=self.exclude_minor
            )

            self.finished.emit(dfs)

        except Exception as e:

            self.error.emit(str(e))