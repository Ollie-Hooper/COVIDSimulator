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
from numpy.random import random, randint, choice
from random import choices

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
VACCINATED = 4


# Vaccination class
class Vaccinator:
    def __init__(self, start_time=20, vaccination_capacity_rate=0.25, vaccination_max_capacity=20):
        self.start_time = start_time  # Day the vaccine begins to be distributed
        self.vaccination_capacity_rate = vaccination_capacity_rate  # How much to increase vaccination capacity each day
        self.vaccination_max_capacity = vaccination_max_capacity  # Max vaccination capacity per day
        self.vaccination_capacity = 0

    def increase_capacity(self):
        # Increases vaccination capacity
        if self.vaccination_capacity + self.vaccination_capacity_rate <= self.vaccination_max_capacity:
            self.vaccination_capacity += self.vaccination_capacity_rate
        else:
            self.vaccination_capacity = self.vaccination_max_capacity

    def vaccinate(self, pop):
        self.increase_capacity()
        new_pop = pop.copy()
        eligible_to_vaccinate = [(i, j) for i in range(len(new_pop)) for j in range(len(new_pop[i])) if
                                 new_pop[i, j].status == SUSCEPTIBLE or new_pop[i, j].status == RECOVERED]
        if int(self.vaccination_capacity) <= len(eligible_to_vaccinate):
            people_to_vaccinate = choices(eligible_to_vaccinate, k=int(self.vaccination_capacity))
        else:
            people_to_vaccinate = eligible_to_vaccinate
        for i, j in people_to_vaccinate:
            new_pop[i, j].set_status(VACCINATED)
        return new_pop


# Person class
class Person:

    def __init__(self, infection_length=14):
        self.status = SUSCEPTIBLE
        self.infection_length = infection_length
        self.age = choice(choice([range(0, 18), range(19, 29), range(30, 49), range(50, 69), range(70, 100)],
                                 p=[0.22, 0.12, 0.31, 0.22, 0.13]))
        self.recovery_probability = 0
        self.infection_probability = 0
        self.death_probability = 0
        self.set_probabilities()

    # probabilities of age based on age group
    def set_probabilities(self):
        # Death statistics based off covid related data on mortality rates of different ages
        if self.age < 50:
            self.recovery_probability = 0.7 / self.infection_length
            self.infection_probability = 0.1
            self.death_probability = 0.01 / self.infection_length
        elif self.age < 60:
            self.recovery_probability = 0.7 / self.infection_length
            self.infection_probability = 0.1
            self.death_probability = 0.02 / self.infection_length
        elif self.age < 70:
            self.recovery_probability = 0.7 / self.infection_length
            self.infection_probability = 0.1
            self.death_probability = 0.04 / self.infection_length
        elif self.age < 80:
            self.recovery_probability = 0.7 / self.infection_length
            self.infection_probability = 0.1
            self.death_probability = 0.08 / self.infection_length
        elif self.age <= 100:
            self.recovery_probability = 0.7 / self.infection_length
            self.infection_probability = 0.1
            self.death_probability = 0.15 / self.infection_length

    def set_status(self, status):
        self.status = status


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
    >>> sim.get_count_status()
    {'susceptible': 90.0, 'infected': 6.0, 'recovered': 3.0, 'dead': 1.0}

    """

    # Status codes to store in the numpy array representing the state.
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DEAD = 3
    VACCINATED = 4

    STATUSES = {
        'susceptible': SUSCEPTIBLE,
        'infected': INFECTED,
        'recovered': RECOVERED,
        'dead': DEAD,
        'vaccinated': VACCINATED
    }
    COLOURMAP = {
        'susceptible': 'yellow',
        'infected': 'red',
        'recovered': 'blue',
        'dead': 'black',
        'vaccinated': 'green'
    }
    COLOURMAP_RGB = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        'yellow': (255, 255, 0),
    }

    def __init__(self, width, height):
        # Basic simulation parameters:
        self.day = 0
        self.width = width
        self.height = height

        # Initialise Population (everyone susceptible with range of ages assigned to each element)
        self.pop = np.zeros((width, height), dtype=Person)
        for i in range(len(self.pop)):
            for j in range(len(self.pop[i])):
                self.pop[i, j] = Person()

        self.vaccinator = Vaccinator()

    def infect_randomly(self, num):
        """Choose num people randomly and make them infected"""
        for n in range(num):
            # Choose a random x, y coordinate and make that person infected
            # NOTE: This might select the same person twice...
            i = randint(self.width)
            j = randint(self.height)
            self.pop[i, j].set_status(self.INFECTED)

    def update(self):
        """Advance the simulation by one day"""
        # Use a copy of the old state to store the new state so that e.g. if
        # someone recovers but was infected yesterday their neighbours might
        # still become infected today.
        old_pop = self.pop
        new_pop = old_pop.copy()
        if self.vaccinator.start_time <= self.day:
            new_pop = self.vaccinator.vaccinate(old_pop)
        for i in range(self.width):
            for j in range(self.height):
                self.set_new_status(new_pop, i, j)
        self.pop = new_pop
        self.day += 1

    def set_new_status(self, pop, i, j):
        """Compute new status for person at i, j in the grid"""
        person = pop[i, j]

        # Update infected person
        if person.status == self.INFECTED:
            if person.recovery_probability > random():
                person.set_status(self.RECOVERED)
            elif person.death_probability > random():
                person.set_status(self.DEAD)

        # Update susceptible person
        elif person.status == self.SUSCEPTIBLE:
            num = self.num_infected_around(pop, i, j)
            if num * person.infection_probability > random():
                person.set_status(self.INFECTED)

    def num_infected_around(self, pop, i, j):
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
                    if pop[ip, jp].status == self.INFECTED:
                        number += 1

        return number

    def get_count_status(self):
        """Dict giving counts of people's status"""

        # NOTE: Maybe it's better to return counts rather than percentages...
        simgrid = self.get_status_grid()
        total = self.width * self.height
        counts = {}
        for status, statusnum in self.STATUSES.items():
            counts[status] = np.count_nonzero(simgrid == statusnum)
        return counts

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
            rgb_matrix[self.get_status_grid() == statusnum] = colour_rgb
        return rgb_matrix

    def get_status_grid(self):
        state = np.zeros(self.pop.shape)

        for i in range(len(state)):
            for j in range(len(state[i])):
                state[i, j] = self.pop[i, j].status
        return state
