# Ian Davis jid7da 2d top down portal


import gamebox
import pygame
import math
import random
CAMERA_WIDTH, CAMERA_HEIGHT = 1000, 600
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
playeroneimage = 'Goku-1.png'
playerone = gamebox.from_image(300, 300, playeroneimage)
playerone.scale_by(1.75)
ticks = 0
background = gamebox.from_color(500, 460, "green", 2000, 50)
music = gamebox.load_sound("https://upload.wikimedia.org/wikipedia/commons/3/3c/Beat_electronic.ogg")
backgroundscreen = gamebox.from_image(550,400, "sea-water-ocean-storm.jpg")
backgroundscreen.scale_by(1)
status_affects = []
facing_left = False
do_flip_image = False

def tick(keys):
    global playeroneimage, playerone, yspeed, ticks, status_affects, facing_left, do_flip_image
    music.play(1)
    ticks +=1
    scoredisplay = gamebox.from_text(0, 0, "SCORE: " + str(ticks // 30), "Arial", 14, "red", italic=True)
    scoredisplay.top = camera.top
    scoredisplay.right = camera.right

    if pygame.K_UP in keys and playerone.touches(background):
        playerone.yspeed = -10
        status_affects.append('airborne')
        keys.remove(pygame.K_UP)

    if 'airborne' in status_affects:
        playeroneimage = 'Goku-jump.png'

    if pygame.K_DOWN in keys and playerone.bottom_touches(background):
        playeroneimage = 'Goku-crouch.png'
        playerone.y = background.y - 30
    elif pygame.K_DOWN not in keys and playerone.bottom_touches(background) and status_affects == []:
        playeroneimage = 'Goku-1.png'

    if pygame.K_RIGHT in keys:
        facing_left = False
        playerone.x += 4
        if (pygame.K_DOWN in keys or pygame.K_PERIOD in keys) and 'airborne' not in status_affects:
            playerone.x += -4
        if pygame.K_PERIOD in keys:
            playeroneimage = 'Goku-kick.png'

    if pygame.K_LEFT in keys:
        facing_left = True
        playerone.x += -4
        if (pygame.K_DOWN in keys or pygame.K_PERIOD in keys) and 'airborne' not in status_affects:
            playerone.x += 4
        if pygame.K_PERIOD in keys:
            playeroneimage = 'Goku-kick.png'

    if status_affects != []:
        debug = gamebox.from_text(30,30, status_affects[0], "Arial", 12, 'red', italic=True)
    else:
        debug = gamebox.from_text(30, 30, 'grounded', "Arial", 12, 'red', italic=True)

    yspeed = playerone.yspeed
    playerone = gamebox.from_image(playerone.x, playerone.y, playeroneimage)
    playerone.scale_by(1.75)
    playerone.yspeed = yspeed
    if facing_left == True:
        playerone.flip()

    playerone.yspeed += .5
    playerone.y = playerone.y + playerone.yspeed
    if playerone.bottom_touches(background):
        playerone.move_to_stop_overlapping(background)

    if playerone.y >= background.y -70 and 'airborne' in status_affects:
        status_affects.remove('airborne')

    camera.draw(backgroundscreen)
    camera.draw(scoredisplay)
    if debug:
        camera.draw(debug)
    camera.draw(playerone)
    camera.display()

ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
