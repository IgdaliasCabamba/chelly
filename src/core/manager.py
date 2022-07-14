class Manager(object):
    def __init__(self, editor):
        self.__editor = editor
    
    @property
    def editor(self):
        return self.__editor
    
