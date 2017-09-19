import pygame
import sys
from pygame.locals import *
import random
import math
import os
from challenges.MS_installer_emulator.RGB import ProgressiveBackgroundColor, ProgressiveForegroundFontParams

if __name__ == '__main__':
    pygame.init()
    screen_resolution = (1920, 1080)
    character_size = 60
    screen = pygame.display.set_mode(screen_resolution, pygame.FULLSCREEN)
    pygame.display.set_caption("Draw_ractangle_with_color_changes")

    bgc_color = ProgressiveBackgroundColor(500)
    fgf_color = ProgressiveForegroundFontParams(1000, screen_resolution, character_size)
    myfont = pygame.font.Font("d:\\sttfs\\msyh.ttf", 60)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        # change screen color
        next_bgc_color = bgc_color.next()
        screen.fill(next_bgc_color)

        next_font_params = fgf_color.next(next_bgc_color)

        if next_font_params["disappear"] is False:
            textImage = myfont.render(next_font_params["text"][0], True, next_font_params["color"])
            screen.blit(textImage, next_font_params["pos"])  # next_font_params["x_pos"]

        # update the screen
        pygame.display.update()
