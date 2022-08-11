class ChellyDocument(object):
    def __init__(self, editor):
        self.__editor = editor
        
    def mirror(self, target_editor):
        target_editor.setDocument(self.__editor.document())