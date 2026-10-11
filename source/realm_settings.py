from realm import create_realm_name
from anima import Anima, green_food_list, food_list
from flora import flora_species
from extratraits import ExtraTraits
import random

import sys
seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print('Primordial biolist of seed ' + str(seed))

width = 600
height = 500

herbivore_count = 380
carnivore_count = 30
any_count = 20

flora_factor = 25
default_tree_count = 25

#[["tree", 600], ["bush", 800], ["lily", 500]]

def generate_primordial_list(width, height, herbivore_count, carnivore_count, any_count):
    anima_list = []
    for i in range(herbivore_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [(rng.choice(green_food_list),), [rng.uniform(1, 5), [1,0.5,0.3]], rng.uniform(15, 30), rng.uniform(5,15), rng.uniform(4,10), rng.uniform(4,10), rng.uniform(30,80), rng.uniform(0, 1), rng.uniform(30,100), rng.uniform(40,200), rng.uniform(5,50), ExtraTraits(set())], None, rng.uniform(0, width) , rng.uniform(0, height)))
    for i in range(carnivore_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [("meat",), [rng.uniform(1, 8), [1,0.5,0.3]], rng.uniform(15, 30), rng.uniform(5,15), rng.uniform(4, 15), rng.uniform(4,15), rng.uniform(30,80), rng.uniform(0, 1), rng.uniform(20,80), rng.uniform(40,200), rng.uniform(5,50), ExtraTraits(set())], None, rng.uniform(0, width) , rng.uniform(0, height)))
    for i in range(any_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [(rng.choice(food_list),), [rng.uniform(1, 5), [1,0.5,0.3]], rng.uniform(15, 30), rng.uniform(5,15), rng.uniform(4,10), rng.uniform(4,10), rng.uniform(30,80), rng.uniform(0, 1), rng.uniform(30,100), rng.uniform(40,200), rng.uniform(5,50), ExtraTraits(set())], None, rng.uniform(0, width) , rng.uniform(0, height)))
    return anima_list

def generate_flora(batch_count, scale_factor):
    extra_batch = True if rng.random() < batch_count % 1 else False
    batch_count = int(batch_count//1 + 2*int(extra_batch) - 1)
    flora_list = [["tree", default_tree_count]]
    for batch in range(batch_count):
        plant = rng.choice(list(flora_species.keys()))
        n = flora_species[plant][5]
        flora_list.append([plant, int(round(rng.gauss(n**scale_factor, n**scale_factor/10)))])
    return flora_list

default_realm_settings = [
    create_realm_name(),
    width,
    height,
    1.0,
    0.15,
    0.02,
    generate_flora(flora_factor, 1),
    generate_primordial_list(width, height, herbivore_count, carnivore_count, any_count),
    "name/diet/extra_traits/strength/toughness",
]


