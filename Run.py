# Ian Davis jid7da 2d top down portal


import gamebox
import pygame
import math
CAMERA_WIDTH, CAMERA_HEIGHT = 1000, 600
BOX_WIDTH, BOX_HEIGHT = 20, 35
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
playeroneimage = 'Goku-1.png'
playerone = gamebox.from_image(300, 400, playeroneimage)
playerone.scale_by(1.75)
background = gamebox.from_color(500, 600, "green", 700, 50)
ticks = 0
music = gamebox.load_sound("https://upload.wikimedia.org/wikipedia/commons/3/3c/Beat_electronic.ogg")

def tick(keys):
    musicplay=msuic.play(-1)
    ticks +=1
    scoredisplay = gamebox.from_text(0, 0, "SCORE: " + str(ticks // 30), "Arial", 14, "red", italic=True)
    scoredisplay.top = camera.top
    scoredisplay.right = camera.right
    camera.draw(scoredisplay)
    global playeroneimage, playerone, yspeed
    camera.clear(gamebox.from_image(0,0, "https://pixabay.com/photo-1825469/")
    yspeed = playerone.yspeed
    playerone = gamebox.from_image(playerone.x, playerone.y, playeroneimage)
    playerone.yspeed = yspeed

    if pygame.K_UP in keys:
        playerone.yspeed = -10

    if pygame.K_DOWN in keys and playerone.touches(background):
        playeroneimage = 'Goku-crouch.png'
    elif pygame.K_DOWN not in keys and playerone.touches(background):
        playeroneimage = 'Goku-1.png'
    if pygame.K_RIGHT in keys:
        playerone.x += 4

    if pygame.K_LEFT in keys:
        playerone.x += -4

    playerone.yspeed += .5
    playerone.y = playerone.y + playerone.yspeed
    if playerone.touches(background):
        playerone.move_to_stop_overlapping(background)

    camera.draw(background)
    camera.draw(playerone)
    camera.display()



ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
