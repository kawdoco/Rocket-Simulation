import numpy as np


class Atmosphere:
   

    def __init__(self, sea_level_density: float = 1.225, scale_height: float = 8500):
        self.__sea_level_density = sea_level_density  
        self.__scale_height = scale_height             

    def density(self, altitude: float) -> float:
   
        return self.__sea_level_density * np.exp(-altitude / self.__scale_height)

    def gravity(self, altitude: float) -> float:
     
        return 9.81

class MarsAtmosphere(Atmosphere):


    def __init__(self):
        super().__init__(sea_level_density=0.020, scale_height=11100)

    def gravity(self, altitude: float) -> float:
        return 3.71