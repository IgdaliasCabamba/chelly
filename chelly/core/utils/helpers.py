from typing import Any, Tuple, Type
from typing_extensions import Self
import weakref
from qtpy.QtCore import QTimer

class ChellyEvent:
    
    class TypeError(Exception):
        ...

    def __init__(self, *emit_types:Tuple[Type]) -> None:
        self.__emit_types = emit_types
        self.__event_handlers = []
    
    def connect(self, callable_object:object) -> Self:
        if callable(callable_object):
            self.__event_handlers.append(callable_object)
        return self
    
    def disconnect(self, callable_object:object) -> Self:
        if callable_object in self.__event_handlers:
            self.__event_handlers.remove(callable_object)
        return self
    
    def emit(self, *callable_objects:Tuple[Any]) -> Self:
        for i in range(len(callable_objects)):
            if not isinstance(callable_objects[i], self.__emit_types[i]):
                raise ChellyEvent.TypeError(f"Expected: {self.__emit_types[i]}, Got: {type(callable_objects[i])}")

        for handler in self.__event_handlers:
            handler(*callable_objects)
        
        return self

class DelayJobRunner:
    """
    Utility class for running job after a certain delay. If a new request is
    made during this delay, the previous request is dropped and the timer is
    restarted for the new request.
    We use this to implement a cooldown effect that prevents jobs from being
    executed while the IDE is not idle.
    A job is a simple callable.
    """

    def __init__(self, delay=500):
        """
        :param delay: Delay to wait before running the job. This delay applies
        to all requests and cannot be changed afterwards.
        """
        self._timer = QTimer()
        self.delay = delay
        self._timer.timeout.connect(self._exec_requested_job)
        self._args = []
        self._kwargs = {}
        self._job = lambda x: None

    def request_job(self, job, *args, **kwargs):
        """
        Request a job execution. The job will be executed after the delay
        specified in the DelayJobRunner contructor elapsed if no other job is
        requested until then.
        :param job: job.
        :type job: callable
        :param args: job's position arguments
        :param kwargs: job's keyworded arguments
        """
        self.cancel_requests()
        self._job = job
        self._args = args
        self._kwargs = kwargs
        self._timer.start(self.delay)

    def cancel_requests(self):
        """
        Cancels pending requests.
        """
        self._timer.stop()
        self._job = None
        self._args = None
        self._kwargs = None

    def _exec_requested_job(self):
        """
        Execute the requested job after the timer has timeout.
        """
        self._timer.stop()
        self._job(*self._args, **self._kwargs)

class TextBlockHelper:
    """
    Helps retrieving the various part of the user state bitmask.
    This helper should be used to replace calls to
    ``QTextBlock.setUserState``/``QTextBlock.getUserState`` as well as
    ``QSyntaxHighlighter.setCurrentBlockState``/
    ``QSyntaxHighlighter.currentBlockState`` and
    ``QSyntaxHighlighter.previousBlockState``.
    The bitmask is made up of the following fields:
        - bit0 -> bit26: User state (for syntax highlighting)
        - bit26: fold trigger state
        - bit27-bit29: fold level (8 level max)
        - bit30: fold trigger flag
        - bit0 -> bit15: 16 bits for syntax highlighter user state (
          for syntax highlighting)
        - bit16-bit25: 10 bits for the fold level (1024 levels)
        - bit26: 1 bit for the fold trigger flag (trigger or not trigger)
        - bit27: 1 bit for the fold trigger state (expanded/collapsed)
    """
    @staticmethod
    def get_state(block):
        """
        Gets the user state, generally used for syntax highlighting.
        :param block: block to access
        :return: The block state
        """
        if block is None:
            return -1
        state = block.userState()
        if state == -1:
            return state
        return state & 0x0000FFFF

    @staticmethod
    def set_state(block, state):
        """
        Sets the user state, generally used for syntax highlighting.
        :param block: block to modify
        :param state: new state value.
        :return:
        """
        if block is None:
            return
        user_state = block.userState()
        if user_state == -1:
            user_state = 0
        higher_part = user_state & 0x7FFF0000
        state &= 0x0000FFFF
        state |= higher_part
        block.setUserState(state)

    @staticmethod
    def get_fold_lvl(block):
        """
        Gets the block fold level
        :param block: block to access.
        :returns: The block fold level
        """
        if block is None:
            return 0
        state = block.userState()
        if state == -1:
            state = 0
        return (state & 0x03FF0000) >> 16

    @staticmethod
    def set_fold_lvl(block, val):
        """
        Sets the block fold level.
        :param block: block to modify
        :param val: The new fold level [0-7]
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        if val >= 0x3FF:
            val = 0x3FF
        state &= 0x7C00FFFF
        state |= val << 16
        block.setUserState(state)

    @staticmethod
    def is_fold_trigger(block):
        """
        Checks if the block is a fold trigger.
        :param block: block to check
        :return: True if the block is a fold trigger (represented as a node in
            the fold panel)
        """
        if block is None:
            return False
        state = block.userState()
        if state == -1:
            state = 0
        return bool(state & 0x04000000)

    @staticmethod
    def set_fold_trigger(block, val):
        """
        Set the block fold trigger flag (True means the block is a fold
        trigger).
        :param block: block to set
        :param val: value to set
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        state &= 0x7BFFFFFF
        state |= int(val) << 26
        block.setUserState(state)

    @staticmethod
    def is_collapsed(block):
        """
        Checks if the block is expanded or collased.
        :param block: QTextBlock
        :return: False for an open trigger, True for for closed trigger
        """
        if block is None:
            return False
        state = block.userState()
        if state == -1:
            state = 0
        return bool(state & 0x08000000)

    @staticmethod
    def set_collapsed(block, val):
        """
        Sets the fold trigger state (collapsed or expanded).
        :param block: The block to modify
        :param val: The new trigger state (True=collapsed, False=expanded)
        """
        if block is None:
            return
        state = block.userState()
        if state == -1:
            state = 0
        state &= 0x77FFFFFF
        state |= int(val) << 27
        block.setUserState(state)