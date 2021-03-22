class Country:

    def __init__(self, population, pop_density, n_cities):
        self.cities = [City(population/n_cities) for i in n_cities]
