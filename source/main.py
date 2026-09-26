import pygame
import time, random

from simulation import Simulation
from realm import Realm
import realm
import cell
from fruit import *
from flora import Flora
from anima import Anima, food_list
from extratraits import ExtraTraits
import nickname
import realm_settings

from todisplay import *
import ui

DATABASE_SAMPLE_INTERVAL = 25 #10

#what happens during collisions? when two animas share same cell centre? 

#ALWAYS REMEMBER TO ADD TRAILING COMMA FOR SINGLE ELEMENT TUPLE

def main():

    

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("EvoSim - setup")
    homeShell = ui.Shell("home")
    homeShell.track_index = 3
    ui.play_music(homeShell)

    while homeShell.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            ui.handle_home_ui(event, homeShell)
           
        clock.tick(5)
        print(clock.get_fps())
        
        screen.fill(ui.HOME_BACKGROUND_COLOUR)
        ui.tick_home_ui(screen, homeShell)
        pygame.display.flip()


    ui.myShell.music_volume = homeShell.music_volume

    mySim = Simulation()

    test_element_list = []
    #for i in range(20):
    #    test_element_list.append(Flora(i, random.uniform(-960, 960) , random.uniform(-540, 540), 10, 0.1)) code expired

    """for i in range(10):
        test_element_list.append(Anima(i, "name/diet/strength/toughness", [("apple",), [random.uniform(1, 2),0.5,0.3], random.uniform(15, 30), random.uniform(5,10), random.uniform(5,15), random.uniform(5,15), random.uniform(20,30), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,120)], None, random.uniform(0, 99) , random.uniform(0, 99)))
        test_element_list.append(Anima(i, "name/diet/strength/toughness", [("berry",), [random.uniform(1, 2),0.5,0.3], random.uniform(15, 30), random.uniform(5,10), random.uniform(5,15), random.uniform(5,15), random.uniform(20,30), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,120)], None, random.uniform(0, 99) , random.uniform(0, 99)))
    for i in range(4):
        test_element_list.append(Anima(i, "name/diet/strength/toughness", [("meat",), [random.uniform(1, 2),0.5,0.3], random.uniform(15, 30), random.uniform(5,10), random.uniform(5,15), random.uniform(5,15), random.uniform(20,30), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,120)], None, random.uniform(0, 99) , random.uniform(0, 99)))
"""
    #for i in range(400): #400
        #test_element_list.append(Anima(i, "name/diet/strength/toughness", [(random.choice(food_list),), [random.uniform(1, 5),0.5,0.3], random.uniform(15, 30), random.uniform(5,25), random.uniform(5,30), random.uniform(5,30), random.uniform(20,30), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50)], None, random.uniform(0, 600) , random.uniform(0, 400)))
        #test_element_list.append(Anima(i, "name/diet/strength/toughness", [("apple",), [random.uniform(1, 5), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4,10), random.uniform(4,10), random.uniform(20,30), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50), []], None, random.uniform(0, 300) , random.uniform(0, 300)))
        #test_element_list.append(Anima(i, "name/diet/strength/toughness", [("apple",), [random.uniform(1, 5), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4,10), random.uniform(4,10), random.uniform(30,80), random.uniform(0, 1), random.uniform(30,100), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, 600) , random.uniform(0, 500)))
    #for i in range(20): #20
        #test_element_list.append(Anima(i, "name/diet/strength/toughness", [("meat",), [random.uniform(1, 8), [1,0.5,0.3]], random.uniform(15, 30), random.uniform(5,15), random.uniform(4, 15), random.uniform(4,15), random.uniform(30,80), random.uniform(0, 1), random.uniform(20,80), random.uniform(40,200), random.uniform(5,50), ExtraTraits(set())], None, random.uniform(0, 600) , random.uniform(0, 500)))

    test_element_list.extend(homeShell.realm_settings[7])

    #homeShell.realm_settings[6] = [[flora[0], int(round(flora[1]* homeShell.realm_scale_factor**2 * homeShell.realm_flora_factor))] for flora in realm_settings.default_realm_settings[6]]
    
    homeShell.realm_settings[6] = realm_settings.generate_flora(homeShell.realm_flora_factor, homeShell.realm_scale_factor)
    homeShell.realm_settings[7] = realm_settings.generate_primordial_list(homeShell.realm_settings[1], homeShell.realm_settings[2], int(round(realm_settings.herbivore_count * homeShell.realm_scale_factor**2)),  int(round(realm_settings.carnivore_count * homeShell.realm_scale_factor**2)),  int(round(realm_settings.any_count * homeShell.realm_scale_factor**2)))
    realm.ICE_MIN_RADIUS *= homeShell.realm_scale_factor
    realm.ICE_MIN_RADIUS = int(realm.ICE_MIN_RADIUS)
    realm.ICE_MAX_RADIUS *= homeShell.realm_scale_factor
    realm.ICE_MAX_RADIUS = int(realm.ICE_MAX_RADIUS)
    
    print("Generating realm...")
    #testRealm = Realm(nickname.generate_nickname("realm"), 600, 400, 1, 0.2, 0.05, [["tree", 3000], ["bush", 5000], ["vine", 1250], ["reed", 1000], ["lily", 2000], ["wildgrass", 25000]],test_element_list, "name/diet/strength/toughness") #birth new test realm
    #name/genome
    #testRealm = Realm(nickname.generate_nickname("realm"), 300, 300, 1.25, 0.1, 0, [["tree", 150]],test_element_list, "name/diet/extra_traits/strength/toughness") #birth new test realm
    #testRealm = Realm(nickname.generate_nickname("realm"), 600, 500, 1.25, 0.1, 0, [["tree", 600]],test_element_list, "name/diet/extra_traits/strength/toughness") #birth new test realm
    testRealm = Realm(*homeShell.realm_settings)

    #lily 0/2000/3000
    mySim.add_realm(testRealm)

    """for element in testRealm.elements:
        print(dir(element))
    print(mySim.realms[0].elements)
    print(testRealm.elements)
    for element in testRealm.elements[0]:
        print(element.capacity, element.fruitNo, element.x, element.y, element.fruit, element.id)"""
    
    #print(testRealm.environment)
    #print(len(testRealm.spatialhash.buckets))
    #print(testRealm.spatialhash.buckets)

    print(testRealm.check_water())
    print(testRealm.check_ice()) 
    
    print(testRealm.count_flora())
    print(testRealm.check_grass())

    #print(testRealm.environment)

    #simulation ui begins
    pygame.display.set_caption("EvoSim: " + testRealm.name)
    ui.play_music(ui.myShell)


    window = ((640-testRealm.width/2, 640+testRealm.width/2),(100, 100 + testRealm.height)) #was 120, 120 + h for y
    """left = window[0][0]
    right = window[0][1]
    top = window[1][0]
    bottom = window[1][1]         COPY+PASTE"""

    #vis_realm = Visual_Realm(window, testRealm)

    blit = ui.draw_world_blit(testRealm)

    print("A new world arises!")

    for i in range(200):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ui.myShell.running = False
            ui.handle_ui(event, ui.myShell, window, testRealm)
           

        if not ui.myShell.paused:                                       #sim paused

            if testRealm.time % DATABASE_SAMPLE_INTERVAL == 0:
                testRealm.database.update()

            mySim.tick()
            
        #clock.tick(5 * ui.myShell.sim_speed)
        print(clock.get_fps())
        print(i)
        
        screen.fill(ui.BACKGROUND_COLOUR)
        ui.tick_visual_realm(testRealm, screen, window, blit, ui.myShell)
        ui.tick_extra_ui(screen, window, ui.myShell)
        pygame.display.flip()

    
    pygame.quit()
        
    
    def dx(record):
        print(record + " : " + to_display(getattr(testRealm.database, record, "No such record")))
        

    #rename to db?
    print("Extra Traits " + to_display(testRealm.database.calc_extra_traits(testRealm.elements[1])))
    flood()
    print(to_display(testRealm.database.anima_populations))
    flood()
    print(to_display(testRealm.database.death_causes))
    flood()
    print(to_display(testRealm.database.avg_genomes))
    flood()
    print(to_display(testRealm.database.diets))
    flood()
    
    print(to_display(testRealm.database.avg_lifespans))
    flood()
    display(testRealm.database.lifespan_quartiles)
    flood()
    display(testRealm.database.age_quartiles)
    flood()
    display(testRealm.database.calc_total_avg_lifespan())
    flood()
    display(testRealm.database.avg_statuses)
    flood()
    display(testRealm.database.offspring_count_distributions)
    flood()
    display([anima.diet for anima in testRealm.elements[1] if len(anima.diet) >= 2])
    return 0



import cProfile
import pstats

if __name__ == "__main__":
    profiler = cProfile.Profile()

    profiler.enable()
    main()
    profiler.disable()

    profiler.dump_stats("evosim_profile_10k_200.prof")

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(30)

#add carcasses to spatial hash and as class

"""for batch in range(400):
            for tick in range(25):
                #print(testRealm.time)
                testRealm.tick()
                vis_realm
                #print([[(anima == anima.target.target)] for anima in testRealm.elements[1] if anima.target != None])
                #print([[anima.distance_to(anima.target), anima.goals, anima.target, (anima.vision+anima.speed+anima.target.speed>= anima.distance_to(anima.target))] for anima in testRealm.elements[1] if isinstance(anima.target, Anima)])
                #print([[anima.round_status(),round(anima.x), round(anima.y), round(anima.dx), round(anima.dy), anima.mode, anima.target, anima.goals] for anima in testRealm.elements[1]]) #anima.status, anima.sig_genome(),anima.x, anima.y, anima.dx, anima.dy, anima.mode, anima.target, anima.goals
                #print([flora.fruitNo for flora in testRealm.elements[0]])

            print(testRealm.count_anima())
            print(testRealm.time)
            testRealm.database.update()"""


#Use IntelliSense to learn about possible attributes.
# Hover to view descriptions of existing attributes.
# For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387