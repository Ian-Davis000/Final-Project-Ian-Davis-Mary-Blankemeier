# Ian Davis jid7da 2d top down portal


import gamebox
import pygame
import math
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

def tick(keys):
    global playeroneimage, playerone, yspeed, ticks, status_affects
    music.play(1)
    ticks +=1
    scoredisplay = gamebox.from_text(0, 0, "SCORE: " + str(ticks // 30), "Arial", 14, "red", italic=True)
    scoredisplay.top = camera.top
    scoredisplay.right = camera.right

    if pygame.K_UP in keys and playerone.touches(background):
        playerone.yspeed = -10
        status_affects.append('airborne')

    if pygame.K_DOWN in keys and playerone.bottom_touches(background):
        playeroneimage = 'Goku-crouch.png'
        playerone.y = background.y - 30
    elif pygame.K_DOWN not in keys and playerone.bottom_touches(background) and status_affects == []:
        playeroneimage = 'Goku-1.png'

    if pygame.K_RIGHT in keys and pygame.K_DOWN not in keys:
        playerone.x += 4

    if pygame.K_LEFT in keys and pygame.K_DOWN not in keys:
        playerone.x += -4

    if 'airborne' in status_affects:
        playeroneimage = 'Goku-jump.png'

    yspeed = playerone.yspeed
    playerone = gamebox.from_image(playerone.x, playerone.y, playeroneimage)
    playerone.scale_by(1.75)
    playerone.yspeed = yspeed

    playerone.yspeed += .5
    playerone.y = playerone.y + playerone.yspeed
    if playerone.bottom_touches(background):
        playerone.move_to_stop_overlapping(background)

    if playerone.y < background.y -30 and 'airborne' in status_affects:
        status_affects.remove('airborne')

    camera.draw(backgroundscreen)
    camera.draw(scoredisplay)
    camera.draw(playerone)
    camera.display()

ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
