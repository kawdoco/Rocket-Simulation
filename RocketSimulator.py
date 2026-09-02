import numpy as np
from scipy.integrate import odeint

from Rocket import Rocket
from Atmosphere import Atmosphere

class RocketSimulator:

    def __init__(self, rocket):
        """
        Initialize the simulator

        Parameters:
        ----------
        rocket : Rocket
            Rocket object to simulate
        """
        self.rocket = rocket
        self.atm = Atmosphere()

    def get_mass(self, t):
        """
        Calculates the current mass of the rocket accounting for propellant burnoff

        Parameters:
        ----------
        t : float
            Current time in seconds

        Returns:
        -----------
        mass : float
            Current mass in kg
        """
        # If propellant has already burned out
        if t > self.rocket.burn_time:
            return self.rocket.dry_mass

        # Propellant consumption rate (kg/s)
        mass_flow_rate = self.rocket.propellant_mass / self.rocket.burn_time

        # How much propellant has burned in time t
        fuel_burned = mass_flow_rate * t

        # Current mass = initial mass - burned propellant
        return self.rocket.total_mass - fuel_burned

    def get_thrust(self, t):
        """
        Returns engine thrust at time t

        Parameters:
        ----------
        t : float
            Current time in seconds

        Returns:
        -----------
        thrust : float
            Thrust in Newtons
        """
        if t <= self.rocket.burn_time:
            return self.rocket.thrust
        return 0.0  # Engine off

    def derivatives(self, state, t):
        """
        KEY FUNCTION: computes derivatives for the ODE system

        This is the heart of the simulator! Physics laws are applied here.

        Parameters:
        ----------
        state : array [x, y, vx, vy]
            x, y   - rocket coordinates (m)
            vx, vy - velocity components (m/s)
        t : float
            Current time (s)

        Returns:
        -----------
        derivatives : array [dx/dt, dy/dt, dvx/dt, dvy/dt]
            dx/dt = vx
            dy/dt = vy
            dvx/dt = ax (acceleration along x)
            dvy/dt = ay (acceleration along y)
        """
        # Unpack state
        x, y, vx, vy = state

        # NOTE: we deliberately do NOT freeze/stop the state here when y < 0.
        # odeint's adaptive solver internally probes points slightly below
        # (or above) the real trajectory while choosing its step size — a
        # probe can dip to y = -1e-9 even seconds before the rocket actually
        # lands. Returning [0, 0, 0, 0] at that instant creates an absorbing
        # state: once acceleration and velocity are forced to zero, they can
        # never become non-zero again, so the whole flight freezes at ~0m
        # altitude. simulate() already trims the results at the real landing
        # point afterwards, so no early cutoff is needed here — the physics
        # should just stay continuous.

        # === GET CURRENT PARAMETERS ===
        m = self.get_mass(t)        # Current mass
        thrust = self.get_thrust(t) # Current thrust
        g = self.atm.gravity(y)     # Gravitational acceleration
        rho = self.atm.density(y)   # Air density at altitude y

        # Total speed (magnitude of velocity vector)
        v = np.sqrt(vx ** 2 + vy ** 2)

        # === AERODYNAMIC DRAG CALCULATION ===
        # Formula: F_drag = 0.5 * ρ * v² * Cd * A
        # Directed AGAINST motion
        if v > 0.1:  # Avoid division by zero
            # Drag force magnitude
            drag_magnitude = 0.5 * rho * v ** 2 * self.rocket.cd * self.rocket.area

            # Projections onto axes (directed against velocity)
            drag_x = -drag_magnitude * (vx / v)
            drag_y = -drag_magnitude * (vy / v)
        else:
            drag_x = 0
            drag_y = 0

        # === THRUST FORCE CALCULATION ===
        # Bug fix: thrust must act along the rocket's fixed launch heading
        # (self._launch_angle_rad, set once in simulate()), NOT along the
        # instantaneous velocity vector. The old code re-derived the thrust
        # direction from (vx/v, vy/v) every step. Since the initial velocity
        # is tiny (0.1 m/s) and easily nudged sideways, any small horizontal
        # drift got amplified: more sideways velocity -> thrust points more
        # sideways -> even more sideways velocity, a positive-feedback
        # runaway. That is why non-90-degree launches were shooting almost
        # horizontally within a fraction of a second instead of climbing.
        # A fixed heading (a normal simplification for a first model) removes
        # this feedback loop entirely.
        if thrust > 0:
            thrust_x = thrust * np.cos(self._launch_angle_rad)
            thrust_y = thrust * np.sin(self._launch_angle_rad)
        else:
            thrust_x = 0
            thrust_y = 0

        # === NEWTON'S SECOND LAW: F = ma => a = F/m ===
        # Sum all forces and divide by mass
        ax = (thrust_x + drag_x) / m
        ay = (thrust_y + drag_y) / m - g  # Minus g because gravity pulls down

        # Return derivatives: [dx/dt, dy/dt, dvx/dt, dvy/dt]
        return [vx, vy, ax, ay]

    def simulate(self, launch_angle=90, duration=60):
        """
        Runs the flight simulation

        Parameters:
        ----------
        launch_angle : float
            Launch angle in degrees (90 = straight up)
        duration : float
            Simulation duration in seconds

        Returns:
        -----------
        results : dict
            Dictionary with simulation results
        """
        print(f"Starting simulation (angle: {launch_angle}°)...")

        # === INITIAL CONDITIONS ===
        angle_rad = np.radians(launch_angle)  # Convert degrees to radians
        self._launch_angle_rad = angle_rad    # fixed heading used by derivatives() for thrust direction

        x0 = 0.0  # Initial X coordinate
        y0 = 0.1  # Initial altitude (slightly above ground)
        vx0 = 0.1 * np.cos(angle_rad)  # Initial velocity along X
        vy0 = 0.1 * np.sin(angle_rad)  # Initial velocity along Y

        initial_state = [x0, y0, vx0, vy0]

        # === TIME GRID ===
        # Create 1000 points from 0 to duration seconds
        t = np.linspace(0, duration, 1000)

        # === SOLVE ODE SYSTEM ===
        # odeint solves the system of differential equations
        solution = odeint(self.derivatives, initial_state, t)

        # Extract results
        x = solution[:, 0]  # X coordinate
        y = solution[:, 1]  # Y coordinate (altitude)
        vx = solution[:, 2]  # Velocity along X
        vy = solution[:, 3]  # Velocity along Y

        # === TRIM RESULTS AFTER LANDING ===
        ground_indices = np.where(y < 0)[0]
        if len(ground_indices) > 0:
            landing_idx = ground_indices[0]
            t = t[:landing_idx]
            x = x[:landing_idx]
            y = y[:landing_idx]
            vx = vx[:landing_idx]
            vy = vy[:landing_idx]

        print("Simulation complete!")

        # Return results as a dictionary
        return {
            'time': t,
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'velocity': np.sqrt(vx ** 2 + vy ** 2),
            'altitude': y
        }
