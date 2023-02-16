from qtpy.QtCore import QTimer


class GlobalUpdateWordSetTimer:
    """Timer updates word set, when editor is idle. (5 sec. after last change)
    Timer is global, for avoid situation, when all instances
    update set simultaneously
    """

    _IDLE_TIMEOUT_MS = 1000

    def __init__(self):
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._onTimer)
        self._scheduledMethods = []

    def schedule(self, method):
        if method not in self._scheduledMethods:
            self._scheduledMethods.append(method)
        self._timer.start(self._IDLE_TIMEOUT_MS)

    def cancel(self, method):
        """Cancel scheduled method
        Safe method, may be called with not-scheduled method"""
        if method in self._scheduledMethods:
            self._scheduledMethods.remove(method)

        if not self._scheduledMethods:
            self._timer.stop()

    def _onTimer(self):
        method = self._scheduledMethods.pop()
        method()
        if self._scheduledMethods:
            self._timer.start(self._IDLE_TIMEOUT_MS)


__all__ = ["GlobalUpdateWordSetTimer"]
