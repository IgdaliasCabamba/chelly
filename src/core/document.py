class ChellyDocument(object):
    def __init__(self, editor):
        self.__editors = [editor]
        self.bind()
    
    def bind(self):
        for editor in self.__editors:
            editor.on_updated.connect(lambda: self.update(editor))
    
    def add_editor(self, new_editor):
        self.__editors.append(new_editor)
        self.update(new_editor)
        self.bind()
    
    def update(self, origin_editor):
        for editor in self.__editors:
            if editor is not origin_editor:
                editor.properties.document = origin_editor.properties.document
                editor.language.lexer = origin_editor.language.lexer
            else:
                print("HEYO")