import tkinter as tk
from tkinter import ttk, messagebox
import logging

from Rocket import Rocket, PRESETS
from RocketSimulator import RocketSimulator
from SelectionScreen import SelectionScreen
from SimulationScreen import SimulationScreen

logging.basicConfig(level=logging.INFO)


class App:
    """
    Space Flight Controller App - Core Navigation & Lifecycle Manager.
    Uses Encapsulation to safely transition between space UI screens.
    """

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Space Rocket Simulator - Mission Control")
        self._root.geometry("1300x800")
        self._root.minsize(1050, 700)
        self._root.configure(bg="#0a0e1a")

        self._current_screen = None
        self.show_selection()

    def _clear_screen(self):
        """Stop Matplotlib animations and clean up existing UI screens."""
        if self._current_screen is not None:
            anim = getattr(self._current_screen, "anim", None)
            if anim is not None and hasattr(anim, "event_source") and anim.event_source:
                anim.event_source.stop()
                self._current_screen.anim = None

            self._current_screen.destroy()
            self._current_screen = None

    def show_selection(self):
        """Display Space Selection Screen."""
        self._clear_screen()
        self._current_screen = SelectionScreen(self._root, on_launch=self._launch)
        self._current_screen.pack(fill=tk.BOTH, expand=True)

    def _launch(self, preset_key: str, angle: float):
        """Run math simulation and render 3D space flight screen."""
        try:
            preset = PRESETS[preset_key]
            rocket = Rocket(preset)
            simulator = RocketSimulator(rocket)

            results = simulator.simulate(
                launch_angle=angle,
                duration=rocket.sim_duration
            )

            self._clear_screen()
            self._current_screen = SimulationScreen(
                self._root,
                rocket=rocket,
                results=results,
                on_back=self.show_selection
            )
            self._current_screen.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            logging.error(f"Launch simulation error: {e}")
            messagebox.showerror("Mission Error", f"Simulation failed: {str(e)}")

    def run(self):
        self._root.mainloop()


def run_app():
    App().run()