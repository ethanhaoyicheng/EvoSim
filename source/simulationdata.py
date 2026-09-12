import statistics
from todisplay import to_display
from anima import food_list, extra_traits

class Realm_Database():
    def __init__(self, realm):
        self.realm = realm 
        self.groups_by_diet = [[],[],[]]
        self.anima_id = -1
        self.ghost_id = -1

        self.death_causes = [0,0,0,0,0]
        
        self.anima_populations = []
        self.avg_genomes = [] 
        self.diets = [] 
        self.avg_lifespans = []
        self.lifespan_quartiles = []
        self.avg_ages = []
        self.age_quartiles = []

        self.avg_statuses = []
        self.needs = []
        self.fruits = []
        self.fruits_per_creature = []
        self.offspring_count_distributions = []
        self.ancestries = []        #use parent lists to find ancestors/common ancestors and track descendants
        self.geomaps = []

    def append_groups_by_diet(self, anima):
        diet_types = ["herbivore", "carnivore", "omnivore"]
        self.groups_by_diet[diet_types.index(anima.diet_type())].append(anima)
    
    def remove_groups_by_diet(self, corpse):
        diet_types = ["herbivore", "carnivore", "omnivore"]
        self.groups_by_diet[diet_types.index(corpse.diet_type())].remove(corpse)

    def update_groups_by_diet(self):

        diet_types = ["herbivore", "carnivore", "omnivore"]

        """
        if len(self.realm.elements[1]) > self.anima_id - len(self.realm.graveyard[1]) - len(self.realm.ghostyard[1]) + 1:    
            for anima in self.realm.elements[1][self.anima_id - len(self.realm.graveyard[1]) - len(self.realm.ghostyard[1]) + 1 :]: #append new animas only
                self.groups_by_diet[diet_types.index(anima.diet_type())].append(anima)
            self.anima_id = self.realm.anima_id() - 1   #-1 then +1 later, so new anima is first evaluated
        """

        #only remove when in ghostyard, so corpses still count for data collection (it is otherwise hard to coordinate both graveyard and ghostyard)
        
        """
        if len(self.realm.ghostyard[1]) > self.ghost_id + 1:
            for dead_anima in self.realm.ghostyard[1][self.ghost_id + 1:]:
                group = self.groups_by_diet[diet_types.index(dead_anima.diet_type())]

                if dead_anima not in group:
                    print("ERROR: dead_anima missing:", dead_anima)
                    print("Diet:", dead_anima.diet_type())
                    print("Group contains:", group)
                    print("ghost_id:", self.ghost_id)
                    print("anima_id:", self.anima_id)

                self.groups_by_diet[diet_types.index(dead_anima.diet_type())].remove(dead_anima)
            self.ghost_id = len(self.realm.ghostyard[1]) - 1
        """


    def increment_death_causes(self, cause_index):
        self.death_causes[cause_index] += 1

    def calc_avg_status(self, anima_list):
        avg_status = []
        status_list = [anima.status for anima in anima_list]
        if status_list:
            for i in range(len(status_list[0])):
                avg_status.append(get_avg([max(status[i], 0) for status in status_list]))   #min value is always 0 here... for future use, let this be known
        return avg_status

    def calc_avg_genome(self, anima_list):
        avg_genome = []
        genome_list = [anima.genome for anima in anima_list]
        if genome_list:
            for i in range(len(genome_list[0])):
                avg_genome.append(get_avg([genome[i] for genome in genome_list]))
        return avg_genome

    def calc_genome_quartiles(self, anima_list):
        avg_genome = []
        genome_list = [anima.genome for anima in anima_list]
        
        #should put all this into my own quartile function with type case
        if len(genome_list) >= 2:
            for i in range(len(genome_list[0])):
                if isinstance(genome_list[0][i], (int, float)):
                    avg_genome.append(statistics.quantiles([genome[i] for genome in genome_list]))
                else:
                    avg_genome.append("D/V")    #meaning discrete value
            return avg_genome
        else:
            return None

    def calc_diets(self, anima_list):
        diet_counter = [[food, 0] for food in food_list]
        diet_list = [anima.diet for anima in anima_list]

        if diet_list:
            for diet in diet_list:
                for food in diet:
                    for item in diet_counter:
                        if food == item[0]:
                            item[1] += 1 
        return diet_counter
    
    def calc_extra_traits(self, anima_list):
        trait_counter = [[trait, 0] for trait in extra_traits]
        traits_list = [anima.extra_traits for anima in anima_list]

        if traits_list:
            for traits in traits_list:
                for trait in traits:
                    for item in trait_counter:
                        if trait == item[0]:
                            item[1] += 1 
        return trait_counter

    def calc_total_avg_lifespan(self):
        dead_ones = self.realm.graveyard[1] + self.realm.ghostyard[1]
        if dead_ones:
            return mean([anima.age for anima in dead_ones])
        else:
            return None
    
    def calc_avg_lifespan(self):
        dead_ones = self.realm.graveyard[1] + self.realm.ghostyard[1][len(self.realm.ghostyard[1])-10 : ]
        if dead_ones:
            return mean([anima.age for anima in dead_ones])
        else:
            return None
    
    def calc_lifespan_quartiles(self):
        dead_ones = self.realm.graveyard[1] + self.realm.ghostyard[1][len(self.realm.ghostyard[1])-10 : ]
        if len(dead_ones) >= 2:
            return statistics.quantiles([anima.age for anima in dead_ones])
        else:
            return None
    
    def calc_avg_age(self, anima_list):
        if anima_list:
            return mean([anima.age for anima in anima_list])
    
    def calc_age_quartiles(self, anima_list):
        if len(anima_list) >= 2:
            return statistics.quantiles([anima.age for anima in anima_list])
        else:
            return None

    def calc_offspring_count_distribution(self, anima_list):
        
        offspring_count_list = [len(anima.offspring) for anima in anima_list]

        if offspring_count_list:
            offspring_count_counter = [[i, 0] for i in range(max(offspring_count_list) + 1)]
            for offspring_count in offspring_count_list:
                offspring_count_counter[offspring_count][1] += 1
            return offspring_count_counter
        return None

    def update(self):
        time = self.realm.time
        #self.update_groups_by_diet()
        groups_by_diet = self.groups_by_diet

        self.anima_populations.append((time, len(groups_by_diet[0]), len(groups_by_diet[1])))
        self.avg_genomes.append((time, self.calc_avg_genome(groups_by_diet[0]), self.calc_avg_genome(groups_by_diet[1]))) 
        self.diets.append((time, self.calc_diets(self.realm.elements[1])))   
        self.avg_lifespans.append((time, self.calc_avg_lifespan())) #, self.calc_avg_lifespan(groups_by_diet[1])
        self.lifespan_quartiles.append((time, self.calc_lifespan_quartiles())) #, self.calc_lifespan_quartiles(groups_by_diet[1])
        self.avg_ages.append((time, self.calc_avg_age(self.realm.elements[1])))
        self.age_quartiles.append((time, self.calc_age_quartiles(self.realm.elements[1])))
        
        self.avg_statuses.append((time, self.calc_avg_status(groups_by_diet[0]), self.calc_avg_status(groups_by_diet[1])))
        self.offspring_count_distributions.append((time, self.calc_offspring_count_distribution(groups_by_diet[0]), self.calc_offspring_count_distribution(groups_by_diet[1])))
    
    def get_avg_genome(self):
        return to_display(self.calc_avg_genome(self.realm.elements[1]))
    
    def get_diets(self):
        return to_display(self.calc_diets(self.realm.elements[1]))

    
                    
def get_avg(genotype_list):       #should be xs maybe

        if isinstance(genotype_list[0], (int, float)):
            avg = mean(genotype_list)

        elif isinstance(genotype_list[0], (list)):
            return [get_avg([genotype[g] for genotype in genotype_list]) for g in range(len(genotype_list[0]))]

        elif isinstance(genotype_list[0], (tuple)):
            return mode(genotype_list)

        else:
            avg = None

        return avg

def mean(xs):
    return sum(xs)/len(xs)

def mode(xs):
    return statistics.mode(xs)

class Sim_Database():
    def __init__(self, simulation):
        self.sim = simulation
        self.table = []

    def add_realms(self):
        for realm in self.sim.realms:
            if realm not in self.table:
                self.add_realm(realm)

    def add_realm(self, realm):
        self.table.append(realm)