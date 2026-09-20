import pygame 
from math import sqrt

from ui_sim_plane import *
from ui_element import *
from ui_design import *
from ui_factfile import draw_anima_record, draw_genome_record, genome_view
from todisplay import to_display
from ui_terminal import *

"""
class Visual_Realm():
    def __init__(self, window, realm):
        self.window = window
        self.realm = realm
        self.scale = 1

        diff = window[0][1] - window[0][0] - realm.width
        if diff > 0:
            self.window[0][0] += diff/2
            self.window[0][1] -= diff/2
        elif diff > 0:
        



    def tick(self):
        """


def tick_visual_realm(realm, screen, window, blit, shell):
    left = window[0][0]
    right = window[0][1]
    top = window[1][0]
    bottom = window[1][1]

    screen.blit(blit, (left,top))

    if shell.anima_to_view:
        anima = shell.anima_to_view
        if not anima.asleep and not anima.is_dead():
            pygame.draw.circle(screen, VISION_COLOUR, (round(left + anima.x), round(top + anima.y)), round(anima.vision+0.5))
        pygame.draw.circle(screen, HIGHLIGHT_COLOUR, (round(left + anima.x), round(top + anima.y)), int(round(min(max(sqrt(anima.size()), 1), 7)) + 1)) # was sqrt size

        genome_view.draw(screen, font)
        if genome_view.status == False:
            draw_anima_record(anima, realm, screen)
        elif genome_view.status == True:
            draw_genome_record(anima, realm, screen)
        

    if FRUIT_COLOUR_SET:
        for flora in realm.elements[0]:
            if flora.fruitNo != 0: 
                pygame.draw.rect(screen, FRUIT_COLOUR_SET[flora.fruit.name], (round(left + flora.x), round(top + flora.y), 1, 1))
    
    for corpse in realm.graveyard[1]:
        pygame.draw.circle(screen, CORPSE_COLOUR, (round(left + corpse.x), round(top + corpse.y)), min(max(corpse.food_chunks/2, 1), 5))
        
    for anima in realm.elements[1]:
        draw_anima(anima, screen, round(left + anima.x), round(top + anima.y))

    apply_brightness(screen, shell.brightness)

def tick_extra_ui(screen, window, shell):
    hide_ui.draw(screen, font)

    if not shell.ui_visible:
        return
    
    for button in Button.get_button_list():
        if button.visible:
            button.draw(screen, font)
    
    for slider in Slider.get_slider_list():
        if slider.visible:
            slider.draw(screen)
    
    screen.blit(font.render(f"Track {to_display(shell.track_index+1,2)}", True, TRACK_TEXT_COLOUR), (650,75))

    txt = tutorial_texts[shell.tutorial_index]
    width, height = font.size(txt)
    pygame.draw.rect(screen, "white", (17, 357, width+6, height+6)) #grey93
    screen.blit(font.render(txt, True, GENERAL_TEXT_COLOUR), (20,360))
    
    txt = colour_tutorial_texts[shell.ctutorial_index]
    width, height = font.size(txt)
    pygame.draw.rect(screen, "white", (17, 487, width+6, height+6))
    screen.blit(font.render(txt, True, GENERAL_TEXT_COLOUR), (20,490))

    draw_terminal(screen, 600, terminal, terminal_font) #600 -> window[1][1]

def tick_home_ui(screen, shell):
    for button in Button.get_home_button_list():
        button.draw(screen, home_font)
    
    for slider in Slider.get_home_slider_list():
        slider.draw(screen)
    
    the_text = big_font.render("Twinkledelux's EvoSim!", False, "yellow")
    screen.blit(the_text, the_text.get_rect(center = (screen.get_width()/2, 100)))

    txt = home_font.render("This realm is called... " + shell.realm_settings[0], False, "green")
    screen.blit(txt, txt.get_rect(center = (screen.get_width()/2 - 5, 150)))

    txt = home_font.render("Size : " + to_display(shell.realm_settings[1]) + "x" + to_display(shell.realm_settings[2]), False, "aquamarine")
    screen.blit(txt, txt.get_rect(center = (screen.get_width()/2 - 5, 240)))

    txt = home_font.render("Temperature : " + to_display(shell.realm_settings[3]), False, "aquamarine")
    screen.blit(txt, txt.get_rect(center = (screen.get_width()/2 - 5, 340)))

    txt = home_font.render("Water coverage : " + to_display(shell.realm_settings[4]), False, "aquamarine")
    screen.blit(txt, txt.get_rect(center = (screen.get_width()/2 - 5, 440)))

    txt = home_font.render("Vegetation density : " + to_display(shell.realm_flora_factor), False, "aquamarine")
    screen.blit(txt, txt.get_rect(center = (screen.get_width()/2 - 5, 540)))


    
#grass is green, flora is purple : legacy
#aquamarine