from pyglm import glm

from physics_engine.force.IForce import IForce
from physics_engine.Particle import Particle


class DragForce(IForce):
    def __init__(self, k1: float, k2: float):
        self.k1 = k1
        self.k2 = k2

    def update(self, particle: Particle, dt: float):
        speed = glm.length(particle.velocity)
        if speed < glm.epsilon():
            return

        direction = particle.velocity / speed
        # simplistic model of drag
        drag_force = -direction * (self.k1 * speed + self.k2 * speed**2)
        particle.add_force(drag_force)
