import sys
from PySide6.QtCore import QThread

# from CommonFunc.print_debug import print_debug


class ThreadWithTrace(QThread):

    def __init__(self, function, parent=None):
        super(ThreadWithTrace, self).__init__(parent)
        self.killed = False
        self.function = function
        
        
    def run(self):
        sys.settrace(self.globaltrace)
        self.function()
        sys.settrace(None)
        

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
