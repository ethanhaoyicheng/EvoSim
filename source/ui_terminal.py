import sys

max_width = 70

class Terminal():
    def __init__(self, capacity = 11):
        self.capacity = capacity
        self.content = []
        self.stdout = sys.__stdout__
    
    def write(self, text):
        self.stdout.write(text)

        for line in text.split("\n"):
            if line.strip() != "":
                self.content.append(line)
        while len(self.content) > self.capacity:
            self.content.pop(0)
    
    def flush(self):       #required for use of stdout
        self.stdout.flush()

def draw_terminal(screen, bottom, terminal, font):
    height = 0

    for line in terminal.content:
        nextline = line
        while nextline != None:
            if len(nextline) > max_width:
                nextline = line[:max_width]
                line = line[max_width:]
            else:
                line = None
            txt = font.render(nextline, True, "blue")
            height -= txt.get_height()
            screen.blit(txt, (30,bottom-height))
            
            nextline = line