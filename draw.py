from all_colors import *
import pygame

pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('рисовалка')

background_color = (255, 255, 255)
FPS = 60
size = 50  
brush_color = (0, 0, 0)
brush_width = 30
border_color = (0, 0, 0)
CUR_INDEX = 0

clock = pygame.time.Clock()
running = True

canvas = pygame.Surface(screen.get_size())
canvas.fill(background_color)

pallete_rect = pygame.Rect(10, 10, size * 12, size)
pallete = pygame.Surface(pallete_rect.size)
pallete.fill(background_color)

dragging_pallete = False
offset = (0, 0)


rect_start = None
rect_current = None
rects = []

def draw_pallate():
    pallete.fill(background_color)
    for i in range(12):
        color_rect = pygame.Rect(i * size, 0, size, size)
        pygame.draw.rect(pallete, COLORS[i], color_rect)
    border_rect = pygame.Rect(CUR_INDEX * size, 0, size, size)
    pygame.draw.rect(pallete, border_color, border_rect, width=3)
    screen.blit(pallete, pallete_rect.topleft)

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if pallete_rect.collidepoint(event.pos):
                    selected_color_index = (event.pos[0] - pallete_rect.left) // size
                    CUR_INDEX = selected_color_index
                    brush_color = COLORS[CUR_INDEX]
                else:
                   
                    pygame.draw.circle(canvas, brush_color, event.pos, brush_width)

            elif event.button == 3:  # Правая кнопка
                if pallete_rect.collidepoint(event.pos):
                  
                    dragging_pallete = True
                    offset = (event.pos[0] - pallete_rect.left, event.pos[1] - pallete_rect.top)
                else:
        
                    rect_start = event.pos
                    rect_current = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if dragging_pallete:
                    dragging_pallete = False
                elif rect_start:
                   
                    x1, y1 = rect_start
                    x2, y2 = rect_current
                    rect_w = abs(x2 - x1)
                    rect_h = abs(y2 - y1)
                    if rect_w > 5 and rect_h > 5:
                        rect = pygame.Rect(min(x1, x2), min(y1, y2), rect_w, rect_h)
                        rects.append((rect, brush_color))
                    rect_start = None
                    rect_current = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_pallete:
                new_pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
                pallete_rect.topleft = new_pos
            if rect_start:
                rect_current = mouse_pos

   
    if mouse_pressed[0] and not pallete_rect.collidepoint(mouse_pos):
        pygame.draw.circle(canvas, brush_color, mouse_pos, brush_width)

    
    screen.fill(background_color)
    screen.blit(canvas, (0, 0))

  
    for r, color in rects:
        pygame.draw.rect(screen, color, r, width=2)

    
    if rect_start and rect_current:
        x1, y1 = rect_start
        x2, y2 = rect_current
        rect_w = abs(x2 - x1)
        rect_h = abs(y2 - y1)
        rect = pygame.Rect(min(x1, x2), min(y1, y2), rect_w, rect_h)
        pygame.draw.rect(screen, brush_color, rect, width=2)

 
    draw_pallate()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
