from pyglm import glm

from physics_engine.force.IForce import IForce
from physics_engine.Particle import Particle


class SpringForce(IForce):
    def __init__(self, other: Particle, k: float, rest_length: float):
        self.other = other
        self.k = k
        self.rest_length = rest_length

    def update(self, particle: Particle, dt: float):
        displacement = self.other.position - particle.position
        distance = glm.length(displacement)
        if distance <= glm.epsilon():
            return
        direction = glm.normalize(displacement)
        force = self.k * (distance - self.rest_length) * direction

        particle.add_force(force)
        self.other.add_force(-force)
