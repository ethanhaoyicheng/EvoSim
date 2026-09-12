from world_facts import *
from biome import *
from flora import Flora, flora_species
from anima import Anima
from cell import Cell
from angle import *
from math import floor, ceil
from nickname import generate_nickname
from todisplay import to_display

from spatialhash import SpatialHash

from simulationdata import Realm_Database

import random

CONSOLE_ON = False

SPATIAL_HASH_CELL_SIZE = 20 

MAX_WATER_GENERATION_ITERATION_COUNT = 999 #99
MAX_ICE_GENERATION_ITERATION_COUNT = 999
MAX_FLORA_GENERATION_ITERATION_COUNT = 999

WATER_MIN_RADIUS = 3
WATER_MAX_RADIUS = 15

ICE_MIN_RADIUS = 18
ICE_MAX_RADIUS = 55
MAX_ICE_CENTRE_Y = 60

POOL_ANGLE_GRADATION = 360

STARTING_FRUIT_RATIO = 0.25

class Realm:
    
    def __init__(self, name, width, height, temperature, wetness, iceness, floraness, primordialList, creature_naming_mode):
        self.time = 0
        self.name = name
        self.width = width
        self.height = height              
        self.temperature = temperature  
        self.wetness = wetness              #water coverage as a ratio to overall area
        self.iceness = iceness              #ice  '''
        self.floraness = floraness          #int list giving how many of each flora species will be generated [[name1, population1], [name2, population2]]
        self.fruit_list = list(set([flora_species[species[0]][4] for species in floraness]))

        self.elements = [[],[]]             #elements updated each realm tick   [flora][anima]  
        self.graveyard = [[],[]]
        self.ghostyard = [[],[]]
        #self.environment = [[],[]]          #elements not updated once simulation starts    [water][ice]
        self.environment = []               #stores terrain or flora at each x/y access by environment[row][col] aka [y][x] 
        self.spatialhash = SpatialHash(SPATIAL_HASH_CELL_SIZE, self.width, self.height)

        self.creature_naming_mode = creature_naming_mode

        self.database = Realm_Database(self)

        self.add_elements(primordialList)
        self.generate_world()

        
        
    
    def generate_world(self):
        self.environment = [["grass" for _ in range(self.width)] for _ in range(self.height)]
        self.__generate_water()
        self.__generate_ice()   #should ice cannibalise water, or avoid in pool generating??
        self.__generate_flora()

    def __generate_water(self):
    
        #self.environment[0] = [[False for _ in range(self.width)] for _0 in range(self.height)]

        #water_limit = self.width * self.height * self.wetness
        print("Generating water...")
        iteration_count = 0
        while self.check_water() < self.wetness and iteration_count < MAX_WATER_GENERATION_ITERATION_COUNT:
            cx = random.randint(0, self.width - 1)  #floats?
            cy = random.randint(0, self.height - 1)
            
            pool_radius = random.randint(WATER_MIN_RADIUS, WATER_MAX_RADIUS)
            self.generate_pool(cx, cy, pool_radius, 1, "rounded")
            
            iteration_count += 1
            print(iteration_count)
            print("iteration^")

    def __generate_ice(self):
        print("Generating ice...")
        iteration_count = 0
        while self.check_ice() < self.iceness and iteration_count < MAX_ICE_GENERATION_ITERATION_COUNT:
            cx = random.randint(0, self.width - 1)  #floats?
            cy = random.randint(0, MAX_ICE_CENTRE_Y)
            pool_radius = random.randint(ICE_MIN_RADIUS, ICE_MAX_RADIUS)
            self.generate_pool(cx, cy, pool_radius, 2, "flattened")

            iteration_count += 1
            print(iteration_count)
            print("iteration^")

    def generate_pool(self, cx, cy, radius, type, shapetype):
        #using parametric polar curves to generate curved pools of varying shape

        angle_start = random.randint(0, POOL_ANGLE_GRADATION)
        r = radius
        pool_points = []
        maxr = 0
        velocity = 0
    
        #acceleration = random.uniform(-0.5, 0.5)
        for u_theta in range (POOL_ANGLE_GRADATION):
            normalising_factor = 2 * PI / POOL_ANGLE_GRADATION
            n_theta = u_theta * normalising_factor
            t = (angle_start + u_theta) * normalising_factor

            velocity += random.uniform(-0.15, 0.15)   
            velocity *= 0.95

            if POOL_ANGLE_GRADATION - u_theta <= 0.1 * POOL_ANGLE_GRADATION:
                velocity += (radius - r)/5 

            #if random.random() < 0.1:
                #acceleration = random.uniform(-0.5, 0.5)

           # velocity += acceleration
            
            if shapetype == "rounded":
                r = max(r + velocity, 1) 
                #r = radius + 2.5 * sin(2 * t + angle_start * normalising_factor)
            elif shapetype == "flattened":
                r = max(r * cos(t) + random.uniform(-2, 2) * sin(t), 1)  
            # -> collect points using rsintheta and rcostheta
            if r > maxr:
                maxr = r
            if shapetype == "rounded":
                pool_points.append((cx + r*cos(t), cy + r*sin(t)))
            elif shapetype == "flattened":
                pool_points.append((cx + r*cos(n_theta), cy + r*sin(n_theta)))
            #print(theta)
        for point in pool_points:
            #print(point)
                self.environment[int(point[1]) % self.height][int(point[0]) % self.width] = terrain_index[type]  #temporary code, need fill in            possible solution: keep choosing adjacent tile closest to next (polar?) function result until back to original tile, then closed object can be easily filled in using edge of pool as boundaries for fill in, for each row start filling in when reach one and stop when reach next, but need to cover edge cases of pools that go off map, cant then use polarity, so how?
                #print((int(point[0]), int(point[1])))
        # -> draw inside polygon of points, checking for edge of world
        centre = Cell(self, cx, cy)
        maxr = int(maxr+1)
        if shapetype == "rounded":
            for row in range(cy-maxr, cy + maxr+1):
                for col in range(cx-maxr, cx + maxr+1):
                        col = col % self.width
                        row = row % self.height
                        cell = Cell(self, col, row)
                        arg = centre.angle_to(cell)
                        u_theta = arg / normalising_factor
                        p1 = pool_points[(floor(u_theta) - angle_start) % POOL_ANGLE_GRADATION]
                        p2 = pool_points[(floor(u_theta) - angle_start+ 1) % POOL_ANGLE_GRADATION]
                        d1 = centre.distance_to(p1)
                        d2 = centre.distance_to(p2)
                        lerpdist = d1 + (d2-d1) * (u_theta-floor(u_theta))
                        if cell.is_within(centre, lerpdist + 1):
                            self.environment[row][col] = terrain_index[type]
                            #print((col,row))
        if shapetype == "flattened":
            for row in range(cy-maxr, cy + maxr+1):
                for col in range(cx-maxr, cx + maxr+1):
                    if 0 <= col < self.width and 0 <= row < self.height:
                        cell = Cell(self, col, row)
                        arg = centre.angle_to(cell)
                        u_theta = arg / normalising_factor
                        p1 = pool_points[floor(u_theta)]
                        p2 = pool_points[ceil(u_theta % 2*PI)]
                        d1 = centre.distance_to(p1)
                        d2 = centre.distance_to(p2)
                        lerpdist = d1 + (d2-d1) * (u_theta-floor(u_theta))
                        if cell.is_within(centre, lerpdist + 0.5):
                            self.environment[row][col] = terrain_index[type]
                           

        #fill in with terrain_index[type]
        

    def __generate_flora(self):
        #species[0] is the name of the species
        #species[1] is the limit of the number of each species to be generated
        flora_id = self.count_flora() #id starts from 0
        for species in self.floraness:
            if species[0] in flora_species:
                for _ in range(int(species[1])):
                    iteration_count = 0
                    while iteration_count < MAX_FLORA_GENERATION_ITERATION_COUNT:
                        cx = random.randint(0, self.width - 1)
                        cy = random.randint(0, self.height - 1)
                        flo = flora_species[species[0]]

                        if self.environment[cy][cx] in flo[0]:

                            starting_fruit_amount = int(flo[1] * STARTING_FRUIT_RATIO) 
                            if random.random() < (flo[1] * STARTING_FRUIT_RATIO) % 1:
                                starting_fruit_amount += 1
                            bud = Flora(flora_id, [flo[1], flo[2], flo[3]], self, cx, cy, flo[4], starting_fruit_amount)    #could make eg bushes cluster together, bush dwellers, vbush camoflage, sim. give animas foresight to see which terrain they will step into, weightings toward preferred terrains, and camo in certain terrains, simulates stealth/ambush
                            self.elements[0].append(bud)
                            self.environment[cy][cx] = species[0] + str(flora_id)                                   #does this mess too much with terrain effects, ie amphibian factor in water, discrete object of whole tile taken up by plant...
                            self.spatialhash.add_element(bud)

                            flora_id += 1
                            iteration_count = MAX_FLORA_GENERATION_ITERATION_COUNT

                        iteration_count += 1
                    
    def realm_report(self):
        return 0

    def status(self):
        return [self.check_water(), self.check_ice(), self.elements, self.graveyard]
    
    def check_grass(self):
        return self.__check_nat_element(0)
    
    def check_water(self):
        return self.__check_nat_element(1)
    
    def check_ice(self):
        return self.__check_nat_element(2)
        
    def __check_nat_element(self, nat_element):
        count = 0
        for row in self.environment:
            for tile in row:
                count += 1 if tile == terrain_index[nat_element] else 0
        ratio = count/(self.width * self.height)
        return ratio
    
    def __count_nat_element(self, nat_element):
        count = 0
        for row in self.environment:
            for tile in row:
                count += 1 if tile == terrain_index[nat_element] else 0
        return count

    def count_flora(self):
        """count = 0
        for element in [entity for group in self.elements for entity in group]:
            if isinstance(element, Flora):
                count += 1"""
        return len(self.elements[0])
    
    def flora_id(self):
        return self.count_flora() + len(self.graveyard[0])

    def count_anima(self):
        """count = 0
        for element in [entity for group in self.elements for entity in group]:
            if isinstance(element, Anima):
                count += 1"""
        return len(self.elements[1])
    
    def anima_id(self):
        return self.count_anima() + len(self.graveyard[1]) + len(self.ghostyard[1])


    def add_element(self, element):
        if isinstance(element, Flora):
            self.elements[0].append(element)
        elif isinstance(element, Anima):
            self.elements[1].append(element)
            
            self.database.append_groups_by_diet(element)
        self.spatialhash.add_element(element)
        element.realm = self
    
    def add_elements(self, elementListToAdd):
        for element in elementListToAdd:
            self.add_element(element)
    
    def bury_element(self, element):
        #self.spatialhash.bury_element(element)      maybe spatial hash no longer has to perform checks?
        if isinstance(element, Flora):
            self.elements[0].remove(element)
            self.graveyard[0].append(element)
        elif isinstance(element, Anima):
            self.elements[1].remove(element)
            self.graveyard[1].append(element)

            self.database.remove_groups_by_diet(element)
    
    def ascend_element(self, element):
        self.spatialhash.remove_element(element)
        if isinstance(element, Flora):
            self.graveyard[0].remove(element)
            self.ghostyard[0].append(element)
        elif isinstance(element, Anima):
            self.graveyard[1].remove(element)
            self.ghostyard[1].append(element)

    def bury_elements(self, element_list):
        for element in element_list:
            self.bury_element(element)
    
    def ascend_elements(self, element_list):
        for element in element_list:
            self.ascend_element(element)

    def tick(self):
        #increment time for all elements
        for flora in self.elements[0]:
            flora.tick()
        for anima in self.elements[1]:
            anima.tickThink()
        for anima in self.elements[1]:
            anima.tickAct()
            if CONSOLE_ON == True:
                pass
        for anima in self.elements[1]:
            anima.tickRespond()

        for anima in self.graveyard[1]:
            anima.tickDecay()

        self.spatialhash.tock(self.elements[1])

        for anima in self.elements[1]:
            if anima.is_dead():

                #trigger death lines
                self.bury_element(anima)
                #anima.end()
                poison_obituary = ""
                if anima.is_poisoned():
                    poison_obituary = " while poisoned"
                print(f"{anima.nickname} died of {anima.autopsy()} aged {to_display(anima.age)}{poison_obituary}. Its final status was {to_display(anima.status)} and it was the parent of {[offspring.nickname for offspring in anima.offspring]}")

                self.database.increment_death_causes(anima.autopsy_index())

        for anima in self.graveyard[1]:
            if anima.food_chunks == 0:
                print(f"{anima.nickname}'s body has fully decayed.")
                self.ascend_element(anima)
                #move to heaven list and remove from spatial hash

        self.time += 1

def create_realm_name():
    return generate_nickname("realm").get_alias()
            


def construct_from_biome(biome, name, width, height, primordialList=None):
    if primordialList == ["default"]:
        primordialList = [creatures[creature] for creature in biome.native_fauna] #***
    
    return Realm(name, width, height, temperature = biome.temperature, wetness = biome.wetness, iceness = biome.iceness, floraness = biomeSCALEBYAREA)
    


#(self, name, width, height, temperature, wetness, iceness, floraness, primordialList, creature_naming_mode):
        


"""console_action_index = {        #leave for now due to eat complications, also anima needs a reference- class vs instance methods
    Anima.do_nothing : None,
    Anima.eat : None,
    Anima.drink : f"{anima.nickname} drank...",
    Anima.sleep : f"Shhh! {self.nickname} is sleeping...",
}"""