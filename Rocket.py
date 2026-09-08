from abc import ABC, abstractmethod
import numpy as np

PRESETS = {
    1: {
        "name": "Student Rocket",
        "description": "Small amateur rocket, low thrust",
        "diameter": 0.1, "length": 1.2,
        "dry_mass": 8.0, "propellant_mass": 2.0,
        "cd": 0.45, "thrust": 400.0, "burn_time": 5.0, "isp": 160.0,
        "sim_duration": 60,
    },
    2: {
        "name": "Sport Rocket",
        "description": "Mid-size high-power rocket",
        "diameter": 0.15, "length": 2.0,
        "dry_mass": 40.0, "propellant_mass": 10.0,
        "cd": 0.35, "thrust": 1800.0, "burn_time": 8.0, "isp": 175.0,
        "sim_duration": 120,
    },
    3: {
        "name": "Heavy Rocket",
        "description": "Large rocket, high thrust, slow acceleration",
        "diameter": 1.0, "length": 2.5,
        "dry_mass": 100.0, "propellant_mass": 5.0,
        "cd": 0.4, "thrust": 3000.0, "burn_time": 10.0, "isp": 180.0,
        "sim_duration": 120,
    },
    4: {
        "name": "Racing Dart",
        "description": "Ultralight dart, minimal drag, extreme acceleration",
        "diameter": 0.05, "length": 0.8,
        "dry_mass": 3.0, "propellant_mass": 1.0,
        "cd": 0.2, "thrust": 250.0, "burn_time": 3.0, "isp": 150.0,
        "sim_duration": 40,
    },
}


# ---------- ABSTRACTION ----------
class Vehicle(ABC):
    """
    Abstract base class for anything that can fly in the simulation.

    RocketSimulator only needs to know that a Vehicle can report its
    mass and thrust at a given time — it doesn't need to know HOW
    that vehicle computes them. That's abstraction.
    """

    @abstractmethod
    def mass_at(self, t: float) -> float:
        """Return this vehicle's mass (kg) at time t (s)."""
        raise NotImplementedError

    @abstractmethod
    def thrust_at(self, t: float) -> float:
        """Return this vehicle's thrust (N) at time t (s)."""
        raise NotImplementedError


# ---------- INHERITANCE (Rocket inherits from Vehicle) ----------
class Rocket(Vehicle):
    def __init__(self, preset: dict = None):
        p = preset or PRESETS[3]

        # === ENCAPSULATION: private attributes, underscore prefix ===
        self._diameter = p["diameter"]
        self._length = p["length"]
        self._area = np.pi * (self._diameter / 2) ** 2

        self._dry_mass = p["dry_mass"]
        self._propellant_mass = p["propellant_mass"]
        self._total_mass = self._dry_mass + self._propellant_mass

        self._cd = p["cd"]

        self._thrust = p["thrust"]
        self._burn_time = p["burn_time"]
        self._isp = p["isp"]

        self._preset_name = p["name"]
        self._sim_duration = p["sim_duration"]

    # === ENCAPSULATION: controlled read-only access via properties ===
    # RocketSimulator still writes `rocket.thrust`, `rocket.cd`, etc. —
    # these just route that through a private attribute now.
    @property
    def diameter(self): return self._diameter

    @property
    def length(self): return self._length

    @property
    def area(self): return self._area

    @property
    def dry_mass(self): return self._dry_mass

    @property
    def propellant_mass(self): return self._propellant_mass

    @property
    def total_mass(self): return self._total_mass

    @property
    def cd(self): return self._cd

    @property
    def thrust(self): return self._thrust

    @property
    def burn_time(self): return self._burn_time

    @property
    def isp(self): return self._isp

    @property
    def preset_name(self): return self._preset_name

    @property
    def sim_duration(self): return self._sim_duration

    # === implements Vehicle's abstract methods ===
    def mass_at(self, t: float) -> float:
        if t > self._burn_time:
            return self._dry_mass
        mass_flow_rate = self._propellant_mass / self._burn_time
        fuel_burned = mass_flow_rate * t
        return self._total_mass - fuel_burned

    def thrust_at(self, t: float) -> float:
        if t <= self._burn_time:
            return self._thrust
        return 0.0

    def info(self):
        """Print rocket parameters"""
        print(f"\n=== ROCKET PARAMETERS: {self._preset_name} ===")
        print(f"Diameter:       {self._diameter} m")
        print(f"Length:         {self._length} m")
        print(f"Total mass:     {self._total_mass} kg")
        print(f"Thrust:         {self._thrust} N")
        print(f"Burn time:      {self._burn_time} s")
        print(f"Thrust/Weight:  {self._thrust / (self._total_mass * 9.81):.2f}")
        print("=" * (28 + len(self._preset_name)) + "\n")


# ---------- POLYMORPHISM (overrides thrust_at differently) ----------
class BoosterRocket(Rocket):
    """
    A rocket whose engine has an ignition delay before it fires.

    Inheritance: reuses everything from Rocket.
    Polymorphism: RocketSimulator calls thrust_at(t) the same way for
    any Vehicle — it doesn't need special-case code to know this is a
    BoosterRocket instead of a plain Rocket.
    """

    def __init__(self, preset: dict = None, ignition_delay: float = 1.0):
        super().__init__(preset)
        self._ignition_delay = ignition_delay

    def thrust_at(self, t: float) -> float:
        if self._ignition_delay <= t <= self._burn_time + self._ignition_delay:
            return self._thrust
        return 0.0