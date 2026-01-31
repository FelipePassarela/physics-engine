from collections.abc import Callable
from pathlib import Path

from matplotlib import animation
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
        self.ax: Axes3D = self.fig.add_subplot(111, projection="3d")
        self.scat = self.ax.scatter(0, 0, 0)
        self.line = self.ax.plot([], [], [], "r-")[0]

        self._setup_plot(scale)

    def _setup_plot(self, scale):
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

        zs = [d["point"].z for d in data]
        xs = [d["point"].x for d in data]
        ys = [d["point"].y for d in data]
        self.scat._offsets3d = (zs, xs, ys)
        self.line.set_data_3d(zs, xs, ys)

        return (self.scat, self.line)

    def show(self):
        plt.show()

    def save_gif(self, filename: Path | str):
        self.anim.save(filename, writer="pillow", fps=int(1000 / self.interval))
