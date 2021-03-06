#!./venv/bin/python

import pygame
import pygame.gfxdraw
from pygame.locals import *
#from GUI.mySprite import SpriteCards, Color, Number
#from GUI.myDrawables import DrawableCard

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3

        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

        pygame.display.flip()
        clock.tick(60)







sys.exit(0)

import os, sys

RESOLUTION = (1000, 500)

pygame.init()

screen = pygame.display.set_mode(RESOLUTION)

fake_screen = screen.copy()

print(os.getcwd())


spritesCards = SpriteCards('resources/sprites.png')




click_pos = (0, 0)

#c = DrawableCard(spritesCards, Card(Color.GREEN, Number.THREE), (400, RESOLUTION[1]*0.75), 30)


done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

fond = pygame.image.load("resources/table.jpg").convert()

while not done:

    screen.fill((0, 0, 0))
    screen.blit(c.getImage(), c.pos_)


    if c.isPointIn(pygame.mouse.get_pos()):
        pygame.gfxdraw.filled_polygon(screen, c.getPolygonTransformed(), (0, 120, 0, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        if event.type == pygame.MOUSEMOTION:
            if c.draggable_:
                mouse_x, mouse_y = event.pos
                c.pos_ = (mouse_x + offset_x, mouse_y + offset_y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if c.isPointIn(event.pos):
                mouse_x, mouse_y = event.pos
                offset_x = c.pos_[0] - mouse_x
                offset_y = c.pos_[1] - mouse_y
                c.draggable_ = True
            pass

        if event.type == pygame.MOUSEBUTTONUP:
            c.draggable_ = False
            pass

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3


    if is_blue: color = (0, 128, 255)
    else: color = (255, 100, 0)

    #sprite.draw(screen)

    #pygame.draw.rect(pic, color, pygame.Rect(x, y, 60, 60))
    #print(screen.get_size())
    #screen.blit(pic,(0,0))
    pygame.draw.circle(screen, (255,0,0), pygame.mouse.get_pos(), 5)
    pygame.display.flip()
    clock.tick(60)
