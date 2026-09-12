import pygame 

class Button():
    button_list = []        #this is for sim buttons
    home_button_list = []   #for buttons on home screen / setup

    def __init__(self, rect, text="", toggleable=False, off_colour=(200,200,200), hover_colour = (200,150,200), on_colour=(200,100,200), border_colour = "grey", text_colour="white", category = "sim"):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.toggleable = toggleable
        self.status = False
        self.hovered = False
        self.clicked = False
        self.off_colour = off_colour
        self.hover_colour = hover_colour
        self.on_colour = on_colour
        self.border_colour = border_colour
        self.text_colour = text_colour

        self.visible = True

        if category == "sim":
            Button.button_list.append(self)
        elif category == "home":
            Button.home_button_list.append(self)
    

    @classmethod
    def get_button_list(cls):
        return cls.button_list
    
    @classmethod
    def get_home_button_list(cls):
        return cls.home_button_list
    
    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def set_text(self, text):
        self.text = text

    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True

    def toggle_visibility(self):
        self.visible = not self.visible

    def handle_event(self, event):
        self.clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                if self.toggleable:
                    self.status = not self.status
    
    def draw(self, screen, font):
        if self.status and (not self.rect.collidepoint(pygame.mouse.get_pos()) or pygame.MOUSEBUTTONDOWN):
            colour = self.on_colour
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            colour = self.hover_colour
        else:
            colour = self.off_colour
        
        pygame.draw.rect(screen, colour, self.rect)
        pygame.draw.rect(screen, self.border_colour, self.rect, 2)

        if self.text:
            txt = font.render(self.text, True, self.text_colour)
            screen.blit(txt, txt.get_rect(center = self.rect.center))

class Slider():
    slider_list = []
    home_slider_list = []

    def __init__(self, rect, value_range=(0,100), default=0, slider_colour = (0,50,150), knob_colour = (100,100,150), category = "sim"):
        self.rect = pygame.Rect(rect)
        self.min = value_range[0]
        self.max = value_range[1]
        self.status = max(self.min, min(self.max, default))   #status is int slider value
        self.dragging = False   # is currently being dragged?
        self.slider_colour = slider_colour
        self.knob_colour = knob_colour

        self.visible = True

        if category == "sim":
            Slider.slider_list.append(self)
        elif category == "home":
            Slider.home_slider_list.append(self)
    
    @classmethod
    def get_slider_list(cls):
        return cls.slider_list
    
    @classmethod
    def get_home_slider_list(cls):
        return cls.home_slider_list
    
    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True

    def toggle_visibility(self):
        self.visible = not self.visible

    def set_status(self, value):
        self.status = max(self.min, min(self.max, value))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.status = self.min + max(0, min(1, (event.pos[0]-self.rect.x)/self.rect.width)) * (self.max-self.min)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.slider_colour, self.rect)
        pygame.draw.circle(screen, self.knob_colour, (self.rect.x + int(self.rect.width * (self.status-self.min)/(self.max-self.min)), self.rect.centery), self.rect.height * 1.15)
                                    
