import numpy as np


class Atmosphere:
    """
    Represents a planet's atmosphere and encapsulates the physics
    formulas used to compute air density and gravity at altitude.
    """

    def __init__(self, sea_level_density: float = 1.225, scale_height: float = 8500):
        self.__sea_level_density = sea_level_density  # kg/m^3, private
        self.__scale_height = scale_height             # m, private

    def density(self, altitude: float) -> float:
        """
        ρ(h) = ρ₀ * e^(-h/H)
        where ρ₀ - sea level density, H - atmospheric scale height
        """
        return self.__sea_level_density * np.exp(-altitude / self.__scale_height)

    def gravity(self, altitude: float) -> float:
        """For altitudes up to ~10 km, gravity can be treated as constant."""
        return 9.81


# ---------- INHERITANCE + POLYMORPHISM (bonus example) ----------
class MarsAtmosphere(Atmosphere):
    """
    Same interface as Atmosphere (density, gravity), different
    physical constants — demonstrates a Vehicle-style simulator
    could run on Mars just by swapping this in.
    """

    def __init__(self):
        super().__init__(sea_level_density=0.020, scale_height=11100)

    def gravity(self, altitude: float) -> float:
        return 3.71