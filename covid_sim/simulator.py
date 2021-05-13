#!/usr/bin/env python3
import numpy as np
from numpy.random import random, randint, choice
from random import choices


"""
Simulator.py is used to generate the data needed to simulate our virus pandemic.
This works by generating a matrix of person objects, each with their own attributes on how the virus will affect them.
Each person has the chance to spread the virus to any of their neighbours, depending on their probabilities of infection
Individuals can be of 4 different states; Susceptible, Infected, Recovered or Dead, during the epidemic.
The simulation begins by randomly infecting a select number of individuals, by updating their status to infected

Additionally, we have included a vaccination method, where persons are updated to a "Vaccinator" status at random,
altering their probabilities.
There are also additional parameters, through the Measures class, that may be selected when running the program. As an
example, the Lockdown Measure will reduce the probability of infection for X number of days.
"""

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3
VACCINATED = 4


# Vaccination class
class Vaccinator:

    """
    The Vaccinator class is used to model our vaccine rollout.
    It begins at a specified date during the epidemic, with the roll out rate developing over time
    The Vaccine is designed to reduce the risk of infection, modelled by changing an individuals probabilities
    """

    def __init__(self, start=20, rate=0.25, max=20):
        self.start_time = start  # Day the vaccine begins to be distributed
        self.vaccination_capacity_rate = rate  # How much to increase vaccination capacity each day
        self.vaccination_max_capacity = max  # Max vaccination capacity per day
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
        # ^ Decides whether a Person is eligible to vaccinate (only if they are Susceptible or Recovered) ^
        if int(self.vaccination_capacity) <= len(eligible_to_vaccinate):
            people_to_vaccinate = choices(eligible_to_vaccinate, k=int(self.vaccination_capacity))
        else:
            people_to_vaccinate = eligible_to_vaccinate
        for i, j in people_to_vaccinate:
            new_pop[i, j].set_status(VACCINATED)
        return new_pop  # Returns updated population with vaccinated persons


# Person class
class Person:
    """
    The Person class creates each individual object to be added to the population
    Each is assigned to an age range, which determines their infection, recovery and death probabilities
    """
    def __init__(self, probabilities, infection_length=14):
        self.status = SUSCEPTIBLE
        self.infection_length = infection_length
        self.age = choice(choice([range(0, 18), range(19, 29), range(30, 49), range(50, 69), range(70, 100)],
                                 p=[0.22, 0.12, 0.31, 0.22, 0.13]))
        self.recovery_probability = 0
        self.infection_probability = 0
        self.death_probability = 0
        self.set_probabilities(probabilities)

    def set_probabilities(self, probabilities):
        # Assigns the input probabilities for each state to the different age ranges
        for age, p in probabilities["Infection"].items():
            if self.age < int(age):
                self.infection_probability = p
                break
        for age, p in probabilities["Recovery"].items():
            if self.age < int(age):
                self.recovery_probability = p
                break
        for age, p in probabilities["Death"].items():
            if self.age < int(age):
                self.death_probability = p
                break
        self.recovery_probability /= self.infection_length
        self.death_probability /= self.infection_length

    def set_status(self, status):
        self.status = status


# Measure class
class Measure:
    """
    The Measure class is used to emulate different scenarios that could be implemented during an epidemic to help combat
    the spread of a virus.
    These are also modeled by changing probabilities.
    However, these will change all persons attributes for the set number of days the measure will last for.
    """
    def __init__(self, start_dates=(25,), end_dates=(75,), multiplier=0.5, probability_attr='infection_probability'):
        self.start_dates = start_dates
        self.end_dates = end_dates
        self.multiplier = multiplier  # chosen probabilities
        self.probability_attr = probability_attr

    def update(self, pop, date):
        if date in self.start_dates:
            new_pop = self.start(pop.copy())
        elif date in self.end_dates:  # Updates population attributes when Measure date is reached
            new_pop = self.stop(pop.copy())
        else:
            new_pop = pop.copy()
        return new_pop

    def start(self, pop):
        for i in range(len(pop)):
            for j in range(len(pop)):
                old_probability = getattr(pop[i, j], self.probability_attr)
                new_probability = old_probability * self.multiplier
                setattr(pop[i, j], self.probability_attr, new_probability)
        return pop

    def stop(self, pop):
        for i in range(len(pop)):
            for j in range(len(pop[i])):
                old_probability = getattr(pop[i, j], self.probability_attr)
                new_probability = old_probability / self.multiplier
                setattr(pop[i, j], self.probability_attr, new_probability)
        return pop

# Series of subclasses of the Measure Class, representing different epidemic scenarios
class Lockdown(Measure):
    def __init__(self, starts=(25,), ends=(75,), multiplier=0.5):
        super().__init__(starts, ends, multiplier, 'infection_probability')


class SocialDistancing(Measure):
    def __init__(self, starts=(10,), ends=(), multiplier=0.5):
        super().__init__(starts, ends, multiplier, 'infection_probability')


class ImprovedTreatment(Measure):
    def __init__(self, starts=(50,), ends=(), multiplier=1.25):
        super().__init__(starts, ends, multiplier, 'recovery_probability')


class Ventilators(Measure):
    def __init__(self, starts=(0,), ends=(), multiplier=0.6):
        super().__init__(starts, ends, multiplier, 'death_probability')


class Simulation:
    """
    The simulation class is used to create the different matrices required to produce the animated simulation
    The status matrix stores the current status of all people in the population.
    This is updated every time step, where the different probabilities determine how the virus spreads.
    Any individual has the chance to infect any susceptible neighbours.
    In this case, this will include any person immediately in any one direction, including 1 diagonally.

    An rgb matrix is also formed, to allow us to better visually show the spread of the virus.
    Each state of a person is represented by a different colour, and the age by a different shade.
    This can then be used to produce the animation grid using Matplotlib
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

    def __init__(self, **kwargs):
        # Basic simulation parameters:
        self.day = 0
        self.width = kwargs["size"]
        self.height = kwargs["size"]

        # Initialise Population (everyone susceptible with range of ages assigned to each element)
        self.pop = np.zeros((kwargs["size"], kwargs["size"]), dtype=Person)
        for i in range(len(self.pop)):
            for j in range(len(self.pop[i])):
                self.pop[i, j] = Person(kwargs["probabilities"], kwargs["length"])

        self.vaccinator = Vaccinator(**kwargs["vaccinator"])
        self.measures = [Lockdown(**kwargs["measures"]["Lockdown"]),
                         SocialDistancing(**kwargs["measures"]["Social Distancing"]),
                         ImprovedTreatment(**kwargs["measures"]["Improved Treatment"]),
                         Ventilators(**kwargs["measures"]["Ventilators"])]

    def infect_randomly(self, num):
        for n in range(num):
            # Choose a random x, y coordinate and make that person infected, do this n number of times
            i = randint(self.width)
            j = randint(self.height)
            self.pop[i, j].set_status(self.INFECTED)

    def update(self):
        # Advance the simulation by one day
        old_pop = self.pop
        new_pop = old_pop.copy()
        # Use a copy of the old state to store the new state so that e.g. if
        # someone recovers but was infected yesterday their neighbours might
        # still become infected today.
        if self.vaccinator.start_time <= self.day:
            new_pop = self.vaccinator.vaccinate(old_pop)

        for measure in self.measures:
            new_pop = measure.update(new_pop, self.day)

        for i in range(self.width):
            for j in range(self.height):
                self.set_new_status(new_pop, i, j)
        self.pop = new_pop
        self.day += 1

    def set_new_status(self, pop, i, j):
        #Compute new status for person at i, j in the grid
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
        #Count the number of infected people around person i, j
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
        #Dictionary giving counts of people's status

        simgrid = self.get_status_grid()
        total = self.width * self.height
        counts = {}
        for status, statusnum in self.STATUSES.items():
            counts[status] = np.count_nonzero(simgrid == statusnum)
        return counts

    def get_rgb_matrix(self):
        rgb_matrix = np.zeros((self.width, self.height, 3), int)
        code_to_status = {v: k for k, v in self.STATUSES.items()} # Gets rbg data from previously declared colour scheme
        for i in range(len(self.pop)):
            for j in range(len(self.pop[i])):
                person = self.pop[i, j]
                age = person.age
                colour_name = self.COLOURMAP[code_to_status[person.status]]
                colour_rgb = self.COLOURMAP_RGB[colour_name]
                age_adjusted_colour_rgb = [c - age if c != 0 else 0 for c in colour_rgb]
                rgb_matrix[i, j] = age_adjusted_colour_rgb
                #Prodcues a darker shade for older ages by taking their age value away from their rgb value
        return rgb_matrix

    def get_status_grid(self):
        state = np.zeros(self.pop.shape)
        for i in range(len(state)):
            for j in range(len(state[i])):
                state[i, j] = self.pop[i, j].status
        return state
