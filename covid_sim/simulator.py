#!/usr/bin/env python3
"""

simulator.py
Oscar Benjamin
March 2021

This script runs simulations of an epidemic (e.g. coronavirus) spreading
around people on a 2-dimensional grid. The script can be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is all done using the same simulation code which can also be imported
from this file and used in other ways.

The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    $ python simulator.py               # run simulation with default settings
    $ python simulator.py --cases=10    # have 10 initial cases
    $ python simulator.py --help        # show all command line options

It is also possible to create a video of the animation (if you install
ffmpeg):

    $ python simulator.py --file=simulation.mp4

NOTE: You need to install ffmpeg for the above to work. The ffmpeg program
must also be on PATH.
"""

import numpy as np
from numpy.random import random, randint

# ----------------------------------------------------------------------------#
#                   Class design                                              #
# ----------------------------------------------------------------------------#

# There are a number of classes here which could be combined in different
# ways.  The idea is that the same classes could be reused for other things.
# The classes are:
#
#    Simulation - stores and updates the simulation state
#    Animation - runs an animation of the simulation
#    GridAnimation - animates the epidemic on a grid
#    LineAnimation - animates a timeseries of the epidemic
#
# The idea is that the Animation class sets up a plot window and creates a
# GridAnimation and LineAnimation to manage the two different plot windows
# that are animated. Each of those has update() and init() methods which the
# Animation class will call to update the view. The Animation class also calls
# the update() method of the Simulation class. The Simulation class provides
# two ways to access the state of the simultion which are get_rgb_matrix() and
# get_percentage_status() and these are used by the *Animation classes to get
# the data that they need to display.
#
# The intention in this design is that the different pieces can be combined in
# different ways. For example it would be possible to make an alternative
# version of the Simulation class that simulated a different model of the
# epidemic. As long as it hsa the update(), get_rgb_matrix() and
# get_percentage_status() methods then it can work with all of the animation
# classes. Also it would be possible to create an alternative version of the
# Animation class that can still reuse e.g. LineAnimation even if it does not
# want to use GridAnimation. Finally other *Animation classes could be created
# as well and could easily be adapted to the scheme just by adding update()
# and init() methods.


SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3


#  Person class

class Person:

    def __init__(self):
        self.state = SUSCEPTIBLE
        self.age = random.choice(
            random.choice([range(0, 18), range(19, 29), range(30, 49), range(50, 69), range(70, 100)],
                          p=[0.22, 0.12, 0.31, 0.22, 0.13]))

    # probabilities of age based on age group
    def set_probabilities(self):
        if self.age < 20:
            self.recovery_probability = 0.7
            self.infected_probability = 0.4
            self.death_probability = 0.001
        elif self.age < 40:
            self.recovery_probability = 0.7
            self.infected_probability = 0.4
            self.death_probability = 0.001
        elif self.age < 60:
            self.recovery_probability = 0.7
            self.infected_probability = 0.4
            self.death_probability = 0.005

    def set_state(self, state):
        self.state = state


# ----------------------------------------------------------------------------#
#                   Simulation class                                          #
# ----------------------------------------------------------------------------#


class Simulation:
    """Simulation of an epidemic on a 2D grid

    In this model there are four states:
    susceptible (S), infected (I), recovered (R) and dead (D).

    The people are arranged in a grid in each state so e.g. if we have a 4x4
    grid the initial state might be like:

    S S S S
    S S I S
    S S S S
    S S S S

    The update() method advances the simulation by one day. For example the
    new state might be:

    S S S S
    S I R S
    S S S I
    S S S S

    Here the person who was infected (I) is now recovered (R). However two of
    their neighbours who were susceptible (S) are now infected (I).

    The state update is not deterministic and is given by probabilities
    according to the following rules:

    1) Infected: an infected person might recover (-> R) with probability given
    by the recovery_probability parameter (default 0.1)

    2) Infected: if an infected person does not recover then they might die (-> D)
    with probability death_propability (default 0.005)

    3) Susceptible: a susceptible person might get infected (-> I) by one of
    their 8 neighbours in the grid. If N of their neighbours are infected then
    they will become infected with probability N*infection_probability where
    infection_probability is a simulation parameter (default 0.1)

    The methods get_rgb_matrix() and get_percentage_status() can be used to
    query the state of the simulation at any time.

    Example
    =======

    Create a simulation on a 10x10 grid (with 100 people) with probabilities
    0.1, 0.2 and 0.05 for recovery, infection and death and 3 people initially
    infected. Run the simulation for 10 days and then ask what percentage of
    people are in each state:

    >>> sim = Simulation(10, 10, recovery=0.1, infection=0.2, death=0.05)
    >>> sim.infect_randomly(3)  # infect three people (chosen randomly)
    >>> for n in range(10):     # advance the simulation through 10 days
    ...     sim.update()
    >>> sim.get_percentage_status()
    {'susceptible': 90.0, 'infected': 6.0, 'recovered': 3.0, 'dead': 1.0}

    """

    # Status codes to store in the numpy array representing the state.
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DEAD = 3

    STATUSES = {
        'susceptible': SUSCEPTIBLE,
        'infected': INFECTED,
        'recovered': RECOVERED,
        'dead': DEAD,
    }
    COLOURMAP = {
        'susceptible': 'green',
        'infected': 'red',
        'recovered': 'blue',
        'dead': 'black',
    }
    COLOURMAP_RGB = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
    }

    def __init__(self, width, height, recovery, infection, death):
        # Basic simulation parameters:
        self.day = 0
        self.width = width
        self.height = height
        self.recovery_probability = recovery
        self.infection_probability = infection
        self.death_probability = death

        # Initialise Population (everyone susceptible with range of ages assigned to each element)
        self.pop = np.zeros((width, height), dtype=Person)
        for i in range(len(self.pop)):
            for j in range(len(self.pop[i])):
                self.pop[i, j] = Person()

    def infect_randomly(self, num):
        """Choose num people randomly and make them infected"""
        for n in range(num):
            # Choose a random x, y coordinate and make that person infected
            # NOTE: This might select the same person twice...
            i = randint(self.width)
            j = randint(self.height)
            self.state[i, j] = self.INFECTED

    def update(self):
        """Advance the simulation by one day"""
        # Use a copy of the old state to store the new state so that e.g. if
        # someone recovers but was infected yesterday their neighbours might
        # still become infected today.
        old_state = self.state
        new_state = old_state.copy()
        for i in range(self.width):
            for j in range(self.height):
                new_state[i, j] = self.get_new_status(old_state, i, j)
        self.state = new_state
        self.day += 1

    def get_new_status(self, state, i, j):
        """Compute new status for person at i, j in the grid"""
        status = state[i, j]

        # Update infected person
        if status == self.INFECTED:
            if self.recovery_probability > random():
                return self.RECOVERED
            elif self.death_probability > random():
                return self.DEAD

        # Update susceptible person
        elif status == self.SUSCEPTIBLE:
            num = self.num_infected_around(state, i, j)
            if num * self.infection_probability > random():
                return self.INFECTED

        # Return the old status (e.g. DEAD/RECOVERED)
        return status

    def num_infected_around(self, state, i, j):
        """Count the number of infected people around person i, j"""

        # Need to be careful about people at the edge of the grid.
        # ivals and jvals are the coordinates of neighbours around i, j
        ivals = range(max(i - 1, 0), min(i + 2, self.width))
        jvals = range(max(j - 1, 0), min(j + 2, self.height))
        number = 0
        for ip in ivals:
            for jp in jvals:
                # Don't count self as a neighbour
                if (ip, jp) != (i, j):
                    if state[ip, jp] == self.INFECTED:
                        number += 1

        return number

    def get_percentage_status(self):
        """Dict giving percentage of people in each statue"""

        # NOTE: Maybe it's better to return counts rather than percentages...
        simgrid = self.state
        total = self.width * self.height
        percentages = {}
        for status, statusnum in self.STATUSES.items():
            count = np.count_nonzero(simgrid == statusnum)
            percentages[status] = 100 * count / total
        return percentages

    def get_rgb_matrix(self):
        """RGB matrix representing the statuses of the people in the grid

        This represents the state as an RGB (colour) matrix using the
        coloursceheme set in the class variables COLOURMAP and COLOURMAP_RGB.
        The resulting matrix is suitable to be used with e.g. matplotlib's
        imshow function.
        """
        rgb_matrix = np.zeros((self.width, self.height, 3), int)
        for status, statusnum in self.STATUSES.items():
            colour_name = self.COLOURMAP[status]
            colour_rgb = self.COLOURMAP_RGB[colour_name]
            rgb_matrix[self.state == statusnum] = colour_rgb
        return rgb_matrix


if __name__ == "__main__":
    #
    # CLI entry point. The main() function can also be imported and called
    # with string arguments.
    #
    import sys

    main(*sys.argv[1:])
