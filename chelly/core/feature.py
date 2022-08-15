class Feature(object):
    def __init__(self, editor):
        self.__editor:object = editor
    
    @property
    def editor(self) -> object:
        return self.__editor
    
