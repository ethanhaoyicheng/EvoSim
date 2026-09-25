from cell import Cell
from extratraits import ExtraTraits, trait_costs
from flora import Flora
from angle import *
from nickname import *
from todisplay import *
import random
from math import sqrt, hypot


#import numpy as np

MIN_DISTANCE_TO_TARGET = 0.05

TERRAIN_FACTOR_WEIGHTED_SUM = 1
GRASS_BIAS = 5
WATER_BIAS = 2

CONSUMPTION_POWER_FACTOR = 0.75

AWAKENING_COST = 2.5 #this is the extra sleep status amount added to sleep debt on being awakened while still asleep

DAMAGE_FACTOR = 5
RANDOM_DAMAGE_FACTOR = 0.2
INK_SHOT_RANGE = 8

BOOST_EXPENSE = 1.2   #should scale as a ratio to normal food expense ***
BOOST_EQUILIBRIUM = 0.25

MAXIMUM_MATING_DRIVE = 75
TWIN_ODDS = 0.025
TWINS_IDENTICAL_ODDS = 0.25

INHERITANCE_TYPE = "binary"
MUTATION_FACTOR = 0.1   #average mutation factor ; default 0.05
DIET_MUTATION_PLUS_FACTOR = 0 #chance of newborn gaining new diet type given they inherited at least one type from parents 0.1
DIET_PRESERVATION_FACTOR = 0.96 #chance of diet element being preserved to child, given parent 0.95
HYBRID_DIETS_ON = False
MIN_GENE_LIMIT = 0.05
MAX_GENE_LIMIT = 500

EXTRA_TRAIT_MUTATION_ODDS = 0.02
EXTRA_TRAIT_ROLLS = 4
EXTRA_TRAIT_PRESERVATION_FACTOR = 0.8

SENESCENCE_AGE = 250 #was 1000 but now scales with square root of size

MEAT_CHUNK_SIZE = 3
MEAT_SIZE_SCALE_POWER_FACTOR = 1
CORPSE_DECAY_RATE = 0.1 # = probability of decay on each tick; first decay and decrease until <1
#decay was 0.05

extra_traits = [
    "egg-laying",
    "claws",
    "flippers",
    "abrupt-wanderer",
    "poisonous",
    "venomous",
    "pincers",
    "snowycloak",
    "strong-gut",
    "sand-attack",
    "spiritful-child",
    "inky-shot",
    "berserker",
    "vampirism",
    "zombie",
    "gluttonous-child",
    "necro-mimicry",
    "absorb-victim",
    "mimic-attack",
    "leviathan",
    "play-dead",
    "plate-armour",
    "growth-syndrome",
]

food_list = [
    "apple",
    "berry",
    "melon",
    "lily",
    "lavendar",
    "meat",
    "wildgrass",
]

green_food_list = food_list.copy()
green_food_list.remove("meat")

class Anima(Cell):

    def __init__(self, id, naming_mode, genome, realm, spawnx, spawny):

        super().__init__(realm, spawnx, spawny)

        self.id = id
        
        self.angle = random.uniform(0, 2 * PI)
        self.roam_angle = random.uniform(0, 2 * PI)
        self.dx = 0
        self.dy = 0

        self.age = 0
        self.status = [25,25,0,0,-999] #hunger, thirst, sleepiness, damage, mating drive (genetic) cannot be >80
        self.target = None
        self.action = [self.do_nothing,self.do_nothing]
        self.rejectedList = []
        self.eatenList = []
        self.offspring = []
        self.parents = []
        self.goals = [] 
        self.mode = 1 # 0 sleep 1 roam 2 approach 3 flee

        self.locked = False
        self.fleeing = False
        self.hunting = False
        self.post_hunt = False

        self.conditions = []
        self.responses = []

        self.asleep = False
        self.sleep_debt = 0
        self.dream = self.do_nothing #***

        self.genome = genome
        self.diet = genome[0]
        self.speed = genome[1][0]

        self.terrain_factor_sum = genome[1][1][0] * GRASS_BIAS + genome[1][1][1] * WATER_BIAS + genome[1][1][2]
        self.grass_factor = genome[1][1][0]/self.terrain_factor_sum * TERRAIN_FACTOR_WEIGHTED_SUM
        self.amphibian_factor = genome[1][1][1]/self.terrain_factor_sum * TERRAIN_FACTOR_WEIGHTED_SUM
        self.ice_factor = genome[1][1][2]/self.terrain_factor_sum * TERRAIN_FACTOR_WEIGHTED_SUM

        self.turnspeed = genome[2]
        self.vision = genome[3]
        self.strength = genome[4]
        self.toughness = genome[5]
        self.birth_size = self.size()

        self.mating_drive = genome[6]
        self.boost_factor = genome[7]
        self.injury_threshold = genome[8]
        self.maturity_age = genome[9]
        self.senescence_age = (SENESCENCE_AGE + self.maturity_age) * sqrt(self.size())
        self.refractory = genome[10]
        self.extra_traits = genome[11]
        self.reach = 2.5

        self.food_given = "meat"
        self.food_effect = [(-MEAT_CHUNK_SIZE * 100),0,0,(-MEAT_CHUNK_SIZE * 3),MEAT_CHUNK_SIZE * 20]
        self.food_chunks =  int((self.size()-1)**MEAT_SIZE_SCALE_POWER_FACTOR/MEAT_CHUNK_SIZE) + 1 #equivalent to fruitNo, could merge

        self.alias = None
        self.nickname = self.create_nickname(naming_mode)  #dependent on realm

    def tickThink(self):
        self.responses.append(self.unlock)
        self.setGoals()
        self.choose_mode()
        self.set_velocity()     #sets velocity and action

       
        #check if can mate

        #method sets private states: dx, dy, target, mode
        
    
    def tickAct(self):
        self.asleep = False
        self.action[1](self.target)
        self.move()   
        self.increment_age()

        #method sets public states: asleep, status

    def tickRespond(self):
        for response in self.responses:
            response()
        self.responses = []
    
    

    def increment_age(self):

        self.update(0, 0.125 * self.energy_expense())
        #print(self.energy_expense())
        self.update(1, 0.2)  # *self.realm.temperature ?
        self.update(2, 0.04 * self.energy_expense())   #need downsides for each trait
        self.update(3,-0.1)

        conditions = self.conditions
        for condition in conditions:
            condition(self)

        if not self.is_mature():
            self.grow()
            if "spiritful-child" in self.extra_traits:
                self.update(2,-0.2)
            if "gluttonous-child" in self.extra_traits:
                self.update(0,1)
                self.grow()
        else:
            #if self.status[4] < self.mating_drive:
                #self.status[4] = min(self.mating_drive, MAXIMUM_MATING_DRIVE)
            if self.status[4] < 10:
                self.update(4, 10-self.status[4]) #should it be less?
            
            self.update(4, 0.1)

            self.update(3, -0.2)

            if "growth-syndrome" in self.extra_traits:
                self.update(0,1)
                self.grow()
        
        if self.is_senescent():
            self.update(3, 0.1)

        self.age += 1

    def energy_expense(self):
        return (0.04 * self.vision**2)/sqrt(self.size()) + self.energy_expense_by_moving() + 1.5 + min(0.25/self.realm.temperature, 2) + self.energy_expense_by_extra_traits() #should vision be sqrt or not?
        #energy is expended by 1. vision/senses 2. movement 3. general expenses 4. heating 5. extra traits
    
    def energy_expense_by_moving(self):
        if self.realm.environment[int(self.y)][int(self.x)] in terrain_energy_expenditure:
            terrain_cost = terrain_energy_expenditure[self.realm.environment[int(self.y)][int(self.x)]]
        else:       #for floras
            terrain_cost = terrain_energy_expenditure["grass"]
        return hypot(self.dx, self.dy) * terrain_cost * sqrt(self.speed)

    def energy_expense_by_extra_traits(self):
        return sum([trait_costs[trait] for trait in self.extra_traits.traits]) * (1.005 ** len(self.extra_traits)) #physical overload factor
        
    def grow(self):
        self.strength += 0.025
        self.toughness += 0.025

    def round_status(self):         #for displaying
        #status = [round(need) for need in self.status]
        return round_list(self.status)
    
    def genome_to_display(self):
        return to_display(self.genome)
    
    def size(self):
        return sqrt(self.strength * self.toughness)   #should size affect eating? various implications

    def diet_type(self):
        if "meat" in self.diet:
            if len(self.diet) == 1:
                return "carnivore"
            else:
                return "omnivore"
        return "herbivore"
    
    
    def will_sleep(self):
        return self.status[2] >= 100 or (self.mode == 0 and self.status[2] >= max(self.status[0], self.status[1]))

    def setGoals(self):
    #this method updates the goals of the associated anima, creating a new empty list and appending at least one int element goal; the greatest need is appended first, then if the second greatest need is close enough in urgency then it is appended too, and so on
    #per tick
                
        self.goals = []
        needs = self.status[:]
        needs[2] = 0        #for now, sleepiness will not affect priority of other needs
        
        if self.post_hunt:
            if needs[0] >= 10 and isinstance(self.target, Anima):          #1 tick delay
                needs[0] = 100
            else:
                self.post_hunt = False
                print(f"{self.nickname} has finished its meal")

        prevGreatestNeed = 0

        for _ in range(len(needs)):
            greatestNeed = needs.index(max(needs))
            if needs[greatestNeed] > prevGreatestNeed - 1.5 * sqrt(abs(100-prevGreatestNeed)):
                self.goals.append(greatestNeed)
                prevGreatestNeed = needs[greatestNeed]
                needs[greatestNeed] = -9999
        return

    def choose_mode(self): 
    #this method updates the mode of the associated anima based on anima logic, setting the int variable mode to the correct value (0:sleep/1:roam/2:approach/3:flee)
    #per tick
        self.hunting = False        #hunting timer

        if self.will_sleep():
            self.mode = 0
            
        else: 
            self.mode = 1

            none_means_fleeing = self.checkSurroundings()
            
            if self.target != None:
                self.mode = 2

            if none_means_fleeing == None and self.target != None:   #currently fleeing ends as soon as cannot see predator
                self.mode = 3
                self.fleeing = True


    def set_action(self, action=None):  #why wasnt tiggerinbg mate eaelier before code fix of simply moving to making set action to be less accessible?
        action_index = {
                            None : [self.do_nothing,self.do_nothing],
                            0 : [self.do_nothing,self.eat],
                            1 : [self.do_nothing,self.drink],
                            #2 : [self.do_nothing,self.sleep],
                            4 : [self.lock_mate,self.mate],
                        }

        if self.mode == 0:
            return [self.do_nothing,self.sleep]
        elif self.mode == 1:
            return [self.do_nothing,self.do_nothing]
        elif self.hunting:                                          #subset of mode 2 where target is not in reach and is a prey food
            return [self.do_nothing,self.set_hunting_action()]
        elif self.mode == 2:
            return action_index[action]
        elif self.mode == 3:
            return [self.do_nothing, self.set_fight_or_flight()]  #next: fight or flight (speed boost)
    
    def set_fight_or_flight(self):
        if "inky-shot" in self.extra_traits and self.distance_to(self.target) < INK_SHOT_RANGE:      #check inkbag also
            return self.ink_shot

        if (self.strength > self.target.toughness and not self.is_injured()) or self.locked or "berserker" in self.extra_traits:
            if self.is_target_in_reach():
                return self.fight
            else:
                return self.do_nothing
        else:
            return self.boost
    
    def set_hunting_action(self):
        if self.is_target_in_reach():
            return self.eat
        elif self.is_starving():
            return self.boost
        return self.do_nothing
    
    def is_target_in_reach(self):
        tx, ty = self.get_target_x(), self.get_target_y()                   #direct centre targetting problem, with high resolution is negligible
        return self.is_within_point(tx,ty,self.reach)

    def checkSurroundings(self):              #checks surroundings and sets target
        vision_modifier = 1

        for _ in range(min(10, self.conditions.count(blind))):
            vision_modifier *= 0.8

        vision = self.vision * vision_modifier

        self.cells_to_check = []

        for dy in range(int(2*vision+1)):      #future: raycasting prevents animas seeing through objects
            row = (int(self.y - vision) + dy) % self.realm.height
            for dx in range(2*int(vision)+1):
                col = (int(self.x - vision + 0.5) + dx) % self.realm.width
                if self.distance_to_point(col, row) <= vision:
                    self.cells_to_check.append((row, col))
                
        target = self.__check_for_danger(vision)
        if target == None:
            for goal in self.goals:
                
                pass #if visible

                if target == None:
                    target = self.check_for(goal, vision)
                    if target != None:
                        self.target = target
                        if goal == 0 and isinstance(target, Anima):
                            self.hunting = True
                        return goal
                                  #should modes be changed outside choosemode?
        self.target = target 
        return None
        #return False

    

    def check_for(self, goal, vision):
        if goal == 0:
            target = self.__check_for_food(vision)
        elif goal == 1:
            target = self.__check_for_water(vision)
        elif goal == 2:
            #self.__check_for_shelter
            target = None
        elif goal == 3:
            #flee?
            target = None
        elif goal == 4:
            target = self.__check_for_mates(vision)
        return target

    def __check_for_food(self, vision):
        nearest_food = None
        nearest_dist = vision 

        for element in self.check_spatial_hash(vision):
            if not element in self.eatenList and element.food_given in self.diet and not self.is_family(element) and not (isinstance(element, Flora) and element.fruitNo == 0):  #allow children to eat parents?
                dist = self.distance_to(element)
                if dist <= nearest_dist:    #vision for emergency clamping
                    if not isinstance(element, Anima) or self.is_threat_to(element) or element.is_dead(): #logical OR short circuits  //self.toughness > element.strength or
                        nearest_dist = dist
                        nearest_food = element 

        #if nearest_food == None and "grass" in self.diet:

        return nearest_food

    def __check_for_water(self, vision):
        nearest_water = None
        nearest_dist = vision + 1

        for pos in self.cells_to_check:
            if self.realm.environment[pos[0]][pos[1]] == "water":
                dist = self.distance_to_point(pos[1], pos[0])
                if min(dist, nearest_dist, vision) == dist:    #vision for emergency clamping
                    nearest_dist = dist
                    nearest_water = (pos[1],pos[0])   
        return nearest_water
    
    def __check_for_mates(self, vision):
        nearest_mate = None
        nearest_dist = vision + 1
        
        for element in self.check_spatial_hash(vision):
            if not element in self.rejectedList and isinstance(element, Anima) and not element == self :         #prevent children and parents?
                dist = self.distance_to(element)                                        
                if min(dist, nearest_dist, vision) == dist:    #vision for emergency clamping
                    if 4 in element.goals and not self.is_threat_to(element) and not self.is_threatened_by(element) and not element.asleep and not element.fleeing:
                        nearest_dist = dist
                        nearest_mate = element 
                    elif not (not self.is_threat_to(element) and not self.is_threatened_by(element)) :
                        self.rejectedList.append(element)  
        return nearest_mate
    
    def __check_for_danger(self, vision):
        nearest_danger = None
        nearest_dist = vision + 1

        for threat in self.check_spatial_hash(vision):
            if isinstance(threat, Anima):
                dist = self.distance_to(threat)
                if min(dist, nearest_dist, vision) == dist:    #vision for emergency clamping  
                    if  self.is_threatened_by(threat):
                        nearest_dist = dist
                        nearest_danger = threat
        return nearest_danger

    def check_spatial_hash(self, vision):
        return self.realm.spatialhash.get_neighbours(self.x, self.y, vision)
    
    def is_threatened_by(self, threat): #so there is a 1-tick wake up grace period
        return isinstance(threat, Anima) and not threat.is_dead() and not threat.asleep and (not threat.is_injured() or threat.status[0] > threat.status[3]) and ((threat.strength > self.toughness) or self.is_injured()) and "meat" in threat.diet and not self.is_family(threat) 
     
    def is_threat_to(self, other): 
        return isinstance(other, Anima) and other.is_threatened_by(self) 
            
    def set_velocity(self):
        true_angle = 0
        speed_modifier = 1 - (self.status[3])/120
        self.action = self.set_action()

        if "plate-armour" in self.extra_traits:
            speed_modifier *= 0.75

        if self.locked:
            speed_modifier = 0

        elif self.mode == 0:
            speed_modifier = 0
        
        # can do slowing down when approaching object

        elif self.mode == 1:
            if "abrupt-wanderer" in self.extra_traits:
                if random.uniform(0,1) < 0.05:
                    self.roam_angle = random.uniform(0, 2 * PI)
            else:
                self.roam_angle += random.uniform(-0.07, 0.07)
                if random.uniform(0,1) < 0.1:
                    self.roam_angle += random.uniform(-0.8, 0.8)
                if random.uniform(0,1) < 0.015:
                    self.roam_angle = random.uniform(0, 2 * PI)
                self.roam_angle = self.roam_angle % (2*PI)

            true_angle = self.roam_angle
        
            """
            dx_t = self.target.x - self.x
dy_t = self.target.y - self.y
dist = math.hypot(dx_t, dy_t)

if dist > 0:
    speed = min(self.speed, dist)
    self.dx = speed * dx_t / dist
    self.dy = speed * dy_t / dist
else:
    self.dx = self.dy = 0
            """
        
        elif self.mode == 2:

            if self.is_target_in_reach():
                speed_modifier = 0
                self.action = self.set_action(self.checkSurroundings())
                self.action[0](self.target)                                 #should this be here?***
            else:
                """dsx = self.get_target_x() - self.x
                dsy = self.get_target_y() - self.y
                true_angle = atan2(dsy, dsx)"""

                true_angle = self.angle_to(self.target)
                
        
        elif self.mode == 3: #flee
            """dsx = self.get_target_x() - self.x
            dsy = self.get_target_y() - self.y
            true_angle = (atan2(dsy, dsx) + math.pi) % (2 * math.pi)"""
            true_angle = self.target.angle_to(self)

            #reset roam angle upon fleeing (to prevent repeatedly running back toward predator once out of vision range)
            self.roam_angle = random.uniform(0, 2 * PI)
            self.roam_angle = self.roam_angle % (2*PI)

        if self.realm.environment[int(self.y)][int(self.x)] == "grass":
            speed_modifier = speed_modifier * (1 + self.grass_factor)
            if "flippers" in self.extra_traits:
                speed_modifier *= 0.75

        if self.realm.environment[int(self.y)][int(self.x)] == "water":  #should round it
            speed_modifier = speed_modifier * (0.5 + self.amphibian_factor)
            if "flippers" in self.extra_traits:
                speed_modifier *= 2

        if self.realm.environment[int(self.y)][int(self.x)] == "ice":
            speed_modifier = speed_modifier * self.ice_factor

        self.angle = self.angle + lerple(self.angle, true_angle, self.turnspeed)
        self.dx = self.speed * cos(self.angle) * speed_modifier
        self.dy = self.speed * sin(self.angle) * speed_modifier

        """if  self.target != None and (self.y + self.dy - self.get_target_y()) * (self.y - self.get_target_y()) < 0:
            self.dy = self.get_target_y() - self.y - MIN_DISTANCE_TO_TARGET * (2*int(self.get_target_y() > self.y) - 1)
        if  self.target != None and  (self.x + self.dx - self.get_target_x()) * (self.x - self.get_target_x()) < 0:
            self.dx = self.get_target_x() - self.x - MIN_DISTANCE_TO_TARGET * (2*int(self.get_target_x() > self.x) - 1)"""
        
        if self.target != None and self.speed * speed_modifier > self.distance_to(self.target):
            self.dy = self.get_target_y() - self.y - MIN_DISTANCE_TO_TARGET * (2*int(self.get_target_y() > self.y) - 1)
            self.dx = self.get_target_x() - self.x - MIN_DISTANCE_TO_TARGET * (2*int(self.get_target_x() > self.x) - 1)
    
    def get_target_x(self):
        if isinstance(self.target, Cell):
            tx = self.target.x
        elif isinstance(self.target, tuple):
            tx = self.target[0]                    #direct centre targetting problem, with high resolution is negligible
        return tx

    def get_target_y(self):
        if isinstance(self.target, Cell):
            ty = self.target.y
        elif isinstance(self.target, tuple):
            ty = self.target[1]                    #direct centre targetting problem, with high resolution is negligible
        return ty


    def move(self, factor = 1):
        self.x += self.dx
        self.y += self.dy
        #temporary solution to edge of map logic
        if not 0 <= self.x < self.realm.width:
            self.x = self.x % self.realm.width
        if not 0 <= self.y < self.realm.height:
            self.y = self.y % self.realm.height
    
    def boost(self, _ = None):
        self.move(self.boost_factor)
        self.update(0, max(BOOST_EXPENSE / BOOST_EQUILIBRIUM * (self.boost_factor**2) * self.energy_expense_by_moving(), BOOST_EXPENSE * self.boost_factor * self.energy_expense_by_moving()))
        print(f"{self.nickname} is boosting to get away from {self.target.nickname}")
        
     
    def fight(self, anima):
        #damage = DAMAGE_FACTOR * (1+random.uniform(-2*RANDOM_DAMAGE_FACTOR,2*RANDOM_DAMAGE_FACTOR)) * (self.strength/anima.toughness + max(0, (self.strength-anima.toughness)))  #factor method??? returning this to use with all random factors
        damage = max(1, DAMAGE_FACTOR * (1+random.uniform(-2*RANDOM_DAMAGE_FACTOR,2*RANDOM_DAMAGE_FACTOR)) * (self.strength/anima.toughness))
        if anima.is_injured():
            damage = damage * 1.15 + 2
        if "plate-armour" in self.extra_traits:
            damage = damage * 0.5
        anima.take_damage(damage)
        print(f"{self.nickname} struck {self.target.nickname} and dealt {to_display(damage)} damage")
        
        if anima.asleep:
            anima.responses.append(self.awaken)
        
        attacks = self.extra_traits #self.extra_traits.attack()

        if "mimic-attack" in self.extra_traits:
            attacks.extend(anima.extra_traits.traits)

        if "pincers" in attacks and self.strength > anima.toughness:
            self.grab(anima)
        
        if "claws" in attacks and random.random() < (self.strength - anima.toughness)/anima.toughness:
            anima.conditions.append(bleed)
            anima.conditions.append(bleed)
        
        if "venomous" in attacks:
            anima.conditions.append(define_poison(5 * self.strength / anima.toughness, "strong-gut" in anima.extra_traits))
        
        if "sand-attack" in attacks:
            anima.conditions.append(blind)
        
        
            
        
    def take_damage(self, amount):
        self.update(3, amount)
        
    def grab(self, target):
        angle = self.angle_to(target)
        r = self.reach * 0.9
        if self.distance_to(target) > r:
            x = self.x
            y = self.y
            def set_position():
                target.x = x + r * cos(angle)
                target.y = y + r * sin(angle)
            target.responses.append(set_position)
        target.responses.append(target.lock)
        self.responses.append(self.lock)
    
    def ink_shot(self, target):
        if random.random() < 0.5:
            target.conditions.append(blind)

    def is_family(self, anima):
        #check immediate family, ie direct children or parents
        return anima in self.offspring or anima in self.parents or anima == self
    
    def is_satiated(self):
        return self.status[0] < 35
    
    def is_starving(self):
        return self.status[0] > 72.5
        
    def is_injured(self):
        return self.status[3] > self.injury_threshold
    
    def is_bleeding(self):
        return any(getattr(condition, "effect_type", None) == "bleed" for condition in self.conditions)
    
    def is_poisoned(self):
        return any(getattr(condition, "effect_type", None) == "poison" for condition in self.conditions)
    

    #def sick():

    def is_mature(self):
        return self.age >= self.maturity_age

    def is_senescent(self):
        return self.age >= self.senescence_age

    def is_dead(self):  
        return False
        if any(need >= 100 for i,need in enumerate(self.status) if i != 2):  #except sleep?
            return True
        return False
    
    def autopsy(self):
        for i in range(len(self.status)):
            if not i == 2 and self.status[i] >= 100:    #cannot die of sleepiness
                return cause_of_death_index[i]
        #age
        return "unknown causes"
    
    def autopsy_index(self):
        for i in range(len(self.status)):
            if not i == 2 and self.status[i] >= 100:
                return i
        
        return None
    
    #mortuary


    def update(self, need, quantity, sign=1):
        if need == 3 and quantity*sign < 0 and self.is_senescent():
            return

        if need == 4 and not self.is_mature():
            return
        
        elif need == 4 and self.status[4] + quantity*sign > MAXIMUM_MATING_DRIVE:
            self.status[4] = MAXIMUM_MATING_DRIVE
            return

        self.status[need] += quantity * sign
        if self.status[need] < 0:
            self.status[need] = 0

    def do_nothing(_ = None, __ = None):
        pass

    def eat(self, source, quantity = 1): #currently eating takes only 1 tick
        if source in self.realm.elements[1]:
            self.fight(source)
            self.responses.append(self.check_prey)
        else: 
            quantity_eaten = source.provide(quantity)
            effect_modifier = quantity_eaten / (self.birth_size**CONSUMPTION_POWER_FACTOR) / sqrt(len(self.diet)+0.25)
            for need in range(len(source.food_effect)): 
                self.update(need,source.food_effect[need] * effect_modifier)    #should be sqrt or not?
            if source.food_given == "meat":
                if "poisonous" in source.extra_traits:
                    if random.random() < 0.25:
                        self.conditions.append(define_poison(12, "strong-gut" in self.extra_traits))
                if "vampirism" in self.extra_traits:
                    for i in range(4):
                        self.drink()
            else:
                self.eatenList.append(source)
            print(f"{self.nickname} ate " + source.food_given)
    

    def drink(self, _ = None):
        self.update(1,-5)
        #print(f"{self.nickname} drank...")

    def sleep(self, _ = None):
        self.asleep = True
        self.update(2, self.sleep_debt)
        self.sleep_debt = 0

        self.update(2,-3)  #sleepiness is reduced inversely with vision
        self.update(3,-1.5)
        self.rejectedList = []
        self.eatenList = []

        self.dream()
        #print(f"Shhh! {self.nickname} is sleeping...")

    def get_sleepiness(self):
        return self.status[2]
    
    def awaken(self):   #response
        self.sleep_debt = max(AWAKENING_COST, self.status[2] - max(self.status[0], self.status[1], self.status[4]))
        self.update(2,-self.sleep_debt+AWAKENING_COST)
        print(f"{self.nickname} was startled awake!") 
    
    def check_prey(self):   #response
        if self.target.is_dead():
            self.post_hunt = True
            if "absorb-victim" in self.extra_traits and self.target.extra_traits:
                self.extra_traits.add(random.choice(list(self.target.extra_traits)))
                self.extra_traits.correct_traits()

    def mate(self, mate):
        """new_genome = self.mix_genomes(mate)

        newborn = Anima(self.realm.anima_id(), self.realm.creature_naming_mode, new_genome, self.realm, self.x, (self.y+1)%self.realm.height)   #random adjacent cell?  #sad that cannot isolate from realm for this line
        newborn.parents.extend([self, mate])
        self.offspring.append(newborn)
        mate.offspring.append(newborn)
        self.realm.add_element(newborn)
        #refractory impacts newborn state

        while random.random() < TWIN_ODDS:
            if random.random() < TWINS_IDENTICAL_ODDS:
                identical_newborn = Anima(self.realm.anima_id(), self.realm.creature_naming_mode, new_genome, self.realm, (self.x+1)%self.realm.width, self.y)
                identical_newborn.parents.extend([self, mate])
                self.offspring.append(identical_newborn)
                mate.offspring.append(identical_newborn)
                self.realm.add_element(identical_newborn)
                print(f"{newborn.nickname} and {identical_newborn.nickname} are identical twins!")
            else:
                new_genome = self.mix_genomes(mate)
                twin_newborn = Anima(self.realm.anima_id(), self.realm.creature_naming_mode, new_genome, self.realm, (self.x+1)%self.realm.width, (self.y+1)%self.realm.height)   #random adjacent cell?  #sad that cannot isolate from realm for this line
                twin_newborn.parents.extend([self, mate])
                self.offspring.append(twin_newborn)
                mate.offspring.append(twin_newborn)
                self.realm.add_element(twin_newborn)
                print(f"{newborn.nickname} and {twin_newborn.nickname} are twins!")"""


        self.update(2,50)
        self.update(3,25)
        self.update(4,-(self.refractory+5))
        mate.update(2,50)
        mate.update(3,25)
        mate.update(4,-(mate.refractory+5))
        mate.locked = False

        print(f"{newborn.nickname} was born to {self.nickname} and {mate.nickname}!")

    def lock_mate(self, mate):
        mate.locked = True
    
    def unlock(self):
        self.locked = False
    
    def lock(self):
        self.locked = True

    def mix_genomes(self, mate):
        """new_genome = []
        for genotype in range(len(self.genome)):
            if isinstance(self.genome[genotype], list):
                new_genome.append([])
                for gene in range(len(self.genome[genotype])):              #incompatible with list diet and list speeds
                    new_genome[genotype].append(mix_genes(type(self.genome[genotype][gene]),self.genome[genotype][gene],mate.genome[genotype][gene]))
            else:
                new_genome.append(mix_genes(type(self.genome[genotype]), self.genome[genotype], mate.genome[genotype]))  """ 
        new_genome =  mix_genes(list, self.genome[:], mate.genome[:], realm_foods(self.realm))
        return new_genome

    def reproduce(self):
        #append to self.offspring
        pass
    
    def provide(self, quantity = 1):
        quantity_provided = min(quantity, self.food_chunks)
        self.food_chunks -= quantity_provided
        return quantity_provided
    
    def tickDecay(self):            #very basic for now
        corpse_to_decay = CORPSE_DECAY_RATE
        while corpse_to_decay >= 1:
            self.food_chunks -= 1
            corpse_to_decay -= 1
        if random.random() < corpse_to_decay:
            self.food_chunks -= 1

    def create_nickname(self, naming_mode):
        nickname_structure = naming_mode.split("/")
        #print(nickname_structure)
        nickname = ""
        for mode in nickname_structure:
            #print(mode)
            #print(vars(self))
            if mode in ["", "nameless"]:
               nickname += "A creature"
            elif mode in ["random", "surprise", "name"]:
               self.alias = generate_nickname("anima")
               nickname += self.alias.get_alias()
            elif mode == "story":
               #nickname += random story name
               pass
            elif mode in vars(self):
                nickname += to_display(getattr(self, mode))
            else:
                pass
            nickname += " "
        nickname = nickname[:len(nickname)-1]

        return nickname
    
    def get_alias(self):
        return self.alias.get_alias()

    def update_nickname(self):
        pass        
    
    
    def name_me(self):
        pass

#should've made genome a class maybe
def mix_genes(gene_type, A, B, food_options = food_list):
    if gene_type == tuple:              #diet must be only tuple
        new_gene = ()
        if random.uniform(0,1) < 0.1 and HYBRID_DIETS_ON == True:                                        #omnivore
            for item in A:
                if item not in new_gene and random.uniform(0,1) < DIET_PRESERVATION_FACTOR:
                    new_gene = new_gene + (item,)
            for item in B:
                if item not in new_gene and random.uniform(0,1) < DIET_PRESERVATION_FACTOR:
                    new_gene = new_gene + (item,)
        else:                                                                                            #elif random.uniform(0,1) < 0.95
            for item in random.choice([A, B]):
                if item not in new_gene and random.uniform(0,1) < DIET_PRESERVATION_FACTOR:
                    new_gene = new_gene + (item,)
        if new_gene == () or (random.uniform(0,1) < DIET_MUTATION_PLUS_FACTOR and HYBRID_DIETS_ON):
            new_gene = new_gene + (random.choice([food for food in food_options if food not in new_gene]),)
        return new_gene
    
    elif gene_type == ExtraTraits:
        new_gene = ExtraTraits(set())
        atraits = list(A.traits)
        btraits = list(B.traits)
        traits = []
        while atraits or btraits:
            if random.random() < 0.5 and atraits:
                traits.append(atraits.pop())
            elif btraits:
                traits.append(btraits.pop())
        for trait in traits:
            if random.random() < EXTRA_TRAIT_PRESERVATION_FACTOR/(len(new_gene)+1) and trait not in new_gene:
                new_gene.add(trait)
        for roll in range(EXTRA_TRAIT_ROLLS):
            if random.random() < EXTRA_TRAIT_MUTATION_ODDS:
                new_gene.add(random.choice(extra_traits))
        new_gene.correct_traits()
        return new_gene
    
    elif gene_type == int:
        #new_gene = (A+B)/2 * (1 + random.uniform(-2,2) * MUTATION_FACTOR)
        if INHERITANCE_TYPE == "mean":
            new_gene = random.gauss(((A+B)/2), (MUTATION_FACTOR*(A+B)/2))
        elif INHERITANCE_TYPE == "binary":
            G = random.choice((A,B))
            new_gene = random.gauss(G, MUTATION_FACTOR*G)
        new_gene = max(new_gene, MIN_GENE_LIMIT)
        new_gene = min(new_gene, MAX_GENE_LIMIT)                                   #should i set limits for each gene specifically? would require overhaul of this and use of a dictionary
        return int(round(new_gene))

    elif gene_type == float:
        #new_gene = (A+B)/2 * (1 + random.uniform(-2,2) * MUTATION_FACTOR)
        if INHERITANCE_TYPE == "mean":
            new_gene = random.gauss(((A+B)/2), (MUTATION_FACTOR*(A+B)/2))
        elif INHERITANCE_TYPE == "binary":
            G = random.choice((A,B))
            new_gene = random.gauss(G, MUTATION_FACTOR*G)
        #new_gene = random.gauss((A+B/2), MUTATION_FACTOR)
        new_gene = max(new_gene, MIN_GENE_LIMIT)
        new_gene = min(new_gene, MAX_GENE_LIMIT)                                   #should i set limits for each gene specifically? would require overhaul of this and use of a dictionary
        return float(new_gene)

    elif gene_type == list:
        return [mix_genes(type(a), a, b, food_options) for a, b in zip(A, B)]
    
    raise ValueError(f"Genotype must be one of the given data types; Invalid type {gene_type}")

def bleed(this):
        this.take_damage(1)
        if random.random() < 0.15: #self.bloodclottingrate, also gene for passive healing?
            this.conditions.remove(bleed)
bleed.effect_type = "bleed"
    
def define_poison(severity, stronggut):
    def suffer_poison(this):
        nonlocal severity
        this.take_damage(severity)
        this.update(0,severity/this.size())
        this.update(1,severity/this.size())
        if random.random() < 0.15 if not stronggut else 0.3: 
            this.conditions.remove(suffer_poison)
            if severity >= 2:
                this.conditions.append(define_poison(int(severity/2), "strong-gut" in this.extra_traits))
    suffer_poison.effect_type = "poison"
    return suffer_poison

def intoxicated(this):
    if random.random() < 0.15 if not "stronggut" in this.extra_traits else 0.3: 
        this.conditions.remove(intoxicated)
intoxicated.effect_type = "intoxicated"

def blind(this):
    if random.random() < 0.15: 
        this.conditions.remove(blind)
blind.effect_type = "blind"

def realm_foods(realm):
        return [fruit.name for fruit in realm.fruit_list if fruit.name in food_list] + ["meat"]




cause_of_death_index = {
    0 : "starvation",
    1 : "thirst",
    3 : "its wounds",
}

terrain_energy_expenditure = {
    "grass" : 1,
    "water" : 1.5,
    "ice" : 2,
}