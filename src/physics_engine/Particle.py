from pyglm import glm


class Particle:
    def __init__(self, position: glm.vec3, mass: float):
        assert mass > glm.epsilon()

        self.position = position
        self.velocity = glm.vec3(0)
        self._inv_mass = 1 / glm.clamp(mass, 0.0001, 1000)
        self.accum_force = glm.vec3(0)

    @property
    def mass(self):
        return 1 / self._inv_mass

    @mass.setter
    def mass(self, mass: float):
        self._inv_mass = 1 / glm.clamp(mass, 0.0001, 1000)

    def add_force(self, force: glm.vec3):
        self.accum_force += force

    def update(self, dt: float):
        acceleration = self.accum_force * self._inv_mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        self.accum_force = glm.vec3(0)

    @property
    def direction(self) -> glm.vec3:
        speed = glm.length2(self.velocity)  # ty:ignore[no-matching-overload]
        if speed <= glm.epsilon():
            return glm.vec3(0)
        return glm.normalize(self.velocity)
