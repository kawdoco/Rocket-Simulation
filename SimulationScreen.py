import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Dark Space Plot Theme Configuration
plt.style.use('dark_background')


class SimulationScreen(ttk.Frame):
    """
    Advanced Space-Themed 3D Visualization Screen with fixed 3D view (no rotation)
    and enhanced visual glow/trail effects for maximum attraction.
    """

    def __init__(self, parent, rocket, results, on_back):
        super().__init__(parent)
        self.rocket = rocket
        self.results = results
        self._go_back = on_back
        self.anim = None

        self._build_ui()
        self._setup_space_dashboard()

    def _build_ui(self):
        self.configure(style="Space.TFrame")
        style = ttk.Style()
        style.configure("Space.TFrame", background="#0a0e1a")

        # Header Bar
        top_bar = tk.Frame(self, bg="#0a0e1a")
        top_bar.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)

        back_btn = tk.Button(
            top_bar,
            text="◄ ABORT / BACK",
            bg="#ff3366",
            fg="#ffffff",
            activebackground="#cc0033",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            command=self._handle_back,
            cursor="hand2"
        )
        back_btn.pack(side=tk.LEFT)

        rocket_name = getattr(self.rocket, 'name', getattr(self.rocket, 'preset_name', 'Orbital Rocket'))
        title = tk.Label(
            top_bar,
            text=f"MISSION LIVE TELEMETRY: {rocket_name.upper()}",
            bg="#0a0e1a",
            fg="#00f0ff",
            font=("Helvetica", 13, "bold")
        )
        title.pack(side=tk.LEFT, padx=20)

    def _setup_space_dashboard(self):
        # Create a dashboard grid layout
        self.fig = plt.Figure(figsize=(12, 6), facecolor="#0a0e1a")
        
        # 1. 3D Space Trajectory Plot (Left Subplot)
        self.ax3d = self.fig.add_subplot(121, projection='3d', facecolor="#0a0e1a")
        
        # Disable Mouse Interaction (Lock view position permanently - Static Camera Angle)
        self.ax3d.disable_mouse_rotation() 
        self.ax3d.view_init(elev=25, azim=-55) # Optimized fixed space perspective view

        # 2. Altitude Graph (Top Right Subplot)
        self.ax_alt = self.fig.add_subplot(222, facecolor="#121829")
        
        # 3. Velocity Graph (Bottom Right Subplot)
        self.ax_vel = self.fig.add_subplot(224, facecolor="#121829")

        self.fig.tight_layout(pad=3.0)

        # Canvas Integration
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Extract Telemetry Data
        time_data = self.results.get('time', self.results.get('t', []))
        x_data = self.results.get('x', [])
        y_data = self.results.get('y', [0] * len(x_data))
        z_data = self.results.get('z', self.results.get('altitude', []))
        vx_data = self.results.get('vx', [0] * len(x_data))
        vz_data = self.results.get('vz', [0] * len(x_data))
        vel_data = self.results.get('velocity', np.sqrt(np.array(vx_data)**2 + np.array(vz_data)**2))

        data_len = len(x_data) if x_data is not None else 0

        # Style 3D Space Scene
        self.ax3d.set_title("3D Space Flight Path (Fixed View)", color="#00f0ff", fontsize=11, fontweight="bold")
        self.ax3d.set_xlabel("X Distance (m)", color="#a0aabb", fontsize=8)
        self.ax3d.set_ylabel("Y Drift (m)", color="#a0aabb", fontsize=8)
        self.ax3d.set_zlabel("Z Altitude (m)", color="#a0aabb", fontsize=8)
        self.ax3d.tick_params(colors='#a0aabb', labelsize=8)

        # Add background grid design
        self.ax3d.xaxis.pane.set_edgecolor('#121829')
        self.ax3d.yaxis.pane.set_edgecolor('#121829')
        self.ax3d.zaxis.pane.set_edgecolor('#121829')
        self.ax3d.xaxis.pane.fill = False
        self.ax3d.yaxis.pane.fill = False
        self.ax3d.zaxis.pane.fill = False

        if data_len > 0:
            # Trajectory Trail Guide
            self.ax3d.plot(x_data, y_data, z_data, color="#00f0ff", linestyle=":", alpha=0.3, label="Planned Orbit")

        # Active Dynamic Trail (Glow tail effect behind rocket)
        (self.active_trail,) = self.ax3d.plot([], [], [], color="#ff00ff", linewidth=2.5, label="Flight Trail")
        
        # Glowing Rocket Marker
        (self.rocket_marker,) = self.ax3d.plot([], [], [], color="#ff3366", marker="o", markersize=9, label="Rocket Core")
        self.ax3d.legend(loc="upper left", facecolor="#0a0e1a", edgecolor="#121829", fontsize=8)

        # Telemetry Graphs Setup
        self.ax_alt.set_title("Altitude vs Time", color="#00f0ff", fontsize=10)
        self.ax_alt.set_ylabel("Altitude (m)", color="#a0aabb", fontsize=8)
        self.ax_alt.grid(True, color="#1a233a", linestyle=":")
        self.ax_alt.tick_params(colors='#a0aabb', labelsize=8)
        if data_len > 0 and len(time_data) == data_len:
            self.ax_alt.plot(time_data, z_data, color="#00ffcc", alpha=0.2)
        (self.alt_line,) = self.ax_alt.plot([], [], color="#00ffcc", linewidth=2)

        self.ax_vel.set_title("Velocity Magnitude vs Time", color="#00f0ff", fontsize=10)
        self.ax_vel.set_xlabel("Time (s)", color="#a0aabb", fontsize=8)
        self.ax_vel.set_ylabel("Velocity (m/s)", color="#a0aabb", fontsize=8)
        self.ax_vel.grid(True, color="#1a233a", linestyle=":")
        self.ax_vel.tick_params(colors='#a0aabb', labelsize=8)
        if data_len > 0 and len(time_data) == data_len:
            self.ax_vel.plot(time_data, vel_data, color="#ff9900", alpha=0.2)
        (self.vel_line,) = self.ax_vel.plot([], [], color="#ff9900", linewidth=2)

        # Live Animation Frame Callback
        def update(frame):
            if frame < data_len:
                # Update Rocket Marker
                self.rocket_marker.set_data([x_data[frame]], [y_data[frame]])
                self.rocket_marker.set_3d_properties([z_data[frame]])

                # Dynamic Trajectory Trail Glow
                self.active_trail.set_data(x_data[:frame], y_data[:frame])
                self.active_trail.set_3d_properties(z_data[:frame])

                # Update Graphs dynamically
                if len(time_data) == data_len:
                    self.alt_line.set_data(time_data[:frame], z_data[:frame])
                    self.vel_line.set_data(time_data[:frame], vel_data[:frame])

            return self.rocket_marker, self.active_trail, self.alt_line, self.vel_line

        if data_len > 0:
            self.anim = FuncAnimation(
                self.fig,
                update,
                frames=data_len,
                interval=25,
                blit=False
            )

    def _handle_back(self):
        """Clean up Matplotlib resources and safely transition back."""
        if self.anim and hasattr(self.anim, 'event_source') and self.anim.event_source:
            self.anim.event_source.stop()
            self.anim = None
        if callable(self._go_back):
            self._go_back()