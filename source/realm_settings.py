from realm import create_realm_name
from anima import Anima, green_food_list, food_list
from flora import flora_species
from extratraits import ExtraTraits
import random

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
    for i in range(10000):
        anima_list.append(Anima(i, "name/diet/strength/toughness", [(random.choice(food_list),), [random.uniform(1, 5), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4,10), random.uniform(4,10), random.uniform(30,80), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, width) , random.uniform(0, height)))

    return anima_list

    for i in range(herbivore_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [(random.choice(green_food_list),), [random.uniform(1, 5), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4,10), random.uniform(4,10), random.uniform(30,80), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, width) , random.uniform(0, height)))
    for i in range(carnivore_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [("meat",), [random.uniform(1, 8), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4, 15), random.uniform(4,15), random.uniform(30,80), random.uniform(0, 1), random.uniform(20,80), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, width) , random.uniform(0, height)))
    for i in range(any_count): 
        anima_list.append(Anima(i, "name/diet/strength/toughness", [(random.choice(food_list),), [random.uniform(1, 5), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4,10), random.uniform(4,10), random.uniform(30,80), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, width) , random.uniform(0, height)))
    return anima_list

def generate_flora(batch_count, scale_factor):
    extra_batch = True if random.random() < batch_count % 1 else False
    batch_count = int(batch_count//1 + 2*int(extra_batch) - 1)
    flora_list = [["tree", default_tree_count]]
    for batch in range(batch_count):
        plant = random.choice(list(flora_species.keys()))
        n = flora_species[plant][5]
        flora_list.append([plant, int(round(random.gauss(n**scale_factor, n**scale_factor/10)))])
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


