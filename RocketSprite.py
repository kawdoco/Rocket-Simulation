from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon


class RocketSprite:
    """
    Draws a small rocket icon (nose cone + body + fins + engine flame) on a
    matplotlib Axes and rotates it to face the current velocity vector.
    """

    # Local sprite geometry, nose points along +Y and origin is centered.
    _BODY = np.array(
        [
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
        ],
        dtype=float,
    )

    _FLAME = np.array(
        [
            [0.10, -0.55],
            [0.00, -1.05],
            [-0.10, -0.55],
        ],
        dtype=float,
    )

    def __init__(
        self,
        ax: Axes,
        body_color: str = "#d8d8d8",
        nose_color: str = "#c0392b",
    ) -> None:
        self.ax = ax
        self.scale = 1.0

        self.body_patch = Polygon(
            self._BODY,
            closed=True,
            facecolor=body_color,
            edgecolor="black",
            linewidth=1.0,
            zorder=5,
        )
        self.flame_patch = Polygon(
            self._FLAME,
            closed=True,
            facecolor="#ff8c00",
            edgecolor="none",
            zorder=4,
            visible=False,
        )
        ax.add_patch(self.body_patch)
        ax.add_patch(self.flame_patch)

        self.nose_color = nose_color
        self.body_color = body_color

    def set_scale(self, scale: float) -> None:
        """Rocket icon size in data units; call after axis limits are known."""
        if not np.isfinite(scale) or scale <= 0:
            raise ValueError("scale must be a positive finite number")
        self.scale = float(scale)

    @staticmethod
    def _transform(points: np.ndarray, angle_deg: float, tx: float, ty: float) -> np.ndarray:
        theta = np.radians(angle_deg)
        rotation = np.array(
            [
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)],
            ],
            dtype=float,
        )
        return points @ rotation.T + np.array([tx, ty], dtype=float)

    def update(self, x: float, y: float, vx: float, vy: float, engine_on: bool) -> None:
        """Move + rotate the sprite so its nose aligns with the velocity vector."""
        speed = np.hypot(vx, vy)

        if speed > 1e-6:
            # Nose begins at +Y in local coordinates and follows velocity direction.
            heading = np.degrees(np.arctan2(vx, vy))
        else:
            heading = 0.0

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