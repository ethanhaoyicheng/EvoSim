from cell import Cell
import fruit
import random
from math import sqrt

class Flora(Cell):
    def __init__(self, id, genotype, realm, spawnx, spawny, fruit=fruit.apple, fruitNo = 0):
        super().__init__(realm, spawnx, spawny)
        self.id = id
        self.realm = realm
        self.fruit = fruit
        self.capacity = genotype[0]
        self.batch_size = genotype[1]
        self.rate = genotype[2] * self.realm.temperature / max(1, min(10, sqrt(self.distance_to_nearest_a(1))))
        self.fruitNo = fruitNo

        self.food_given = self.fruit.name
        self.food_effect = self.fruit.statusChange

    def bear(self, amount = 1):
        self.fruitNo += amount
    
    def provide(self, quantity = 1):
        quantity_provided = min(quantity, self.fruitNo)
        self.fruitNo -= quantity_provided
        return quantity_provided

    def tick(self):
        if random.uniform(0,1) < self.rate and self.fruitNo < self.capacity:
            self.bear(self.batch_size)

flora_species = {
    "tree" : [["grass"], 4, 3, 0.01, fruit.apple, 100],
    #"bush" : [["grass"], 10, 4, 0.025, fruit.berry, 125],
    #"vine" : [["grass", "water"], 1, 1, 0.0025, fruit.melon, 15],
    #"reed" : [["water"], 2, 2, 0.02, fruit.lavendar, 40],
    "lily" : [["water"], 1, 1, 0.05, fruit.lily, 100],
    #"wildgrass" : [["grass"], 1, 1, 0.01, fruit.wildgrass, 400],
    
    "beanstalk" : [["grass", "tree"], 1, 1, 1, fruit.bean, 3],
    #magical beanstalk rarely spawns magic bean giving mutations
}

#add plants with multiple different fruit each?

#add effects to plants, ie poison