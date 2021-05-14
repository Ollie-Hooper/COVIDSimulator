import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


class Animation:
    """ 
    Animation.py takes infomation generated by the simulator.py and displays it in the 
    form of visual diagrams. These include grid animations and line animations. 

    """

    def __init__(self, simulation, duration):
        """Sets out the framework for the animation to take place in"""
        self.simulation = simulation
        self.duration = duration

        self.figure = plt.figure(figsize=(8, 4))
        self.axes_grid = self.figure.add_subplot(1, 2, 1)
        self.axes_line = self.figure.add_subplot(1, 2, 2)

        self.gridanimation = GridAnimation(self.axes_grid, self.simulation)
        self.lineanimation = LineAnimation(self.axes_line, self.simulation, duration)

    def show(self):
        """Runs the animation on screen"""
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                                  init_func=self.init, blit=True, interval=200)
        plt.show()

    def save(self, filename):
        """Run the animation and save as a video"""
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                                  init_func=self.init, blit=True, interval=300)
        writergif = PillowWriter(fps=10)
        animation.save(filename, writer=writergif)

    def init(self):
        """Initialise the animation (FuncAnimation)"""
        actors = []
        actors += self.gridanimation.init()
        actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Continously updates the animation frame by frame """
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animates the grid showing people's status (infected, dead, etc...) at each position"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        rgb_matrix = self.simulation.get_rgb_matrix()
        """Assigns people status' to colours for visual purposes"""
        self.image = self.axes.imshow(rgb_matrix)
        self.axes.set_xticks([])
        self.axes.set_yticks([])

    def init(self):
        return self.update(0)

    def update(self, framenum):
        """(frame number indicates number of days)"""
        day = framenum
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image.set_array(rgb_matrix)
        return [self.image]


class LineAnimation:
    """Animates a line series showing numbers of people in each status"""

    def __init__(self, axes, simulation, duration):
        """Labels the animation for simple interpretation by a user"""
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.xdata = []
        self.ydata = {status: [] for status in simulation.STATUSES}
        self.line_mpl = {}
        for status, colour in simulation.COLOURMAP.items():
            [line] = self.axes.plot([], [], color=colour, label=status, linewidth=2)
            self.line_mpl[status] = line
        self.axes.legend(prop={'size': 'x-small'}, loc='center right')
        self.axes.set_xlabel('days')
        self.axes.set_ylabel('%', rotation=0)

    def init(self):
        """Limits maximum size of the grid"""
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, 100])
        return []

    def update(self, framenum):
        """Converting counts into percentages"""
        counts = self.simulation.get_count_status()
        total = self.simulation.width * self.simulation.height
        percents = {k: 100 * v / total for k, v in counts.items()}
        self.xdata.append(len(self.xdata))
        for status, percent in percents.items():
            self.ydata[status].append(percent)
            self.line_mpl[status].set_data(self.xdata, self.ydata[status])
        return list(self.line_mpl.values())


def plot_simulation(simulation, duration):
    """Produces a grid plot showing status' at different points in time.

    At the end of the animation, a 5x3 grid of subplots showing the status at 15 different days (frames)
    throughout the simulation is generated.
    """
    W, H = 5, 3
    N = W * H

    fig = plt.figure()
    axes = fig.subplots(nrows=H, ncols=W).flat

    """Fixes the sapcing between subplots"""
    fig.subplots_adjust(wspace=0.1, hspace=0.4)

    """Finding days that are approximately equally spaced"""
    days = [(duration * i) // (N - 1) for i in range(N)]

    for ax, day in zip(axes, days):
        while simulation.day < day:
            simulation.update()
        rgb_matrix = simulation.get_rgb_matrix()
        ax.imshow(rgb_matrix)
        ax.set_title('Day ' + str(day))
        ax.set_xticks([])
        ax.set_yticks([])

    """ Return the figure generated by animation.py. The user of this 
    program can then decide whether to either show (screen) or savefig (file)."""
    return fig


def plot_ages(simulation):
    """Produces a histogram of the age distribution in the simulation"""
    age_grid = simulation.age_grid

    n_bins = 100
    fig, axs = plt.subplots(1, 1)
    axs.hist(age_grid.flatten(), bins=n_bins)
    axs.set_xlabel("Age")
    axs.set_ylabel("Count")

    return fig
