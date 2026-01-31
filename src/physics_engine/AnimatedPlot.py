from collections.abc import Callable
from pathlib import Path

from matplotlib import animation
from matplotlib import pyplot as plt
from pyglm import glm


class AnimatedPlot:
    def __init__(
        self, update_func: Callable, nframes: int, interval: int = 50, scale: int = 1
    ):
        self.nframes = nframes
        self.interval = interval
        self.scale = scale
        self.func = update_func

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.scat = self.ax.scatter(0, 0, 0)

        self.ax.set_xlim(0, scale)
        self.ax.set_ylim(0, scale)
        self.ax.set_zlim(0, scale)
        # Matplotlib axis convention differs from OpenGL, so map to OpenGL.
        self.ax.set_xlabel(r"$Z$")
        self.ax.set_ylabel(r"$X$")
        self.ax.set_zlabel(r"$Y$")

        self.anim = animation.FuncAnimation(
            self.fig,
            self._update,
            frames=self.nframes,
            interval=self.interval,
            blit=False,
            repeat=True,
        )

    def _update(self, frame: int) -> tuple:
        data: list[dict[str, glm.vec3]] = self.func()
        self.scat._offsets3d = (
            [d["point"].z for d in data],
            [d["point"].x for d in data],
            [d["point"].y for d in data],
        )
        return (self.scat,)

    def show(self):
        plt.show()

    def save_gif(self, filename: Path | str):
        self.anim.save(filename, writer="pillow", fps=int(1000 / self.interval))
