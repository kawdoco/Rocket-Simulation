import numpy as np
from scipy.integrate import odeint

from src.Rocket import Rocket
from src.Atmosphere import Atmosphere

class RocketSimulator:

    def __init__(self, rocket):
      
        self.rocket = rocket
        self.atm = Atmosphere()

    def get_mass(self, t):
       
        return self.rocket.mass_at(t)

    def get_thrust(self, t):
       
        return self.rocket.thrust_at(t)

    def derivatives(self, state, t):
       
        x, y, vx, vy = state
        
        m = self.get_mass(t)        
        thrust = self.get_thrust(t) 
        g = self.atm.gravity(y)    
        rho = self.atm.density(y)  

        
        v = np.sqrt(vx ** 2 + vy ** 2)

     
        if v > 0.1:  
            drag_magnitude = 0.5 * rho * v ** 2 * self.rocket.cd * self.rocket.area

           
            drag_x = -drag_magnitude * (vx / v)
            drag_y = -drag_magnitude * (vy / v)
        else:
            drag_x = 0
            drag_y = 0

        if thrust > 0:
            thrust_x = thrust * np.cos(self._launch_angle_rad)
            thrust_y = thrust * np.sin(self._launch_angle_rad)
        else:
            thrust_x = 0
            thrust_y = 0

      
        ax = (thrust_x + drag_x) / m
        ay = (thrust_y + drag_y) / m - g 

        
        return [vx, vy, ax, ay]

    def simulate(self, launch_angle=90, duration=60):
       
        print(f"Starting simulation (angle: {launch_angle}°)...")

    
        angle_rad = np.radians(launch_angle) 
        self._launch_angle_rad = angle_rad    

        x0 = 0.0  
        y0 = 0.1  
        vx0 = 0.1 * np.cos(angle_rad) 
        vy0 = 0.1 * np.sin(angle_rad) 

        initial_state = [x0, y0, vx0, vy0]

        t = np.linspace(0, duration, 1000)

        solution = odeint(self.derivatives, initial_state, t)

       
        x = solution[:, 0]  
        y = solution[:, 1] 
        vx = solution[:, 2] 
        vy = solution[:, 3] 

        ground_indices = np.where(y < 0)[0]
        if len(ground_indices) > 0:
            landing_idx = ground_indices[0]
            t = t[:landing_idx]
            x = x[:landing_idx]
            y = y[:landing_idx]
            vx = vx[:landing_idx]
            vy = vy[:landing_idx]

        print("Simulation complete!")

        return {
            'time': t,
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'velocity': np.sqrt(vx ** 2 + vy ** 2),
            'altitude': y
        }