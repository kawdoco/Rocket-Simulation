from tkinter import ttk


class BaseScreen(ttk.Frame):
    """
    Abstract parent class shared by all screens in the simulator.

    OOP concepts shown here:
    - Inheritance:   SelectionScreen and SimulationScreen inherit from this
                     class, so they share the same setup.
    - Abstraction:   _build_ui() is only declared here. Each child screen
                     must provide its own version.
    - Polymorphism:  every screen has a _build_ui() method, but each one
                     draws something different.
    """

    def __init__(self, parent):
        # Shared setup that every screen needs (inherited from ttk.Frame)
        super().__init__(parent)
        self.configure(style="Space.TFrame")

    def _build_ui(self):
        # Abstract method: child screens must override this one.
        raise NotImplementedError("Each screen must build its own UI")