from PySide6.QtWidgets import QFrame

class CompleterWidget(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor = parent
    
    def show_for(self, text):
        pass