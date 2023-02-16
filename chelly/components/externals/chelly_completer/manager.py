from .base_widget import BaseCompletionWidget
from dataclasses import dataclass


class CompleterManager:
    @dataclass
    class CompletionWidgets:
        completion_list: BaseCompletionWidget = None
        completion_tooltip: BaseCompletionWidget = None

    def __init__(self, editor) -> None:
        self.__editor = editor
        self._widgets = CompleterManager.CompletionWidgets()

    @property
    def editor(self):
        return self.__editor

    @property
    def editor(self):
        return self.__editor

    def set_completion_list(
        self, completion_list_widget: BaseCompletionWidget, new: bool = False
    ) -> BaseCompletionWidget:
        if new:
            widget = completion_list_widget(self.editor)
            self._widgets.completion_list = widget
            return widget

        if self._widgets.completion_list is None:
            widget = completion_list_widget(self.editor)
            self._widgets.completion_list = widget
            return widget
        return self._widgets.completion_list

    def set_completion_tooltip(
        self, completion_widget: BaseCompletionWidget
    ) -> BaseCompletionWidget:
        widget = completion_widget(self.editor)
        self._widgets.completion_tooltip = widget
        return widget

    def update_geometry(self):
        ...


__all__ = ["CompleterManager"]
