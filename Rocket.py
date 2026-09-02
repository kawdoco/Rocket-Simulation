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


class Rocket:
    def __init__(self, preset: dict = None):
        p = preset or PRESETS[3]

        # === GEOMETRY ===
        self.diameter = p["diameter"]
        self.length = p["length"]
        self.area = np.pi * (self.diameter / 2) ** 2

        # === MASSES ===
        self.dry_mass = p["dry_mass"]
        self.propellant_mass = p["propellant_mass"]
        self.total_mass = self.dry_mass + self.propellant_mass

        # === AERODYNAMICS ===
        self.cd = p["cd"]

        # === ENGINE ===
        self.thrust = p["thrust"]
        self.burn_time = p["burn_time"]
        self.isp = p["isp"]

        self.preset_name = p["name"]
        self.sim_duration = p["sim_duration"]

    def info(self):
        """Print rocket parameters"""
        print(f"\n=== ROCKET PARAMETERS: {self.preset_name} ===")
        print(f"Diameter:       {self.diameter} m")
        print(f"Length:         {self.length} m")
        print(f"Total mass:     {self.total_mass} kg")
        print(f"Thrust:         {self.thrust} N")
        print(f"Burn time:      {self.burn_time} s")
        print(f"Thrust/Weight:  {self.thrust / (self.total_mass * 9.81):.2f}")
        print("=" * (28 + len(self.preset_name)) + "\n")
