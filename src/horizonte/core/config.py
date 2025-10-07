from dataclasses import dataclass

a_DEFAULT_STEPS = 500

@dataclass
class SimConfig:
    n:int = 256              # nodos CML
    r:float = 3.9            # parámetro mapa logístico
    kappa:float = 0.15       # acoplamiento
    noise:float = 0.001
    steps:int = a_DEFAULT_STEPS
    seed:int = 42
    window:int = 100
