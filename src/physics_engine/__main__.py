import random
from functools import partial

from pyglm import glm

from physics_engine.AnimatedPlot import AnimatedPlot
from physics_engine.force.DragForce import DragForce
from physics_engine.force.GravityForce import GravityForce
from physics_engine.Particle import Particle
from physics_engine.ParticleForceRegistry import ParticleForceRegistry


def update(
    registry: ParticleForceRegistry, size: int, dt: float
) -> list[dict[str, glm.vec3]]:
    registry.update(dt)
    plot_data = []

    for particle, _ in registry.get_registry():
        for axis in range(len(particle.position)):
            if particle.position[axis] < 0:
                particle.position[axis] = 0
                particle.velocity[axis] *= -1
            if particle.position[axis] > size - 1:
                particle.position[axis] = size - 1
                particle.velocity[axis] *= -1

        plot_data.append({"position": particle.position})

    return plot_data


def main() -> None:
    SIZE = 60
    DELTA_TIME = 0.05
    N_PARTICLES = 100

    registry = ParticleForceRegistry()
    for _ in range(N_PARTICLES):
        position = glm.vec3(
            SIZE * random.random(), SIZE * random.random(), SIZE * random.random()
        )
        mass = 1000 * random.random()
        forces = [
            GravityForce(gravity=glm.vec3(0, -20, 0)),
            DragForce(k1=0.1, k2=0.01),
        ]
        registry.add(particle=Particle(position, mass), forces=forces)

    anim = AnimatedPlot(
        partial(update, registry=registry, size=SIZE, dt=DELTA_TIME),
        nframes=60,
        scale=SIZE,
        interval=int(DELTA_TIME * 1000),
    )
    anim.show()


if __name__ == "__main__":
    main()
