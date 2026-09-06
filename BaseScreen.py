from tkinter import ttk

class BaseScreen(ttk.Frame):
    """
    This is the shared 'parent' for all our screens.
    Like 'Animal' is the parent of Duck and Dog.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="Space.TFrame")

    def _build_ui(self):
        raise NotImplementedError("Each screen must build its own UI")