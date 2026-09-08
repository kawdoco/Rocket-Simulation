import numpy as np
from matplotlib.patches import Polygon


class RocketSprite:
    """
    Draws a small rocket icon (nose cone + body + fins + engine flame) on a
    matplotlib Axes, and rotates/moves it to follow the flight path.

    Keeping this in its own class (separate from the simulation window) is
    an OOP composition example: SimulationScreen "has a" RocketSprite, it
    doesn't need to know how the rocket is drawn — only that it can be
    updated with a new position/heading each frame.
    """

    # Silhouette in local coordinates, nose pointing along +Y, centred at origin.
    _BODY = np.array([
        [0.00, 1.00],   # nose tip
        [0.18, 0.55],   # right shoulder
        [0.18, -0.35],  # right body edge
        [0.32, -0.55],  # right fin tip
        [0.12, -0.35],  # right fin inner
        [0.00, -0.55],  # engine base (centre)
        [-0.12, -0.35], # left fin inner
        [-0.32, -0.55], # left fin tip
        [-0.18, -0.35], # left body edge
        [-0.18, 0.55],  # left shoulder
    ])

    _FLAME = np.array([
        [0.10, -0.55],
        [0.00, -1.05],
        [-0.10, -0.55],
    ])

    def __init__(self, ax, body_color="#d8d8d8", nose_color="#c0392b"):
        self.ax = ax
        self.scale = 1.0

        self.body_patch = Polygon(self._BODY, closed=True,
                                   facecolor=body_color, edgecolor="black",
                                   linewidth=1.0, zorder=5)
        self.flame_patch = Polygon(self._FLAME, closed=True,
                                    facecolor="#ff8c00", edgecolor="none",
                                    zorder=4, visible=False)
        ax.add_patch(self.body_patch)
        ax.add_patch(self.flame_patch)

    def set_scale(self, scale):
        """Rocket icon size in data units (call this after axis limits are known)."""
        self.scale = max(scale, 1e-6)

    @staticmethod
    def _transform(points, angle_deg, tx, ty):
        theta = np.radians(angle_deg)
        rot = np.array([[np.cos(theta), -np.sin(theta)],
                         [np.sin(theta), np.cos(theta)]])
        return points @ rot.T + np.array([tx, ty])

    def update(self, x, y, vx, vy, engine_on):
        """Move + rotate the sprite so its nose points along the velocity vector."""
        speed = abs(vx) + abs(vy)
        heading = np.degrees(np.arctan2(vx, vy)) if speed > 1e-6 else 0.0

        body_pts = self._transform(self._BODY * self.scale, -heading, x, y)
        self.body_patch.set_xy(body_pts)

        if engine_on:
            flame_pts = self._transform(self._FLAME * self.scale, -heading, x, y)
            self.flame_patch.set_xy(flame_pts)
            self.flame_patch.set_visible(True)
        else:
            self.flame_patch.set_visible(False)

    def artists(self):
        return [self.body_patch, self.flame_patch]
