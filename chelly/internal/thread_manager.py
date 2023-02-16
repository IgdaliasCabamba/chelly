from threading import Lock, Thread
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QThread


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class ChellyQThreadManager(metaclass=SingletonMeta):
    __slots__ = ("__qapp", "__qthreads")

    def __init__(self, qapp: QApplication = None) -> None:
        if not isinstance(qapp, QApplication):
            raise TypeError(f"ChellyQThreadManager requires an {QApplication} instance")

        self.__qapp = qapp
        self.__qthreads = []
        self.__qapp.aboutToQuit.connect(lambda: self.__kill__())
        self.__qapp.lastWindowClosed.connect(lambda: self.__kill__())

    def append(self, qthread: QThread) -> None:
        if isinstance(qthread, QThread):
            if qthread in self.__qthreads:
                return None

            self.__qthreads.append(qthread)

    def remove(self, qthread: QThread) -> None:
        if qthread not in self.__qthreads:
            return None

        self.__qthreads.remove(qthread)

    def __kill__(self):
        deleted_threads = []
        for qthread in self.__qthreads:
            if qthread not in deleted_threads:
                qthread.quit()
                # qthread.terminate()
                qthread.wait()
                qthread.deleteLater()
            deleted_threads.append(qthread)

        self.__qthreads.clear()


__all__ = ["ChellyQThreadManager", "SingletonMeta"]
