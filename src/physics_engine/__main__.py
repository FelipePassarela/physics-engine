import argparse
from functools import partial

from pyglm import glm

from physics_engine.AnimatedPlot import AnimatedPlot
from physics_engine.Simulation import Simulation


def update(simulation: Simulation) -> list[dict[str, glm.vec3]]:
    simulation.update()
    plot_data: list[dict] = []
    for particle in simulation.particles:
        plot_data.append({"point": particle.position})
    return plot_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate particles under forces.")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output GIF filename",
    )
    args = parser.parse_args()

    simulation = Simulation()
    anim = AnimatedPlot(
        partial(update, simulation=simulation),
        nframes=60,
        scale=simulation.SCALE,
        interval=50,
    )

    if args.output is None:
        anim.show()
    else:
        anim.save_gif(args.output or "particle_simulation.gif")


if __name__ == "__main__":
    main()
