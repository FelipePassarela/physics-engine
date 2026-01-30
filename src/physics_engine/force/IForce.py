from abc import ABC, abstractmethod

from physics_engine.Particle import Particle


class IForce(ABC):
    @abstractmethod
    def update(self, particle: Particle, dt: float):
        pass
