# Ian Davis jid7da Fighting Game
# Mary Blankemeier mhb5zf
# Sprites by AngryBoy on DBZVortex
# Splash Screen from
#
# Music from Dragon Ball

import gamebox
import pygame
import math
CAMERA_WIDTH, CAMERA_HEIGHT = 1000, 600
camera = gamebox.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
ticks = 0
background = gamebox.from_color(500, 570, "green", 2000, 50)
sidewalls = [gamebox.from_color(-100, 300, "green", 200, 1500), gamebox.from_color(1100, 300, "green", 200, 1500)]
music = gamebox.load_sound("Boss-5-looped.ogg")
kamehameha = gamebox.load_sound("Kamehameha.ogg")
backgroundscreen = gamebox.from_image(500, 200, "DBZBackground.png")
backgroundscreen.scale_by(1.7)
kamehameha_sprsheet = gamebox.load_sprite_sheet('Kamehameha-blast-2.png', 1, 9)
transform_sprsheet = gamebox.load_sprite_sheet('Goku-Saiyan-Transformation.png', 3, 5)

status_affects_p1 = []
facing_left_p1 = False
animation_frame_count_p1 = 0
attackbox_p1_exists = False
attackbox_p1 = gamebox.from_color(-100, -100, 'red', 1, 1)
on_hit_p1 = False
attack_cooldown_p1 = 0
doublejump_p1 = False
kamehameha_list_p1 = []
on_press_p1 = False
charge_p1 = 0
transform_bar_p1 = 0
transform_bar1_p1 = 0

status_affects_p2 = []
facing_left_p2 = True
animation_frame_count_p2 = 0
attackbox_p2_exists = False
attackbox_p2 = gamebox.from_color(1100, -100, 'red', 1, 1)
on_hit_p2 = False
attack_cooldown_p2 = 0
doublejump_p2 = False
kamehameha_list_p2 = []
on_press_p2 = False
charge_p2 = 0
transform_bar_p2 = 0
transform_bar1_p2 = 0

splash_screen = gamebox.from_image(CAMERA_WIDTH/2, CAMERA_HEIGHT/2+20, 'Goku-VS-Frieza.png')
splash_screen.width = camera.width
show_splash = True
character_select = False


def splash(keys):
    global show_splash
    global character_select
    global ticks
    if ticks == 0:
        pygame.mixer.music.load("Piccolos Theme.ogg")
        pygame.mixer.music.play(-1)
    camera.draw(splash_screen)
    camera.display()
    if keys:
        show_splash = False
        character_select = True
        #pygame.mixer.Channel(1).play(pygame.mixer.Sound('misc_menu_4.wav'))
        ticks = -1
    ticks += 1


character_select_pic = gamebox.from_image(CAMERA_WIDTH/2, CAMERA_HEIGHT/2, 'Goku-Vegeta.png')
character_select_pic.height = camera.height
character_list = ['Goku-sprite-sheet.png','Goku-sprite-sheet-red.png']
character_p1 = 0
character_p2 = 0
icons = gamebox.load_sprite_sheet('Big Icons.png', 1, 10)
select_highlight_toggle_p1 = False
select_highlight_toggle_p2 = False


def character_select_screen(keys):
    global character_select, character_p1, character_p2, ticks, select_highlight_toggle_p1, select_highlight_toggle_p2
    global playerone, playertwo, sprsheet_p1, sprsheet_p2
    if ticks == 0:
        pygame.mixer.music.load("Perfect Cell Theme.ogg")
        pygame.mixer.music.play(-1)
    if pygame.K_LEFT in keys and not select_highlight_toggle_p1:
        character_p1 -= 1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('click.wav'))
    if pygame.K_RIGHT in keys and not select_highlight_toggle_p1:
        character_p1 += 1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('click.wav'))
    if pygame.K_PERIOD in keys:
        select_highlight_toggle_p1 = not select_highlight_toggle_p1
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('misc_menu_4.wav'))
    if pygame.K_a in keys and not select_highlight_toggle_p2:
        character_p2 -= 1
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('click.wav'))
    if pygame.K_d in keys and not select_highlight_toggle_p2:
        character_p2 += 1
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('click.wav'))
    if pygame.K_LSHIFT in keys:
        select_highlight_toggle_p2 = not select_highlight_toggle_p2
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('misc_menu_4.wav'))
    if (pygame.K_COMMA in keys or pygame.K_LCTRL in keys) and (select_highlight_toggle_p1 and select_highlight_toggle_p2):
        character_select = False
        ticks = -1
        sprsheet_p1 = gamebox.load_sprite_sheet(character_list[character_p1%len(character_list)], 9, 11)
        sprsheet_p2 = gamebox.load_sprite_sheet(character_list[character_p2%len(character_list)], 9, 11)
        playerone = gamebox.from_image(300, 0, sprsheet_p1[0])
        playerone.scale_by(1.75)
        playertwo = gamebox.from_image(700, 0, sprsheet_p2[0])
        playertwo.scale_by(1.75)
    keys.clear()
    select_highlight_p1 = gamebox.from_color(100, 350, 'gold', 130, 178)
    select_highlight_p2 = gamebox.from_color(300, 350, 'gold', 130, 178)
    character1 = gamebox.from_image(100, 350, icons[character_p1%2])
    character2 = gamebox.from_image(300, 350, icons[character_p2%2])
    camera.draw(character_select_pic)
    if select_highlight_toggle_p1:
        camera.draw(select_highlight_p1)
    if select_highlight_toggle_p2:
        camera.draw(select_highlight_p2)
    camera.draw(character1)
    camera.draw(character2)
    camera.display()
    ticks += 1


def tick(keys):
    global ticks, sprsheet_p1, sprsheet_p2, kamehameha_sprsheet, kamehameha
    global playeroneimage, playerone, status_affects_p1, facing_left_p1, animation_frame_count_p1, attackbox_p1_exists
    global attackbox_p1, on_hit_p1, attack_cooldown_p1, doublejump_p1, kamehameha_list_p1, on_press_p1, charge_p1
    global transform_bar_p1, transform_bar1_p1
    global playertwoimage, playertwo, status_affects_p2, facing_left_p2, animation_frame_count_p2, attackbox_p2_exists
    global attackbox_p2, on_hit_p2, attack_cooldown_p2, doublejump_p2, kamehameha_list_p2, on_press_p2, charge_p2
    global transform_bar_p2, transform_bar1_p2
    if show_splash:
        splash(keys)
        keys.clear()
        return
    if character_select:
        character_select_screen(keys)
        keys.clear()
        return
    if ticks == 0:
        pygame.mixer.music.load("Boss-5-looped.ogg")
        pygame.mixer.music.play(-1)
    ticks += 1
    scoredisplay = gamebox.from_text(0, 0, "SCORE: " + str(ticks // 30), "Arial", 14, "red", italic=True)
    scoredisplay.top = camera.top
    scoredisplay.right = camera.right

    # MOVEMENT PLAYER ONE #####
    # UP
    if pygame.K_UP in keys and playerone.touches(background):
        playerone.yspeed = -10
        status_affects_p1.append('airborne')
    if not playerone.touches(background) and not doublejump_p1 and pygame.K_UP in keys:
        doublejump_p1 = True
        playerone.yspeed = -10
    if playerone.touches(background):
        doublejump_p1 = False
    if 'airborne' in status_affects_p1 and animation_frame_count_p1 == 0:
        playeroneimage = sprsheet_p1[2]
    # DOWN
    if pygame.K_DOWN in keys and playerone.bottom_touches(background) and animation_frame_count_p1 == 0:
        playeroneimage = sprsheet_p1[1]
        playerone.y = background.y - 30
    elif 'airborne' not in status_affects_p1 and animation_frame_count_p1 == 0:
        playeroneimage = sprsheet_p1[0]
    # RIGHT
    if pygame.K_RIGHT in keys:
        facing_left_p1 = False
        if playeroneimage == sprsheet_p1[0] or playeroneimage == sprsheet_p1[2] or 'airborne' in status_affects_p1:
            playerone.x += 4
    # LEFT
    if pygame.K_LEFT in keys:
        facing_left_p1 = True
        if playeroneimage == sprsheet_p1[0] or playeroneimage == sprsheet_p1[2] or 'airborne' in status_affects_p1:
            playerone.x += -4

    # MOVEMENT PLAYER TWO ######
    # UP
    if pygame.K_w in keys and playertwo.touches(background):
        playertwo.yspeed = -10
        status_affects_p2.append('airborne')
    if not playertwo.touches(background) and not doublejump_p2 and pygame.K_w in keys:
        doublejump_p2 = True
        playertwo.yspeed = -10
    if playertwo.touches(background):
        doublejump_p2 = False
    if 'airborne' in status_affects_p2 and animation_frame_count_p2 == 0:
        playertwoimage = sprsheet_p2[2]
    # DOWN
    if pygame.K_s in keys and playertwo.bottom_touches(background) and animation_frame_count_p2 == 0:
        playertwoimage = sprsheet_p2[1]
        playertwo.y = background.y - 30
    elif 'airborne' not in status_affects_p2 and animation_frame_count_p2 == 0:
        playertwoimage = sprsheet_p2[0]
    # RIGHT
    if pygame.K_d in keys:
        facing_left_p2 = False
        if playertwoimage == sprsheet_p2[0] or playertwoimage == sprsheet_p2[2] or 'airborne' in status_affects_p2:
            playertwo.x += 4
    # LEFT
    if pygame.K_a in keys:
        facing_left_p2 = True
        if playertwoimage == sprsheet_p2[0] or playertwoimage == sprsheet_p2[2] or 'airborne' in status_affects_p2:
            playertwo.x += -4

    # ATTACKS PLAYER ONE
    if pygame.K_PERIOD in keys and animation_frame_count_p1 == 0 and attack_cooldown_p1 == 0:
        if pygame.K_RIGHT in keys or pygame.K_LEFT in keys:
            playeroneimage = sprsheet_p1[5]
            animation_frame_count_p1 = 20
            attackbox_p1_exists = True
            on_hit_p2 = False
        if pygame.K_UP in keys:
            playeroneimage = sprsheet_p1[6]
            animation_frame_count_p1 = 25
            playerone.yspeed -= -3
            attackbox_p1_exists = True
            on_hit_p2 = False
    if pygame.K_PERIOD in keys and animation_frame_count_p1 == 0:
        if pygame.K_DOWN in keys:
            playeroneimage = sprsheet_p1[3]
            animation_frame_count_p1 = 10
    # EMPOWERED ATTACKS PLAYER ONE
    if pygame.K_COMMA in keys and animation_frame_count_p1 == 0 and attack_cooldown_p1 == 0:
        if pygame.K_RIGHT in keys or pygame.K_LEFT in keys:
            animation_frame_count_p1 = 60
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Kamehameha.ogg'))
            kamehameha_list_p1.append([gamebox.from_color(-30, -100, 'red', 1, 1), True, False])
    if pygame.K_COMMA in keys and animation_frame_count_p1 == 0 and attack_cooldown_p1 == 0:
        if pygame.K_DOWN in keys:
            playeroneimage = transform_sprsheet[ticks//5 % 2]
            charge_p1 += 40/480
            transform_bar_p1 = gamebox.from_color(playerone.x+charge_p1/2-25+10*facing_left_p1, playerone.y+20, 'white', charge_p1, 4)
            transform_bar1_p1 = gamebox.from_color(playerone.x-5+10*facing_left_p1, playerone.y+20, 'black', 42, 6)
            if charge_p1 >= 40:
                charge_p1 = 0
                sprsheet_p1 = gamebox.load_sprite_sheet('goku-ss-sprite-sheet.png', 9, 11)
                keys.remove(pygame.K_DOWN)
            if on_press_p1:
                on_press_p1 = False
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('Goku Screaming.ogg'))
    if pygame.K_DOWN not in keys or playeroneimage not in transform_sprsheet:
        on_press_p1 = True
        transform_bar_p1 = 0
        transform_bar1_p1 = 0
        if not kamehameha_list_p1:
            pygame.mixer.Channel(1).stop()

        # ATTACKS PLAYER TWO
    if pygame.K_LSHIFT in keys and animation_frame_count_p2 == 0 and attack_cooldown_p2 == 0:
        if pygame.K_d in keys or pygame.K_a in keys:
            playertwoimage = sprsheet_p2[5]
            animation_frame_count_p2 = 20
            attackbox_p2_exists = True
            on_hit_p1 = False
        if pygame.K_w in keys:
            playertwoimage = sprsheet_p2[6]
            animation_frame_count_p2 = 25
            playertwo.yspeed -= -3
            attackbox_p2_exists = True
            on_hit_p1 = False
    if pygame.K_LSHIFT in keys and animation_frame_count_p2 == 0:
        if pygame.K_s in keys:
            playertwoimage = sprsheet_p2[3]
            animation_frame_count_p2 = 10
    # EMPOWERED ATTACKS PLAYER TWO
    if pygame.K_LCTRL in keys and animation_frame_count_p2 == 0 and attack_cooldown_p2 == 0:
        if pygame.K_a in keys or pygame.K_d in keys:
            animation_frame_count_p2 = 60
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('Kamehameha.ogg'))
            kamehameha_list_p2.append([gamebox.from_color(-30, -100, 'red', 1, 1), True, False])
    if pygame.K_LCTRL in keys and animation_frame_count_p2 == 0 and attack_cooldown_p2 == 0:
        if pygame.K_s in keys:
            playertwoimage = transform_sprsheet[ticks//5 % 2]
            charge_p2 += .085
            transform_bar_p2 = gamebox.from_color(playertwo.x+charge_p2/2-25+10*facing_left_p2, playertwo.y+20, 'white', charge_p2, 4)
            transform_bar1_p2 = gamebox.from_color(playertwo.x-5+10*facing_left_p2, playertwo.y+20, 'black', 42, 6)
            if charge_p2 >= 40:
                charge_p2 = 0
                sprsheet_p2 = gamebox.load_sprite_sheet('goku-ss-sprite-sheet.png', 9, 11)
                keys.remove(pygame.K_s)
            if on_press_p2:
                on_press_p2 = False
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('Goku Screaming.ogg'))
    if pygame.K_s not in keys or playertwoimage not in transform_sprsheet:
        on_press_p2 = True
        transform_bar_p2 = 0
        transform_bar1_p2 = 0
        if not kamehameha_list_p2:
            pygame.mixer.Channel(2).stop()

    # REMOVES JUMP KEY TO ALLOW DOUBLE JUMP - MUST GO AFTER ATTACKS
    if pygame.K_UP in keys:
        keys.remove(pygame.K_UP)
    if pygame.K_w in keys:
        keys.remove(pygame.K_w)

    # PROJECTILES P1
    kmhmh = 0
    while kmhmh < len(kamehameha_list_p1):
        if kamehameha_list_p1[kmhmh][1]:
            if animation_frame_count_p1 >= 20:
                playeroneimage = sprsheet_p1[math.floor(25-animation_frame_count_p1*12/40)]
            if animation_frame_count_p1 <= 20:
                playeroneimage = sprsheet_p1[19]
                attackbox_p1_exists = True
            if animation_frame_count_p1 == 20:
                kamehameha_list_p1[kmhmh][0].x = playerone.x+40-80*facing_left_p1
                kamehameha_list_p1[kmhmh][0].y = playerone.y+10
                kamehameha_list_p1[kmhmh][2] = facing_left_p1
            if animation_frame_count_p1 == 0:
                kamehameha_list_p1[kmhmh][1] = False
        kamehameha_image = kamehameha_sprsheet[math.floor(ticks//5 % 9)]
        kamehameha_list_p1[kmhmh][0] = gamebox.from_image(kamehameha_list_p1[kmhmh][0].x, kamehameha_list_p1[kmhmh][0].y, kamehameha_image)
        kamehameha_list_p1[kmhmh][0].x += 8 - 16*(kamehameha_list_p1[kmhmh][2])
        kamehameha_list_p1[kmhmh][0].scale_by(1.75)
        if kamehameha_list_p1[kmhmh][2]:
            kamehameha_list_p1[kmhmh][0].flip()
        if -50 > kamehameha_list_p1[kmhmh][0].x or kamehameha_list_p1[kmhmh][0].x > CAMERA_WIDTH + 50:
            kamehameha_list_p1.remove(kamehameha_list_p1[kmhmh])
        kmhmh += 1

    # PROJECTILES P2
    kmhmh = 0
    while kmhmh < len(kamehameha_list_p2):
        if kamehameha_list_p2[kmhmh][1]:
            if animation_frame_count_p2 >= 20:
                playertwoimage = sprsheet_p2[math.floor(25-animation_frame_count_p2*12/40)]
            if animation_frame_count_p2 <= 20:
                playertwoimage = sprsheet_p2[19]
                attackbox_p2_exists = True
            if animation_frame_count_p2 == 20:
                kamehameha_list_p2[kmhmh][0].x = playertwo.x+40-80*facing_left_p2
                kamehameha_list_p2[kmhmh][0].y = playertwo.y+10
                kamehameha_list_p2[kmhmh][2] = facing_left_p2
            if animation_frame_count_p2 == 0:
                kamehameha_list_p2[kmhmh][1] = False
        kamehameha_image = kamehameha_sprsheet[math.floor(ticks//5 % 9)]
        kamehameha_list_p2[kmhmh][0] = gamebox.from_image(kamehameha_list_p2[kmhmh][0].x, kamehameha_list_p2[kmhmh][0].y, kamehameha_image)
        kamehameha_list_p2[kmhmh][0].x += 8 - 16*(kamehameha_list_p2[kmhmh][2])
        kamehameha_list_p2[kmhmh][0].scale_by(1.75)
        if kamehameha_list_p2[kmhmh][2]:
            kamehameha_list_p2[kmhmh][0].flip()
        if -50 > kamehameha_list_p2[kmhmh][0].x or kamehameha_list_p2[kmhmh][0].x > CAMERA_WIDTH + 50:
            kamehameha_list_p2.remove(kamehameha_list_p2[kmhmh])
        kmhmh += 1

    # IMAGE CREATE PLAYER ONE
    # HITBOX CREATE PLAYER ONE
    yspeed_p1 = playerone.yspeed
    xspeed_p1 = playerone.xspeed
    playerone = gamebox.from_image(playerone.x, playerone.y, playeroneimage)
    playerone.scale_by(1.75)
    playerone_hitbox = gamebox.from_color(playerone.x-5+10*facing_left_p1, playerone.y+10, "green", 35, 60)
    if attackbox_p1_exists:
        if playeroneimage == sprsheet_p1[5]:
            attackbox_p1 = gamebox.from_color(playerone.x + 20 - 40 * facing_left_p1, playerone.y + 11, "red", 40, 20)
        if playeroneimage == sprsheet_p1[6]:
            attackbox_p1 = gamebox.from_color(playerone.x + 10-20*facing_left_p1, playerone.y - 25, "red", 30, 20)
    playerone.yspeed = yspeed_p1
    playerone.xspeed = xspeed_p1
    playerone_hitbox.yspeed = yspeed_p1
    if facing_left_p1:
        playerone.flip()

    playerone.yspeed += .5
    playerone.y = playerone.y + playerone.yspeed
    playerone.x = playerone.x + playerone.xspeed
    if playerone.bottom_touches(background):
        playerone.move_to_stop_overlapping(background)
    for sidewall in sidewalls:
        if playerone.touches(sidewall):
            playerone.move_to_stop_overlapping(sidewall)

    if playerone.y >= background.y - 70 and 'airborne' in status_affects_p1:
        status_affects_p1.remove('airborne')
    playerone.xspeed = playerone.xspeed*.9

    # IMAGE CREATE PLAYER TWO
    # HITBOX CREATE PLAYER TWO
    yspeed_p2 = playertwo.yspeed
    xspeed_p2 = playertwo.xspeed
    playertwo = gamebox.from_image(playertwo.x, playertwo.y, playertwoimage)
    playertwo.scale_by(1.75)
    playertwo_hitbox = gamebox.from_color(playertwo.x-5+10*facing_left_p2, playertwo.y+10, "green", 35, 60)
    if attackbox_p2_exists:
        if playertwoimage == sprsheet_p2[5]:
            attackbox_p2 = gamebox.from_color(playertwo.x + 20 - 40 * facing_left_p2, playertwo.y + 11, "red", 40, 20)
        if playertwoimage == sprsheet_p2[6]:
            attackbox_p2 = gamebox.from_color(playertwo.x + 10-20*facing_left_p2, playertwo.y - 25, "red", 30, 20)
    playertwo.yspeed = yspeed_p2
    playertwo.xspeed = xspeed_p2
    playertwo_hitbox.yspeed = yspeed_p2
    if facing_left_p2:
        playertwo.flip()

    playertwo.yspeed += .5
    playertwo.y = playertwo.y + playertwo.yspeed
    playertwo.x = playertwo.x + playertwo.xspeed
    if playertwo.bottom_touches(background):
        playertwo.move_to_stop_overlapping(background)
    for sidewall in sidewalls:
        if playertwo.touches(sidewall):
            playertwo.move_to_stop_overlapping(sidewall)

    if playertwo.y >= background.y - 70 and 'airborne' in status_affects_p2:
        status_affects_p2.remove('airborne')
    playertwo.xspeed = playertwo.xspeed*.9

    # HITBOX DETECTION
    for kmhmh in range(0, len(kamehameha_list_p2)):
        if kamehameha_list_p2[kmhmh][0].touches(playerone_hitbox):
            doublejump_p2 = False
            if playeroneimage in transform_sprsheet:
                charge_p1 = 0
            if playeroneimage == sprsheet_p1[3] and kamehameha_list_p2[kmhmh][2] != facing_left_p1:
                playerone.xspeed = 2 - (4 * kamehameha_list_p2[kmhmh][2])
            else:
                playeroneimage = sprsheet_p1[4]
                animation_frame_count_p1 = 20
                playerone.xspeed = 5 - (10 * kamehameha_list_p2[kmhmh][2])
            if kamehameha_list_p2[kmhmh][2] and playertwoimage != sprsheet_p2[3]:
                facing_left_p1 = False
            elif not kamehameha_list_p2[kmhmh][2] and playertwoimage != sprsheet_p2[3]:
                facing_left_p1 = True
    if attackbox_p2.touches(playerone_hitbox) and not on_hit_p1:
        on_hit_p1 = True
        doublejump_p2 = False
        if playeroneimage in transform_sprsheet:
            charge_p1 = 0
        if playertwoimage == sprsheet_p2[5] and (playeroneimage != sprsheet_p1[3] or facing_left_p1 == facing_left_p2):
            playerone.xspeed = -2
            playerone.xspeed = 10 - (20 * facing_left_p2)
            playeroneimage = sprsheet_p1[4]
            animation_frame_count_p1 = 20
        elif playertwoimage == sprsheet_p2[6] and (playeroneimage != sprsheet_p1[3] or facing_left_p1 == facing_left_p2):
            playeroneimage = sprsheet_p1[20]
            animation_frame_count_p1 = 20
            playerone.yspeed = -10
            playerone.xspeed = 2 - (4 * facing_left_p2)
        elif (playertwoimage == sprsheet_p2[5] or playertwoimage == sprsheet_p2[6]) and playeroneimage == sprsheet_p1[3] and facing_left_p1 != facing_left_p2:
            playerone.xspeed = 2 - (4 * facing_left_p2)
        if facing_left_p2 and playeroneimage != sprsheet_p1[3]:
            facing_left_p1 = False
        elif not facing_left_p2 and playeroneimage != sprsheet_p1[3]:
            facing_left_p1 = True

    for kmhmh in range(0, len(kamehameha_list_p1)):
        if kamehameha_list_p1[kmhmh][0].touches(playertwo_hitbox):
            doublejump_p1 = False
            if playertwoimage in transform_sprsheet:
                charge_p2 = 0
            if playertwoimage == sprsheet_p2[3] and kamehameha_list_p1[kmhmh][2] != facing_left_p2:
                playertwo.xspeed = 2 - (4 * kamehameha_list_p1[kmhmh][2])
            else:
                playertwoimage = sprsheet_p2[4]
                animation_frame_count_p2 = 20
                playertwo.xspeed = 5 - (10 * kamehameha_list_p1[kmhmh][2])
            if kamehameha_list_p1[kmhmh][2] and playeroneimage != sprsheet_p1[3]:
                facing_left_p2 = False
            elif not kamehameha_list_p1[kmhmh][2] and playeroneimage != sprsheet_p1[3]:
                facing_left_p2 = True
    if attackbox_p1.touches(playertwo_hitbox) and not on_hit_p2:
        on_hit_p2 = True
        doublejump_p1 = False
        if playertwoimage in transform_sprsheet:
            charge_p2 = 0
        if playeroneimage == sprsheet_p1[5] and (playertwoimage != sprsheet_p2[3] or facing_left_p1 == facing_left_p2):
            playertwo.yspeed = -2
            playertwo.xspeed = 10 - (20 * facing_left_p1)
            playertwoimage = sprsheet_p2[4]
            animation_frame_count_p2 = 20
        elif playeroneimage == sprsheet_p1[6] and (playertwoimage != sprsheet_p2[3] or facing_left_p1 == facing_left_p2):
            playertwoimage = sprsheet_p2[20]
            animation_frame_count_p2 = 20
            playertwo.yspeed = -10
            playertwo.xspeed = 2 - (4 * facing_left_p1)
        elif playertwoimage == sprsheet_p2[3] and facing_left_p1 != facing_left_p2:
            playertwo.xspeed = 2 - (4 * facing_left_p1)
        if facing_left_p1 and playeroneimage != sprsheet_p1[3]:
            facing_left_p2 = False
        elif not facing_left_p1 and playeroneimage != sprsheet_p1[3]:
            facing_left_p2 = True

    # REDUCES ANIMATION DURATION
    # ATTACK COOLDOWNS
    if animation_frame_count_p1 <= 0:
        animation_frame_count_p1 = 0
        attackbox_p1_exists = False
        attackbox_p1 = gamebox.from_color(-100, -100, 'red', 1, 1)
        if attack_cooldown_p1 > 0:
            attack_cooldown_p1 -= 1
    else:
        animation_frame_count_p1 -= 1
        if animation_frame_count_p1 == 0:
            attack_cooldown_p1 = 10

    if animation_frame_count_p2 <= 0:
        animation_frame_count_p2 = 0
        attackbox_p2_exists = False
        attackbox_p2 = gamebox.from_color(1100, -100, 'red', 1, 1)
        if attack_cooldown_p2 > 0:
            attack_cooldown_p2 -= 1
    else:
        animation_frame_count_p2 -= 1
        if animation_frame_count_p2 == 0:
            attack_cooldown_p2 = 10

    camera.draw(backgroundscreen)
    camera.draw(scoredisplay)
    debug = False
    if debug:
        camera.draw(playerone_hitbox)
        camera.draw(playertwo_hitbox)
        if attackbox_p2_exists:  # and (playertwoimage == 'Goku-kick.png' or playertwoimage == 'Goku-Uppunch.png'):
            camera.draw(attackbox_p2)
        if attackbox_p1_exists:  # and (playeroneimage == 'Goku-kick.png' or playeroneimage == 'Goku-Uppunch.png'):
            camera.draw(attackbox_p1)
    camera.draw(playerone)
    camera.draw(playertwo)
    if transform_bar1_p1 != 0:
        camera.draw(transform_bar1_p1)
    if transform_bar_p1 != 0:
        camera.draw(transform_bar_p1)
    if transform_bar1_p2 != 0:
        camera.draw(transform_bar1_p2)
    if transform_bar_p2 != 0:
        camera.draw(transform_bar_p2)
    for kmhmh in range(0, len(kamehameha_list_p1)):
        camera.draw(kamehameha_list_p1[kmhmh][0])
    for kmhmh in range(0, len(kamehameha_list_p2)):
        camera.draw(kamehameha_list_p2[kmhmh][0])
    camera.display()


ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
