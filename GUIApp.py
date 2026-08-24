import tkinter as tk
from tkinter import ttk

from Rocket import Rocket, PRESETS
from RocketSimulator import RocketSimulator
from SelectionScreen import SelectionScreen
from SimulationScreen import SimulationScreen


class App:
    """
    Top-level controller. Owns ONE persistent Tk root and swaps between
    SelectionScreen and SimulationScreen inside it.

    Why this matters: the earlier "runs once, then crashes on the next
    launch" bug came from re-creating Tk()/animation objects without
    cleaning up the old ones. Here there is only ever one Tk() root for the
    whole program, each screen is a disposable Frame, and any running
    animation is explicitly stopped before its screen is destroyed.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rocket Flight Simulator")
        self.root.geometry("1300x800")
        self.root.minsize(1000, 650)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.current_screen = None
        self.show_selection()

    def _clear_screen(self):
        if self.current_screen is not None:
            # If the simulation screen is up, make sure its animation is
            # stopped before the frame (and its figures) get destroyed.
            go_back = getattr(self.current_screen, "_go_back", None)
            if go_back is not None and getattr(self.current_screen, "anim", None) is not None:
                self.current_screen.anim.event_source.stop()
                self.current_screen.anim = None
            self.current_screen.destroy()
            self.current_screen = None

    def show_selection(self):
        self._clear_screen()
        self.current_screen = SelectionScreen(self.root, on_launch=self._launch)
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def _launch(self, preset_key, angle):
        preset = PRESETS[preset_key]
        rocket = Rocket(preset)
        simulator = RocketSimulator(rocket)
        results = simulator.simulate(launch_angle=angle, duration=rocket.sim_duration)

        self._clear_screen()
        self.current_screen = SimulationScreen(
            self.root, rocket, results, on_back=self.show_selection
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()


def run_app():
    App().run()
