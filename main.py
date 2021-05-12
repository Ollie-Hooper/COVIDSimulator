import argparse

from covid_sim.simulator import Simulation
from covid_sim.animation import plot_simulation, Animation


def main(*args):
    """Command line entry point.

    $ python simulator.py                        # show animation on screen
    $ python simulator.py --file=video.mp4       # save animation to video
    $ python simulator.py --plot                 # show plot on screen
    $ python simulator.py --plot --file=plot.pdf # save plot to pdf

    """
    #
    # Use argparse to handle parsing the command line arguments.
    #   https://docs.python.org/3/library/argparse.html
    #
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--size', metavar='N', type=int, default=50,
                        help='Use a N x N simulation grid')
    parser.add_argument('--duration', metavar='T', type=int, default=100,
                        help='Simulate for T days')
    parser.add_argument('--recovery', metavar='P', type=float, default=0.1,
                        help='Probability of recovery (per day)')
    parser.add_argument('--infection', metavar='P', type=float, default=0.1,
                        help='Probability of infecting a neighbour (per day)')
    parser.add_argument('--death', metavar='P', type=float, default=0.005,
                        help='Probability of dying when infected (per day)')
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--plot', action='store_true',
                        help='Generate plots instead of an animation')
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    args = parser.parse_args(args)

    # Set up the simulation
    simulation = Simulation(args.size, args.size,
                            args.recovery, args.infection, args.death)
    simulation.infect_randomly(args.cases)

    # Plot or animation?
    import matplotlib as plt
    if args.plot:
        fig = plot_simulation(simulation, args.duration)

        if args.file is None:
            #  python simulator.py --plot
            plt.show()
        else:
            #  python simulator.py --plot --file=plot.pdf
            fig.savefig(args.file)
    else:
        animation = Animation(simulation, args.duration)

        if args.file is None:
            #  python simulator.py
            animation.show()
        else:
            #  python simulator.py --file=animation.mp4
            #
            # NOTE: this needs ffmpeg to be installed.
            animation.save(args.file)


if __name__ == "__main__":
    #
    # CLI entry point. The main() function can also be imported and called
    # with string arguments.
    #
    import sys

    main(*sys.argv[1:])
