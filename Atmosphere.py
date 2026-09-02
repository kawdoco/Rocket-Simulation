import numpy as np

class Atmosphere:

    @staticmethod
    def density(altitude):
        """
        Calculates air density at a given altitude

        Parameters:
        ----------
        altitude : float
            Altitude above sea level in meters

        Returns:
        -----------
        rho : float
            Air density in kg/m³

        Formula: ρ(h) = ρ₀ * e^(-h/H)
        where ρ₀ - sea level density
              H  - atmospheric scale height
        """
        rho0 = 1.225  # Sea level density, kg/m³
        H = 8500  # Atmospheric scale height, m

        return rho0 * np.exp(-altitude / H)

    @staticmethod
    def gravity(altitude):
        """
        Gravitational acceleration

        For student rockets (altitudes up to 10 km) can be treated as constant
        """
        return 9.81  # m/s²
