import pygame
from math import sqrt

fruit_set = {
    "apple" : "red",
    "berry" : "blue",
    "lily" : "yellow",
    "lavendar" : "purple",
    "melon" : "darkolivegreen1",
    "wildgrass" : "green",
    "bean" : "forestgreen",
}

monochrome_fruit_set = {
    "apple" : "gray89",
    "berry" : "gray97",
    "lily" : "gray89",
    "lavendar" : "gray50",
    "melon" : "gray29",
    "wildgrass" : "gray93",
    "bean" : "gray10",
}

og_set = {
    "id" : "Punk Petri (Not recommended)",
    "grass" : "green",
    "flora" : "purple",
    "fruit" : None,
    "water" : "blue",
    "child" : "yellow",
    "old"   : "yellow",
    "corpse" : "orangered",
    "adult" : "yellow",
    "meateater" : "yellow",
    "found_food" : "yellow",
    "found_water" : "yellow",
    "roam" : "yellow",
    "vision" : "yellow",
    "highlight" : "white",
}

classic_set = {
    "id" : "Classic",
    "grass" : "green",
    "flora" : "forestgreen",
    "fruit" : fruit_set,
    "water" : "blue",
    "child" : "turquoise1",
    "old"   : "white",
    "corpse" : "red4",
    "adult" : "yellow",
    "meateater" : "slateblue3",
    "found_food" : "purple",
    "found_water" : "steelblue1",
    "roam" : "dodgerblue",
    "vision" : "yellow",
    "highlight" : "yellow",
}

vibrant_set = {
    "id" : "Vibrant!",
    "grass" : "mediumspringgreen",
    "flora" : "magenta",
    "fruit" : fruit_set,
    "water" : "turquoise1",
    "child" : "green",
    "old"   : "maroon4",
    "corpse" : "red4",
    "adult" : "yellow",
    "meateater" : "violetred1",
    "found_food" : "purple",
    "found_water" : "steelblue1",
    "roam" : "dodgerblue",
    "vision" : "yellow",
    "highlight" : "yellow",
}

oceanic_set = {
    "id" : "Oceanic",
    "grass" : "seagreen1",
    "flora" : "seagreen3",
    "fruit" : fruit_set,
    "water" : "royalblue3",
    "child" : "turquoise1",
    "old"   : "white",
    "corpse" : "seashell4",
    "adult" : "yellow",
    "meateater" : "navyblue",
    "found_food" : "purple",
    "found_water" : "royalblue2",
    "roam" : "dodgerblue",
    "vision" : "yellow",
    "highlight" : "yellow",
}

demonic_set = {
    "id" : "DEMONIC",
    "grass" : "red4",
    "flora" : "red",
    "fruit" : fruit_set,
    "water" : "gold2",
    "child" : "black",
    "old"   : "gray84",
    "corpse" : "white",
    "adult" : "gray50",
    "meateater" : "purple",
    "found_food" : "purple",
    "found_water" : "gold2",
    "roam" : "dodgerblue",
    "vision" : "yellow",
    "highlight" : "yellow",
}

monochrome_set = {
    "id" : "Noir", #B&W
    "grass" : "white",
    "flora" : "gray80",
    "fruit" : monochrome_fruit_set,
    "water" : "black",
    "child" : "gray95",
    "old"   : "gray75",
    "corpse" : "white",
    "adult" : "gray85",
    "meateater" : "gray65",
    "found_food" : "gray40",
    "found_water" : "gray10",
    "roam" : "gray70",
    "vision" : "gray60",
    "highlight" : "gray60",
}

mature_set = {
    "id" : "Mature",
    "grass" : "darkolivegreen3",
    "flora" : "forestgreen",
    "water" : "dodgerblue",
    "fruit" : fruit_set,
    "child" : "green",
    "old"   : "white",
    "corpse" : "red",
    "adult" : "aquamarine",
    "meateater" : "slateblue3",
    "found_food" : "purple",
    "found_water" : "steelblue1",
    "roam" : "blue",
    "vision" : "yellow",
    "highlight" : "yellow", #magenta
}

declutter_classic_set = {
    "grass" : "green",
    "flora" : "forestgreen",
    "fruit" : None,
    "child" : "turquoise1",
    "old"   : "white",
    "corpse" : "red4",
    "adult" : "yellow",
}

declutter_mature_set = mature_set.copy()
declutter_mature_set["id"] = "Decluttered (Fruit-less)"
declutter_mature_set["fruit_set"] = None

#olivegreen?

colour_set = classic_set

colour_sets = [classic_set, mature_set, vibrant_set, oceanic_set, demonic_set, monochrome_set, declutter_mature_set, og_set,]

def set_sim_colours(colour_set):
    global GRASS_COLOUR, FLORA_COLOUR, WATER_COLOUR, CHILD_COLOUR, SENESCENT_COLOUR, CORPSE_COLOUR, MEAT_EATER_COLOUR, ADULT_COLOUR, FOUND_FOOD_COLOUR, FOUND_WATER_COLOUR, ROAM_COLOUR
    global VISION_COLOUR, HIGHLIGHT_COLOUR
    global FRUIT_COLOUR_SET

    GRASS_COLOUR = colour_set["grass"]
    FLORA_COLOUR = colour_set["flora"]
    WATER_COLOUR = colour_set["water"]
    CHILD_COLOUR = colour_set["child"]
    SENESCENT_COLOUR = colour_set["old"]
    CORPSE_COLOUR = colour_set["corpse"]
    MEAT_EATER_COLOUR = colour_set["meateater"]
    ADULT_COLOUR = colour_set["adult"]

    FOUND_FOOD_COLOUR = colour_set["found_food"]
    FOUND_WATER_COLOUR = colour_set["found_water"]
    ROAM_COLOUR = colour_set["roam"]
    
    VISION_COLOUR = colour_set["vision"]
    HIGHLIGHT_COLOUR = colour_set["highlight"]


    FRUIT_COLOUR_SET = colour_set["fruit"]

set_sim_colours(colour_set)

            
#if (a;b) and (c;d):
#   1/(ab) >= 1/(cd)
#where x;y is such that x is the time required to check condition and y is the pass rate of condition. Equilibrium where ab = cd; there order has no effect on efficiency 

def draw_world_blit(realm):

    #only use these variables here
    width = realm.width
    height = realm.height

    blit = pygame.Surface((width, height))

    blit.fill(GRASS_COLOUR)

    for row in range(height):
        for col in range(width):
            if realm.environment[row][col] == "water":
                pygame.draw.rect(blit, WATER_COLOUR, (col, row, 1, 1))
    for row in range(height):
        for col in range(width):
            if realm.environment[row][col] == "ice":
                pygame.draw.rect(blit, "white", (col, row, 1, 1))
    for flora in realm.elements[0]:
        if not flora.fruit.name in ("lavendar", "lily", "wildgrass") and FRUIT_COLOUR_SET != None:
            pygame.draw.rect(blit, FLORA_COLOUR, (round(flora.x-1), round(flora.y-1), 3, 3))
        if flora.fruit.name == "bean" and FRUIT_COLOUR_SET != None:
            pygame.draw.rect(blit, FRUIT_COLOUR_SET["bean"], (round(flora.x-1), round(flora.y-1), 3, 3))
    return blit

def draw_anima(anima, screen, cx, cy):
    bodycolour = "purple" if anima.is_poisoned() else "orangered" if anima.is_injured() else "orange" if anima.status[3] >= 25 else SENESCENT_COLOUR if anima.is_senescent() else CHILD_COLOUR if not anima.is_mature() else MEAT_EATER_COLOUR if "meat" in anima.diet else ADULT_COLOUR
    pygame.draw.circle(screen, bodycolour, (cx, cy), int(round(min(max(sqrt(anima.size()), 1), 7))))

    #spaghetti code :
    eyecolour = "gold" if anima.asleep else "black" if anima.hunting else FOUND_WATER_COLOUR if anima.mode == 2 and isinstance(anima.target, tuple) else FOUND_FOOD_COLOUR if anima.mode == 2 else "white" if anima.mode == 3 else "violet" if 4 in anima.goals else ROAM_COLOUR 
    pygame.draw.circle(screen, eyecolour, (cx, cy), int(round(min(max(sqrt(anima.vision/2), 1), min(max(sqrt(anima.size())-1, 1), 6)))))

