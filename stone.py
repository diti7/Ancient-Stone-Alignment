import pygame
import math
import sys

pygame.init()
screen = pygame.display.set_mode((1400, 1000))
pygame.display.set_caption("Tel-Aviv Yafo - Ancient Stone Alignment")

#*************************************************************************************************************

colours = {
    'black':(0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'light_gray': (220, 220, 220),
    'gold': (255, 255, 0), #Summer solstice stones
    'blue': (173, 216, 230),#Winter solstice stones
    'pink': (255, 192, 203), #Equinoxes stones
    'purple': (138, 43, 226),#Star Altair
    'orange': (255, 140, 0),#Venus
    'green': (0, 128, 0),#Star Alphard
    'sand': (238, 203, 173),   #bg
    'compass': (25, 25, 112)
}

fonts ={ 
    'title': pygame.font.Font(None, 42),
    'subtitle': pygame.font.Font(None, 32),
    'regular': pygame.font.Font(None, 28),
    'small': pygame.font.Font(None, 22),
    'tiny': pygame.font.Font(None, 18)
}

#*************************************************************************************************************
def draw_stone(pos, color, size, shape= "rectangle"):
    x, y = pos #positions...
    dark_color = tuple(max(0, c-40) for c in color)
    
    #stone shapes?
    if shape == "circle":
        pygame.draw.circle(screen, color, pos, size)
        pygame.draw.circle(screen, dark_color, pos, size, 2)
    elif shape == "star":
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            radius = size if i % 2==0 else size * 0.4
            points.append((x + radius * math.cos(angle), y +radius * math.sin(angle)))
        pygame.draw.polygon(screen,  color, points)
        pygame.draw.polygon(screen, dark_color, points, 2)

    else:  #rectangle - default
        pygame.draw.rect(screen, color, (x-size//2, y - size, size, size *2))
        pygame.draw.rect(screen, dark_color, (x-size//2, y- size, size, size*2), 2)

#base circle...
def draw_compass(center, radius):
    pygame.draw.circle(screen, colours['compass'],center, radius+ 40, 2)
    
    for angle, label in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
        rad = math.radians(90 - angle)
        end_x = center[0] + (radius + 35) * math.cos(rad)
        end_y = center[1] - (radius + 35) * math.sin(rad)
        pygame.draw.line(screen, colours['compass'], center, (end_x, end_y), 3)
        
        text = fonts['regular'].render(label, True, colours['compass'])
        text_rect = text.get_rect(center = (center[0] + (radius + 50)* math.cos(rad), center[1]-(radius + 50) * math.sin(rad)))
        screen.blit(text, text_rect)

def draw_alignment(center):
    #outer circle+inner circle=middle...
    outer_r, inner_r = 280, 150
    middle_r = (outer_r + inner_r) // 2
    
    #draw bg!
    pygame.draw.circle(screen, colours['sand'], center, outer_r +60)
    pygame.draw.circle(screen, colours['light_gray'], center, outer_r, 2)

    pygame.draw.circle(screen, colours['gray'], center, inner_r, 1)
    draw_compass(center, outer_r)
    
    #centre stone?
    draw_stone(center, (160, 160, 160), 20, "circle")
    
    alignments = [
        #solstices (outer circle) = name, azimuth, colour, r, s
        {"name": "Summer Solstice", "azimuth": 62.0, "color": colours['gold'], "radius": outer_r, "size": 25},
        {"name": "Summer Solstice", "azimuth": 297.9, "color": colours['gold'], "radius": outer_r, "size": 25},
        {"name": "Winter Solstice", "azimuth": 118.1, "color": colours['blue'],"radius": outer_r, "size": 25},
        {"name": "Winter Solstice", "azimuth": 242.0, "color": colours['blue'], "radius": outer_r, "size": 25},
        
        #Equinoxes (outer circle)
        {"name": "Equinox","azimuth": 90.0, "color": colours['pink'], "radius": outer_r, "size": 22},
        {"name": "Equinox", "azimuth": 270.0, "color": colours['pink'],"radius": outer_r, "size": 22},
        
        #stars (inner circle)
        {"name": "Altair", "azimuth": 79.6, "color": colours['purple'], "radius": inner_r, "size": 18, "shape": "star"},
        {"name": "Altair", "azimuth": 280.5,"color": colours['purple'], "radius": inner_r, "size": 18, "shape":"star"},
        {"name":"Alphard", "azimuth": 100.4, "color": colours['green'],"radius":inner_r, "size": 18, "shape": "star"},
        {"name": "Alphard", "azimuth": 259.6,"color": colours['green'], "radius": inner_r, "size": 18, "shape": "star"},
        
        #venus (middle circle)
        {"name": "Venus", "azimuth": 76.6,"color": colours['orange'], "radius": middle_r, "size": 18,"shape":"circle"},
        {"name": "Venus", "azimuth": 283.6, "color": colours['orange'], "radius": middle_r, "size": 18, "shape": "circle"},
        
        #Extras......x
        {"name": "", "azimuth":0, "color": colours['gray'], "radius": outer_r, "size": 20},
        {"name": "", "azimuth": 180, "color": colours['gray'], "radius":outer_r,"size": 20},
        {"name": "", "azimuth": (242.0 + 180)/2, "color": colours['gray'], "radius": outer_r, "size": 20},
        {"name": "", "azimuth": (118.1 + 180)/2, "color": colours['gray'], "radius": outer_r, "size": 20},
        {"name": "", "azimuth": (297.9+0)/2, "color": colours['gray'],"radius": outer_r, "size": 20},
        {"name": "", "azimuth": (62.0 +0)/2, "color": colours['gray'], "radius": outer_r, "size": 20}
    ]
    #aligning... ... ... ... ... ...
    for align in alignments:
        rad = math.radians(90 - align["azimuth"])
        x = center[0] + align["radius"] * math.cos(rad)
        y = center[1]- align["radius"] * math.sin(rad)
        
        shape = align.get("shape", "rectangle")
        draw_stone((x, y), align["color"], align["size"], shape)
        
        #azimuth labels? add degree...
        if align["name"]:  # Only show labels for named stones
            text= fonts['tiny'].render(f"{align['azimuth']}°", True, colours['black'])
            text_rect = text.get_rect(center=(x, y + align["size"] + 20))
            pygame.draw.rect(screen, colours['white'], text_rect.inflate(4, 2))
            pygame.draw.rect(screen, colours['black'], text_rect.inflate(4, 2), 1)
            
            screen.blit(text, text_rect)

def draw_ui():
    #title
    title = fonts['title'].render("ANCIENT STONE ALIGNMENT SITE", True, colours['black'])
    screen.blit(title, (700 - title.get_width() //2, 30))
    
    #Legend
    pygame.draw.rect(screen,colours['white'], (50, 150, 300, 400))
    pygame.draw.rect(screen, colours['black'], (50, 150, 300, 400), 2)
    
    legend_title = fonts['subtitle'].render("         STONE LEGEND", True, colours['black'])
    screen.blit(legend_title, (60, 160))
    
    items = [
        ("Summer Solstice", colours['gold']), ("Winter Solstice", colours['blue']), ("Equinox", colours['pink']),
        ("Star Altair", colours['purple']), ("Star Alphard", colours['green']), ("Venus", colours['orange']),
        ("Extra Stones", colours['gray'])
    ]
    
    for i, (name, color) in enumerate(items):
        y = 200 + i * 50
        pygame.draw.rect(screen, color, (60, y, 25, 25))
        screen.blit(fonts['small'].render(name, True, colours['black']), (95, y))

#*************************************************************************************************************
def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                #running=true???
                running=False
        
        screen.fill((250, 248, 240))  #background colour.
        draw_alignment((700, 500))
        draw_ui()

        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()