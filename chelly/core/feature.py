class Feature(object):
    def __init__(self, editor):
        self.__editor:object = editor
        self.__enabled = True

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, status:bool) -> None:
        self.__enabled = status

    @property
    def editor(self) -> object:
        return self.__editor
    
