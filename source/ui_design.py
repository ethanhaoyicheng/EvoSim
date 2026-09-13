import pygame 
import sys
from ui_element import *
from ui_sim_plane import * #for colours in tutorial
from ui_terminal import Terminal
from ui_factfile import genome_view

from realm_settings import default_realm_settings, create_realm_name
import realm_settings

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

pygame.init()

font = pygame.font.SysFont(None, 24)
home_font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 40)
terminal_font = pygame.font.SysFont("consolas", 10)

terminal = Terminal()
sys.stdout = terminal

HOME_BACKGROUND_COLOUR = "blue"
BACKGROUND_COLOUR = "white"
GENERAL_TEXT_COLOUR = "royalblue1"
TRACK_TEXT_COLOUR = "pink"

class Shell():
    def __init__(self, category = "sim"):
        if category == "home":
            self.sfx_volume = 0.5
            self.music_volume = 0.5
            self.sfx_muted = False
            self.music_muted = False

            self.track_index = 0

            self.running = True

            self.brightness = 1

            self.colorid = 0

            self.realm_settings = default_realm_settings[:]
            self.realm_scale_factor = 1
            self.realm_flora_factor = realm_settings.flora_factor

        else:
            self.sfx_volume = 0.5
            self.music_volume = 0.5
            self.sfx_muted = False
            self.music_muted = False

            self.track_index = 0

            self.ui_visible = True
            self.sim_speed = 1
            self.paused = False
            self.running = True
            self.brightness = 1

            self.tutorial_index = 0
            self.ctutorial_index = 0

            self.anima_to_view = None

myShell = Shell()

#HOME

hmusic_up = Button((250,70,30,30), "+", category="home")
hmusic_down = Button((290,70,30,30), "-", category="home")
hmusic_mute = Button((1000,70,65,30), "Mute", category="home")
hmusic_unmute = Button((1000,120,80,30), "Unmute", category="home")


hchange_realm_name = Button((850,136,60,25), "New", category="home")

hsize_up = Button((813,193,25,25), "+", category="home")
hsize_down = Button((447,193,25,25), "-", category="home")
hsize_slider = Slider((485,200,310,10), (0.1,1), 1, category="home")

htemp_up = Button((813,293,25,25), "+", category="home")
htemp_down = Button((447,293,25,25), "-", category="home")
htemp_slider = Slider((485,300,310,10), (0,3), default_realm_settings[3], category="home")

hwet_up = Button((813,393,25,25), "+", category="home")
hwet_down = Button((447,393,25,25), "-", category="home")
hwet_slider = Slider((485,400,310,10), (0,1), default_realm_settings[4], category="home")

hflora_up = Button((813,493,25,25), "+", category="home")
hflora_down = Button((447,493,25,25), "-", category="home")
hflora_slider = Slider((485,500,310,10), (0,100), realm_settings.flora_factor, category="home")

hcolorset_button = Button((813,500,70,25), "Colour!", category="home")

start = Button((540,600,200,45), "GENERATE WORLD", category="home")


#SFX
sfx_up = Button((20,20,30,30), "+")
sfx_down = Button((60,20,30,30), "-")
sfx_slider = Slider((100,25,150,10), (0, 1), myShell.sfx_volume)
sfx_mute = Button((260,20,60,30), "Mute")
sfx_unmute = Button((330,20,70,30), "Unmute")

#MUSIC
music_play = Button((20,70,80,30), "Play/Pause")
music_next = Button((110,70,60,30), "Next")
music_prev = Button((180,70,60,30), "Prev")

music_up = Button((250,70,30,30), "+")
music_down = Button((290,70,30,30), "-")
music_slider = Slider((330,75,150,10), (0, 1), myShell.music_volume)

music_mute = Button((490,70,60,30), "Mute")
music_unmute = Button((560,70,70,30), "Unmute")

#  BRIGHTNESS / CONTRAST 
brightness_slider = Slider((20,130,200,10), (0.2, 1.5), 1)
contrast_toggle = Button((230,120,120,30), "Hi-Contrast", toggleable=True)

#  LANGUAGE 
languages = ["EN","CN","TM"]
lang_buttons = [Button((20+i*60,170,50,30), lang) for i,lang in enumerate(languages)]

#  UI 
hide_ui = Button((20,210,100,30), "Hide UI")

#  SIM CONTROL 
speed_buttons = [Button((20+i*60,260,50,30), f"x{s}") for i,s in enumerate([1,2,4,8])]
pause_btn = Button((520,650,100,30), "Pause")
end_btn = Button((635,650,100,30), "End")

#  TUTORIAL 
tutorial_texts = [
    "Welcome to your very own realm! (Press the > icon)",
    "Each of those little circles moving around in your realm is an organism, also known as an 'anima'",
    "You can click on an anima to pull up a fact file giving information about it. Try it!",
    "Anima need to eat, drink, sleep and stay healthy. If they can do all of that, they might mate",
    "Otherwise, they'll die!",
    "The offspring of two anima will have traits which are a genetic combination of its parents'",
    "Let me give you an idea of what some of these traits might be:",
    "Larger organisms require more food but are better in fights and age more slowly*",
    "Vision is another trait which determines how far an organism can sense the other things in the simulation",
    "An organism's vision range is represented by how large its eye is",
    "Animas can develop unique extra traits such as a venomous bite, plate armour, or neverending growth",
    "All in all, animas have " + "14" + " genetic traits, PLUS any unique extra traits",
    "The fact file of an anima gives further stats including its complete genome and immediate family",
    "The first two organisms displayed in the 'Family' section are its parents, and up its 4 eldest children will be displayed underneath",
    "(Note: first generation organisms won't have parents, only children)",
    "You can control the music, sound effects, simulation speed, and more, using all the buttons you can see around here...",
    "That's the basic tutorial! Keep reading for info that's a little more niche ->",
    "An anima will increase in size until they reach their genetically given maturity age (given in the fact file in simulation ticks)",
    "An anima's age is given in the fact file in decaticks (unit of 10 ticks)"
    "An anima's size is the geometric mean of their strength (how hard they can hit) and their toughness (how much they can take)",
    "An anima's needs have the following numbers corresponding to them:",
    "0: hunger, 1: thirst, 2: sleepiness; 3: damage, 4: mating drive",
    "These apply to both the goal numbers in an anima's goals, and the index of each status in an anima's status list",
    "That's about it for now...",
    "Have fun, and happy evolving!",
]

colour_tutorial_texts = [
    "An anima's state can be observed from the colours of its body and eye. For instance, an anima's eye turns gold when it sleeps*",
    "*This applies to the default colour set",
    "Default body colours: purple = poisoned, orange-red = hurt, red = wounded...",
    "...senescent = white, child = green, grey-blue = adult meat-eater, aquamarine = adult non-meat-eater ",
    "Default eye colours: blue = wandering, purple = found food, light blue = found water, lilac = searching for mate, black = hunting, white = fleeing",
    "You can't tell everything from just the colours though - click on an anima to pull up a fact file giving you all the details!",
]

evo_fact_texts = [
    "Evolution is driven by natural selection!"
]

next_tut = Button((20,320,60,30), ">")
prev_tut = Button((90,320,60,30), "<")

next_ctut = Button((20,450,60,30), ">")
prev_ctut = Button((90,450,60,30), "<")

pygame.mixer.init()



tracks = ["peritune-folk-chinese(chosic.com).mp3", "00664805.mp3", "Alan Walker - Faded.mp3", "Alan Walker - The Spectre.mp3"]  

def play_music(shell):
    #pygame.mixer.music.load(tracks[shell.track_index])
    pygame.mixer.music.load(resource_path(tracks[shell.track_index]))
    pygame.mixer.music.play(-1)

anima_selection_range = 8

def handle_ui(event, shell, sim_window, realm):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        left = sim_window[0][0]
        right = sim_window[0][1]
        top = sim_window[1][0]
        bottom = sim_window[1][1]

        mx, my = pygame.mouse.get_pos()
        if left < mx < right and top < my < bottom:
            shell.anima_to_view = None
            genome_view.hide()

            nearest_anima = None
            nearest_dist = anima_selection_range

            for anima in realm.elements[1] + realm.graveyard[1]:
                dist = anima.distance_to_point(mx - left, my - top)
                if dist <= nearest_dist:
                    nearest_anima = anima
                    nearest_dist = dist                    
                    genome_view.show()
            shell.anima_to_view = nearest_anima
            
            

    for b in Button.button_list:
        b.handle_event(event)

    for b in lang_buttons + speed_buttons:
        b.handle_event(event)

    for s in Slider.slider_list:
        s.handle_event(event)

    #  SFX 
    if sfx_up.clicked: shell.sfx_volume = min(1, shell.sfx_volume+0.05); sfx_slider.set_status(shell.sfx_volume)
    if sfx_down.clicked: shell.sfx_volume = max(0, shell.sfx_volume-0.05); sfx_slider.set_status(shell.sfx_volume)
    if sfx_mute.clicked: shell.sfx_muted = True
    if sfx_unmute.clicked: shell.sfx_muted = False

    if sfx_slider.dragging: shell.sfx_volume = sfx_slider.status
    pygame.mixer.set_num_channels(8)
    for i in range(8):
        pygame.mixer.Channel(i).set_volume(0 if shell.sfx_muted else shell.sfx_volume)

    #  MUSIC 
    if music_play.clicked:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    if music_next.clicked:
        shell.track_index = (shell.track_index+1)%len(tracks)
        play_music(shell)

    if music_prev.clicked:
        shell.track_index = (shell.track_index-1)%len(tracks)
        play_music(shell)

    if music_up.clicked: shell.music_volume = min(1, shell.music_volume+0.05); music_slider.set_status(shell.music_volume)
    if music_down.clicked: shell.music_volume = max(0, shell.music_volume-0.05); music_slider.set_status(shell.music_volume)
    if music_mute.clicked: shell.music_muted = True
    if music_unmute.clicked: shell.music_muted = False

    if music_slider.dragging: shell.music_volume = music_slider.status
    pygame.mixer.music.set_volume(0 if shell.music_muted else shell.music_volume)

    #  BRIGHTNESS 
    shell.brightness = brightness_slider.status



    #  LANGUAGE 
    for i,b in enumerate(lang_buttons):
        if b.clicked:
            print("Language:", languages[i])

    #  UI 
    if hide_ui.clicked:
        shell.ui_visible = not shell.ui_visible

    #  SIM 
    for i,b in enumerate(speed_buttons):
        if b.clicked:
            shell.sim_speed = [1,2,4,8][i]

    if pause_btn.clicked:
        shell.paused = not shell.paused

    if end_btn.clicked:
        shell.running = False

    #  TUTORIAL 
    if next_tut.clicked:
        shell.tutorial_index = min(len(tutorial_texts)-1, shell.tutorial_index+1)
    if prev_tut.clicked:
        shell.tutorial_index = max(0, shell.tutorial_index-1)

    if next_ctut.clicked:
        shell.ctutorial_index = min(len(colour_tutorial_texts)-1, shell.ctutorial_index+1)
    if prev_ctut.clicked:
        shell.ctutorial_index = max(0, shell.ctutorial_index-1)

    if genome_view.clicked:
        if not genome_view.status:
            genome_view.set_text("VIEW GENOME")
        else:
            genome_view.set_text("VIEW ANIMA")


def handle_home_ui(event, shell):
    for b in Button.home_button_list:
        b.handle_event(event)

    for s in Slider.home_slider_list:
        s.handle_event(event)
    
    if hmusic_up.clicked: shell.music_volume = min(1, shell.music_volume+0.05); music_slider.set_status(shell.music_volume)
    if hmusic_down.clicked: shell.music_volume = max(0, shell.music_volume-0.05); music_slider.set_status(shell.music_volume)
    if hmusic_mute.clicked: shell.music_muted = True
    if hmusic_unmute.clicked: shell.music_muted = False
    
    if hchange_realm_name.clicked : shell.realm_settings[0] = create_realm_name()

    if hsize_up.clicked : shell.realm_scale_factor = min(1, shell.realm_scale_factor + 0.05); hsize_slider.set_status(shell.realm_scale_factor)
    if hsize_down.clicked : shell.realm_scale_factor = max(0.1, shell.realm_scale_factor - 0.05); hsize_slider.set_status(shell.realm_scale_factor)
    if hsize_slider.dragging : shell.realm_scale_factor = hsize_slider.status

    shell.realm_settings[1] = int(default_realm_settings[1] * shell.realm_scale_factor)
    shell.realm_settings[2] = int(default_realm_settings[2] * shell.realm_scale_factor)

    if htemp_up.clicked: shell.realm_settings[3] = min(3, shell.realm_settings[3] + 0.05); htemp_slider.set_status(shell.realm_settings[3])
    if htemp_down.clicked : shell.realm_settings[3] = max(0, shell.realm_settings[3] - 0.05); htemp_slider.set_status(shell.realm_settings[3])
    if htemp_slider.dragging : shell.realm_settings[3] = htemp_slider.status

    if hwet_up.clicked: shell.realm_settings[4] = min(1, shell.realm_settings[4] + 0.01); hwet_slider.set_status(shell.realm_settings[4])
    if hwet_down.clicked : shell.realm_settings[4] = max(0, shell.realm_settings[4] - 0.01); hwet_slider.set_status(shell.realm_settings[4])
    if hwet_slider.dragging : shell.realm_settings[4] = hwet_slider.status

    if hflora_up.clicked: shell.realm_flora_factor = min(100, shell.realm_flora_factor + 1); hflora_slider.set_status(shell.realm_flora_factor)
    if hflora_down.clicked : shell.realm_flora_factor = max(0, shell.realm_flora_factor - 1); hflora_slider.set_status(shell.realm_flora_factor)
    if hflora_slider.dragging : shell.realm_flora_factor = hflora_slider.status

    if hcolorset_button.clicked:
        shell.colorid += 1
        if shell.colorid >= len(colour_sets):
            shell.colorid = 0

    pygame.mixer.music.set_volume(0 if shell.music_muted else shell.music_volume)
    
    if start.clicked:
        set_sim_colours(colour_sets[shell.colorid])
        shell.running = False

    return
