# Ian Davis jid7da 2d top down portal


import gamebox
import pygame
import math
import random
CAMERA_WIDTH, CAMERA_HEIGHT = 1000, 600
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
ticks = 0
background = gamebox.from_color(500, 460, "green", 2000, 50)
music = gamebox.load_sound("https://upload.wikimedia.org/wikipedia/commons/3/3c/Beat_electronic.ogg")
backgroundscreen = gamebox.from_image(550,400, "sea-water-ocean-storm.jpg")
backgroundscreen.scale_by(1)

playeroneimage = 'Goku-1.png'
playerone = gamebox.from_image(300, 0, playeroneimage)
playerone.scale_by(1.75)
status_affects_p1 = []
facing_left_p1 = False
animation_frame_count_p1 = 0
attackbox_p1_exists = False

playertwoimage = 'Goku-1.png'
playertwo = gamebox.from_image(700, 0, playertwoimage)
playerone.scale_by(1.75)
status_affects_p2 = []
facing_left_p2 = True
animation_frame_count_p2 = 0
attackbox_p2_exists = False


def tick(keys):
    global ticks
    global playeroneimage, playerone, status_affects_p1, facing_left_p1, animation_frame_count_p1, attackbox_p1_exists
    global playertwoimage, playertwo, status_affects_p2, facing_left_p2, animation_frame_count_p2, attackbox_p2_exists
    music.play(1)
    ticks +=1
    scoredisplay = gamebox.from_text(0, 0, "SCORE: " + str(ticks // 30), "Arial", 14, "red", italic=True)
    scoredisplay.top = camera.top
    scoredisplay.right = camera.right


    # MOVEMENT PLAYER ONE
    if pygame.K_UP in keys and playerone.touches(background):
        playerone.yspeed = -10
        status_affects_p1.append('airborne')

    if 'airborne' in status_affects_p1 and animation_frame_count_p1 == 0:
        playeroneimage = 'Goku-jump.png'

    if pygame.K_DOWN in keys and playerone.bottom_touches(background) and animation_frame_count_p1 == 0:
        playeroneimage = 'Goku-crouch.png'
        playerone.y = background.y - 30
    elif 'airborne' not in status_affects_p1 and animation_frame_count_p1 == 0:
        playeroneimage = 'Goku-1.png'

    if pygame.K_RIGHT in keys:
        facing_left_p1 = False
        if (playeroneimage != 'Goku-kick.png' and playeroneimage != 'Goku-shield.png') or 'airborne' in status_affects_p1:
            playerone.x += 4
        if (pygame.K_DOWN in keys or pygame.K_PERIOD in keys) and 'airborne' not in status_affects_p1 and animation_frame_count_p1 == 0:
            playerone.x += -4

    if pygame.K_LEFT in keys:
        facing_left_p1 = True
        if (playeroneimage != 'Goku-kick.png' and playeroneimage != 'Goku-shield.png') or 'airborne' in status_affects_p1:
            playerone.x += -4
        if (pygame.K_DOWN in keys or pygame.K_PERIOD in keys) and 'airborne' not in status_affects_p1 and animation_frame_count_p1 == 0:
            playerone.x += 4

    # MOVEMENT PLAYER TWO
    if pygame.K_w in keys and playertwo.touches(background):
        playertwo.yspeed = -10
        status_affects_p2.append('airborne')

    if 'airborne' in status_affects_p2 and animation_frame_count_p2 == 0:
        playertwoimage = 'Goku-jump.png'

    if pygame.K_s in keys and playertwo.bottom_touches(background) and animation_frame_count_p2 == 0:
        playertwoimage = 'Goku-crouch.png'
        playertwo.y = background.y - 30
    elif 'airborne' not in status_affects_p2 and animation_frame_count_p2 == 0:
        playertwoimage = 'Goku-1.png'

    if pygame.K_d in keys:
        facing_left_p2 = False
        if (playertwoimage != 'Goku-kick.png' and playertwoimage != 'Goku-shield.png') or 'airborne' in status_affects_p2:
            playertwo.x += 4
        if (pygame.K_s in keys or pygame.K_LSHIFT in keys) and 'airborne' not in status_affects_p2 and animation_frame_count_p2 == 0:
            playertwo.x += -4

    if pygame.K_a in keys:
        facing_left_p2 = True
        if (playertwoimage != 'Goku-kick.png' and playertwoimage != 'Goku-shield.png') or 'airborne' in status_affects_p2:
            playertwo.x += -4
        if (pygame.K_s in keys or pygame.K_LSHIFT in keys) and 'airborne' not in status_affects_p2 and animation_frame_count_p2 == 0:
            playertwo.x += 4

    #ATTACKS PLAYER ONE
    if pygame.K_PERIOD in keys and animation_frame_count_p1 == 0:
        if pygame.K_RIGHT in keys or pygame.K_LEFT in keys:
            playeroneimage = 'Goku-kick.png'
            animation_frame_count_p1 = 30
            attackbox_p1_exists = True
        if pygame.K_UP in keys:
            playeroneimage = 'Goku-Uppunch.png'
            animation_frame_count_p1 = 25
            playerone.yspeed -= -3
        if pygame.K_DOWN in keys:
            playeroneimage = 'Goku-shield.png'
            animation_frame_count_p1 = 10

    #ATTACKS PLAYER TWO
    if pygame.K_LSHIFT in keys and animation_frame_count_p2 == 0:
        if pygame.K_d in keys or pygame.K_a in keys:
            playertwoimage = 'Goku-kick.png'
            animation_frame_count_p2 = 30
            attackbox_p2_exists = True
        if pygame.K_w in keys:
            playertwoimage = 'Goku-Uppunch.png'
            animation_frame_count_p2 = 25
            playertwo.yspeed -= -3
        if pygame.K_s in keys:
            playertwoimage = 'Goku-shield.png'
            animation_frame_count_p2 = 10


    # DEBUG STUFF
    if status_affects_p1 != []:
        debug = gamebox.from_text(30,30, status_affects_p1[0], "Arial", 12, 'red', italic=True)
    else:
        debug = gamebox.from_text(30, 30, 'grounded', "Arial", 12, 'red', italic=True)

    # IMAGE CREATE PLAYER ONE
    # HITBOX CREATE PLAYER ONE
    yspeed_p1 = playerone.yspeed
    playerone = gamebox.from_image(playerone.x, playerone.y, playeroneimage)
    playerone.scale_by(1.75)
    playerone_hitbox = gamebox.from_color(playerone.x-5*(facing_left_p1 == False)+5*(facing_left_p1 == True), playerone.y+10, "green", 35, 60)
    if attackbox_p1_exists and playeroneimage == 'Goku-kick.png':
        attackbox_p1 = gamebox.from_color(playerone.x + 20 * (facing_left_p1 == False) - 20 * (facing_left_p1 == True), playerone.y + 5,
                       "red", 40, 20)
    playerone.yspeed = yspeed_p1
    playerone_hitbox.yspeed = yspeed_p1
    if facing_left_p1 == True:
        playerone.flip()

    playerone.yspeed += .5
    playerone.y = playerone.y + playerone.yspeed
    if playerone.bottom_touches(background):
        playerone.move_to_stop_overlapping(background)

    if playerone.y >= background.y -70 and 'airborne' in status_affects_p1:
        status_affects_p1.remove('airborne')

    # IMAGE CREATE PLAYER TWO
    # HITBOX CREATE PLAYER TWO
    yspeed_p2 = playertwo.yspeed
    playertwo = gamebox.from_image(playertwo.x, playertwo.y, playertwoimage)
    playertwo.scale_by(1.75)
    playertwo_hitbox = gamebox.from_color(playertwo.x-5*(facing_left_p2 == False)+5*(facing_left_p2 == True),playertwo.y+10, "green", 35, 60)
    if attackbox_p2_exists and playertwoimage == 'Goku-kick.png':
        attackbox_p2 = gamebox.from_color(playertwo.x + 20 * (facing_left_p2 == False) - 20 * (facing_left_p2 == True), playertwo.y + 5,
                       "red", 40, 20)
    playertwo.yspeed = yspeed_p2
    playertwo_hitbox.yspeed = yspeed_p2
    if facing_left_p2:
        playertwo.flip()

    playertwo.yspeed += .5
    playertwo.y = playertwo.y + playertwo.yspeed
    if playertwo.bottom_touches(background):
        playertwo.move_to_stop_overlapping(background)

    if playertwo.y >= background.y - 70 and 'airborne' in status_affects_p2:
        status_affects_p2.remove('airborne')

    # REDUCES ANIMATION DURATION
    animation_frame_count_p1 -= 1
    if animation_frame_count_p1 <= 0:
        animation_frame_count_p1 = 0
        attackbox_p1_exists = False

    animation_frame_count_p2 -= 1
    if animation_frame_count_p2 <= 0:
        animation_frame_count_p2 = 0
        attackbox_p2_exists = False

    camera.draw(backgroundscreen)
    camera.draw(scoredisplay)
    if debug:
        camera.draw(debug)
        camera.draw(playerone_hitbox)
        camera.draw(playertwo_hitbox)
        if attackbox_p2_exists and playertwoimage == 'Goku-kick.png':
            camera.draw(attackbox_p2)
        if attackbox_p1_exists and playeroneimage == 'Goku-kick.png':
            camera.draw(attackbox_p1)
    camera.draw(playerone)
    camera.draw(playertwo)
    camera.display()


ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
