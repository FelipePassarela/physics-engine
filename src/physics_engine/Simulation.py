import random as rd
import time

from pyglm import glm

from physics_engine.force.DragForce import DragForce
from physics_engine.force.GravityForce import GravityForce
from physics_engine.force.ParticleForceRegistry import ParticleForceRegistry
from physics_engine.force.SpringForce import SpringForce
from physics_engine.Particle import Particle


class Simulation:
    def __init__(self):
        self.registry: ParticleForceRegistry = ParticleForceRegistry()
        self.particles: list[Particle] = []
        self.SCALE = 60
        self._last_time = time.time()  # to calculate delta time

        self._setup_particles()

    def _setup_particles(self):
        for _ in range(2):
            position = glm.vec3(
                self.SCALE * rd.random(),
                self.SCALE * rd.random(),
                self.SCALE * rd.random(),
            )
            mass = 10 * self.SCALE * rd.random()
            particle = Particle(position=position, mass=mass)
            self.particles.append(particle)

        for particle in self.particles:
            other = (
                self.particles[1]
                if particle is self.particles[0]
                else self.particles[0]
            )
            forces = [
                GravityForce(gravity=glm.vec3(0, -20, 0)),
                DragForce(k1=0.1, k2=0.01),
                SpringForce(other=other, k=100, rest_length=3),
            ]
            self.registry.add(particle=particle, forces=forces)

    def update(self):
        now = time.time()
        dt = now - self._last_time
        self._last_time = now

        self.registry.update(dt)
        self.handle_collision()

    def handle_collision(self):
        for particle, _ in self.registry.get_registry():
            for axis in range(len(particle.position)):
                # TODO: Make box constraint by walls with infinite mass
                if particle.position[axis] < 0:
                    particle.position[axis] = 0
                    particle.velocity[axis] *= -1
                if particle.position[axis] > self.SCALE - 1:
                    particle.position[axis] = self.SCALE - 1
                    particle.velocity[axis] *= -1
