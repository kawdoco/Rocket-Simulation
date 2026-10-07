from tkinter import ttk


class BaseScreen(ttk.Frame):
  

    def __init__(self, parent):
       
        super().__init__(parent)
        self.configure(style="Space.TFrame")

    def _build_ui(self):
    
        raise NotImplementedError("Each screen must build its own UI")