from pyglm import glm

from physics_engine.force.IForce import IForce
from physics_engine.Particle import Particle


class GravityForce(IForce):
    def __init__(self, gravity: glm.vec3):
        self.gravity = gravity

    def update(self, particle: Particle, dt: float):
        particle.accum_force += self.gravity * particle.mass
