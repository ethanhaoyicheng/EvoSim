import pygame
from todisplay import *
from ui_sim_plane import draw_anima
from ui_element import Button, Slider
from flora import Flora

pygame.init()
rfont = pygame.font.SysFont(None, 18)
rcolour = "steelblue3"
row_size = 25

genome_view = Button((0,0,0,0), "GENOME VIEW", True, text_colour="green3")
genome_view.hide()

def draw_anima_record(anima, realm, screen):
    record = pygame.Rect((640 + realm.width/2 + 50, 90, 220, 500), width = 0, border_radius = 0)
    pygame.draw.rect(screen, "wheat", record)

    txt = rfont.render(anima.get_alias(), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+25)))

    txt = rfont.render("ID " + str(anima.id), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+50)))

    txt = rfont.render("LOC : " + to_display((anima.x, anima.y)), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+75)))

    txt = rfont.render("AGE : " + str(int(anima.age/10)), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100)))

    txt = rfont.render("STATUS : " + to_display(anima.status), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + row_size)))

    txt = rfont.render("GOALS : " + to_display(anima.goals), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 2*row_size)))

    txt = rfont.render("FLEEING FROM " + anima.target.nickname, True, rcolour) if anima.mode == 3 and hasattr(anima.target, "nickname") else rfont.render("APPROACHING " + (anima.target.food_given + " PLANT AT " + str((anima.target.x, anima.target.y)) if isinstance(anima.target, Flora) else anima.target.nickname if hasattr(anima.target, "nickname") else "WATER AT " + str(anima.target) if isinstance(anima.target, tuple) else "A GHOST"), True, rcolour) if not anima.target == None else rfont.render("SLEEPING", True, rcolour) if anima.asleep else rfont.render("WANDERING", True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 3*row_size)))

    txt = rfont.render("FAMILY :", True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 4*row_size)))

    #txt = rfont.render("GENOME : " + to_display(anima.genome), True, rcolour) 
    #screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 4*row_size)))
    #genome button triggers switch to genome view page ***
    draw_genome_view_button(record)

    if len(anima.parents) >= 1:
        draw_anima(anima.parents[0], screen, (record.centerx + record.x)/2, record.y+100 + 5*row_size)


    if len(anima.parents) >= 2:
        draw_anima(anima.parents[1], screen, (record.centerx + record.x+record.width)/2, record.y+100 + 5*row_size)
    
    if len(anima.offspring) >= 1:
        draw_anima(anima.offspring[0], screen, (record.centerx + record.x)/2, record.y+100 + 6*row_size)

    if len(anima.offspring) >= 2:
        draw_anima(anima.offspring[1], screen, (record.centerx + record.x+record.width)/2, record.y+100 + 6*row_size)
    
    if len(anima.offspring) >= 3:
        draw_anima(anima.offspring[2], screen, (record.centerx + record.x)/2, record.y+100 + 7*row_size)

    if len(anima.offspring) >= 4:
        draw_anima(anima.offspring[3], screen, (record.centerx + record.x+record.width)/2, record.y+100 + 7*row_size)
        
    #energy consumption
    txt = rfont.render("DECEASED FROM " + to_display(anima.autopsy()).upper(), True, rcolour) if anima.is_dead() else rfont.render("", True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 9*row_size)))

    txt = rfont.render("CNK : " + anima.nickname, True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 11*row_size)))

    #txt = rfont.render("GOALS : " + to_display(anima.goals), True, rcolour)
    #screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+100 + 12*row_size)))
    

    #target and parents have sprites printed to display which can be clicked on to select them ***


genotype_list = ["DIET", "SPEED", "TURNING SPEED", "VISION RANGE", "STRENGTH", "TOUGHNESS", "MATING DRIVE", "BOOST FACTOR", "INJURY THRESHOLD", "MATURITY AGE", "REFRACTORY", "EXTRA TRAITS"]

def draw_genome_record(anima, realm, screen):
    genome = anima.genome
    record = pygame.Rect((640 + realm.width/2 + 50, 90, 220, 500), width = 0, border_radius = 0)
    pygame.draw.rect(screen, "wheat", record)

    txt = rfont.render(anima.get_alias(), True, rcolour)
    screen.blit(txt, txt.get_rect(center = (record.centerx, record.y+25)))

    for g in range(len(anima.genome)):
        display = to_display(genome[g])
        if g == 4: 
            display += f"({to_display(anima.strength)})"
        elif g == 5:
            display += f"({to_display(anima.toughness)})"
        txt = rfont.render(genotype_list[g] + " : " + display, True, rcolour)
        screen.blit(txt, txt.get_rect(center = (record.centerx, record.y + 55 + g*row_size)))

    #genome button triggers switch back to anima view page ***
    draw_genome_view_button(record)

def draw_genome_view_button(record):
    render = rfont.render(genome_view.text, True, (0,0,0))
    gvw, gvh = render.get_size()
    gvw += 40
    gvh += 20
    genome_view.set_rect((record.centerx-gvw/2, record.y+100 + 14*row_size - gvh/2, gvw, gvh))

    

    
    

    