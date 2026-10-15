from dataclasses import dataclass

@dataclass
class Calcstate:
    angle: str = "rad"
    precision: int = 9
    format: str = "dec"

state = Calcstate()