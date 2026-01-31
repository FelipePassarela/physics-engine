from typing import Iterable

from physics_engine.force.IForce import IForce
from physics_engine.Particle import Particle


class ParticleForceRegistry:
    _registry: dict[Particle, list[IForce]]

    def __init__(self):
        self._registry = {}

    def add(self, particle: Particle, forces: Iterable[IForce]):
        if particle not in self._registry:
            self._registry[particle] = list(forces)
        else:
            self._registry[particle].extend(forces)

    def remove(self, particle: Particle, force: IForce):
        if particle not in self._registry:
            return
        if force not in self._registry[particle]:
            return
        self._registry[particle].remove(force)

    def clear(self):
        self._registry.clear()

    def update(self, dt: float):
        for particle, forces in self._registry.items():
            for force in forces:
                force.update(particle, dt)
            particle.update(dt)

    def get_registry(self) -> Iterable[tuple[Particle, list[IForce]]]:
        return self._registry.items()
