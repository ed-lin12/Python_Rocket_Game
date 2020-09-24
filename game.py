import pygame
import rocket
import enemy_ufo
import alien
import sprites
import random

# initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# create a game display
pygame.display.set_icon(sprites.icon)
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

# font downloaded from: http://www.dafont.com/8-bit-madness.font
font = 'data/sprites/8-Bit-Madness.ttf'

# initialize BGM : Duck Tales - "The Moon"
pygame.mixer.music.load('data/sounds/moon.mp3')
pygame.mixer_music.set_volume(1)
pygame.mixer.music.play(-1)



# text rendering function
def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# sprite pixel format converting
for convert_sprites in sprites.all_sprites:
    convert_sprites.convert_alpha()

# framerate
clock = pygame.time.Clock()
FPS = 30

# player variables
player = rocket.Rocket(100, display_height/2-40)
moving = True
godmode = False

# score variables
score = 0
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())

# enemy rocket variables
enemy_ufo = enemy_ufo.EnemyUfo(-200, display_height/2-40)
enemy_ufo_alive = False

# alien variables
alien = alien.Alien(-200, 400)
alien_alive = False

# spaceship variables
spaceship_x = 800
spaceship_y = random.randint(0, 400)
spaceship_alive = False
spaceship_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen("!", font, 200, red)

# asteroid variables
asteroid_x = -200
asteroid_y = random.randint(0, 400)

# extra life variables
extra_life_x = -200
extra_life_y = random.randint(0, 400)

# bullet variables
bullets = []

# bomb variables
bombs = []

# sounds
shoot = pygame.mixer.Sound('data/sounds/shoot.wav')
pop = pygame.mixer.Sound('data/sounds/pop.wav')
bomb = pygame.mixer.Sound('data/sounds/bomb.wav')
explosion = pygame.mixer.Sound('data/sounds/explosion.wav')
explosion2 = pygame.mixer.Sound('data/sounds/explosion2.wav')
select = pygame.mixer.Sound('data/sounds/select.wav')
select2 = pygame.mixer.Sound('data/sounds/select2.wav')
alert = pygame.mixer.Sound('data/sounds/alert.wav')
whoosh = pygame.mixer.Sound('data/sounds/whoosh.wav')
oneup = pygame.mixer.Sound('data/sounds/1-up.wav')

# main menu
def main_menu():

    menu = True

    selected = "play"

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = "play"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = "quit"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select2)
                    if selected == "play":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # drawing background
        game_display.blit(sprites.background, (0, 0))

        if godmode:
            title = message_to_screen("ROCKET (GODMODE)", font, 80, yellow)
        else:
            title = message_to_screen("ROCKET", font, 100, white)
        controls_1 = message_to_screen("use WASD to move, SPACE to shoot,", font, 30, white)
        controls_2 = message_to_screen("L-SHIFT to drop bombs, and P to toggle pause", font, 30, white)
        if selected == "play":
            play = message_to_screen("PLAY", font, 75, green)
        else:
            play = message_to_screen("PLAY", font, 75, white)
        if selected == "quit":
            game_quit = message_to_screen("QUIT", font, 75, green)
        else:
            game_quit = message_to_screen("QUIT", font, 75, white)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        controls_2_rect = controls_2.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()

        # drawing text
        game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40))
        game_display.blit(controls_1, (display_width/2 - (controls_1_rect[2]/2), 120))
        game_display.blit(controls_2, (display_width/2 - (controls_2_rect[2]/2), 140))
        game_display.blit(play, (display_width/2 - (play_rect[2]/2), 200))
        game_display.blit(game_quit, (display_width/2 - (quit_rect[2]/2), 260))

        pygame.display.update()
        pygame.display.set_caption("ROCKET by Ed Lin")


def pause():

    global highscore_file
    global highscore_int

    paused = True

    player.moving_up = False
    player.moving_left = False
    player.moving_down = False
    player.moving_right = False

    paused_text = message_to_screen("PAUSED", font, 100, white)
    paused_text_rect = paused_text.get_rect()

    game_display.blit(paused_text, (display_width/2 - (paused_text_rect[2]/2), 40))

    pygame.display.update()
    clock.tick(15)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.Sound.play(select)
                    paused = False

# create a game loop
def game_loop():

    global spaceship_x
    global spaceship_y
    global spaceship_alive
    global spaceship_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file
    global highscore_int
    global score

    global asteroid_x
    global asteroid_y

    global extra_life_x
    global extra_life_y

    global enemy_ufo_alive

    global alien_alive

    game_exit = False
    game_over = False

    game_over_selected = "play again"

    while not game_exit:

        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "play again"
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "quit"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(select2)
                        if game_over_selected == "play again":
                            if score > highscore_int:
                                highscore_file = open('highscore.dat', "w")
                                highscore_file.write(str(score))
                                highscore_file.close()
                            game_over = False

                            score = 0

                            asteroid_x = 800
                            extra_life_x = 800

                            enemy_ufo.x = -200
                            enemy_ufo_alive = False
                            enemy_ufo.bullets = []

                            alien.x = -200
                            alien_alive = False
                            alien.bullets = []

                            spaceship_x = 800
                            spaceship_alive = False
                            warning = False
                            warning_counter = 0
                            warning_counter = 0

                            player.wreck_start = False
                            player.y = display_height/2-40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            game_loop()
                        if game_over_selected == "quit":
                            pygame.quit()
                            quit()

            game_over_text = message_to_screen("GAME OVER", font, 100, white)
            your_score = message_to_screen("YOUR SCORE WAS: " + str(score), font, 50, white)
            if game_over_selected == "play again":
                play_again = message_to_screen("PLAY AGAIN", font, 75, green)
            else:
                play_again = message_to_screen("PLAY AGAIN", font, 75, white)
            if game_over_selected == "quit":
                game_quit = message_to_screen("QUIT", font, 75, green)
            else:
                game_quit = message_to_screen("QUIT", font, 75, white)

            game_over_rect = game_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            game_display.blit(game_over_text, (display_width/2 - game_over_rect[2]/2, 40))
            game_display.blit(your_score, (display_width/2 - (your_score_rect[2]/2+5), 100))
            game_display.blit(play_again, (display_width/2 - play_again_rect[2]/2, 200))
            game_display.blit(game_quit, (display_width/2 - game_quit_rect[2]/2, 260))

            pygame.display.update()
            pygame.display.set_caption("ROCKET running at " + str(int(clock.get_fps())) + " frames per second.")
            clock.tick(10)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()

            if moving:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.moving_up = True
                    if event.key == pygame.K_a:
                        player.moving_left = True
                    if event.key == pygame.K_s:
                        player.moving_down = True
                    if event.key == pygame.K_d:
                        player.moving_right = True
                    if event.key == pygame.K_SPACE:
                        if not player.wreck_start:
                            pygame.mixer.Sound.play(shoot)
                            bullets.append([player.x, player.y])
                    if event.key == pygame.K_LSHIFT:
                        if not player.wreck_start:
                            pygame.mixer.Sound.play(bomb)
                            bombs.append([player.x, player.y])
                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(select)
                        pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player.moving_up = False
                    if event.key == pygame.K_a:
                        player.moving_left = False
                    if event.key == pygame.K_s:
                        player.moving_down = False
                    if event.key == pygame.K_d:
                        player.moving_right = False

        if player.health < 1:
            pygame.mixer.Sound.play(explosion)
            player.wreck()

        if player.wrecked:
            game_over = True

        # draw background
        game_display.blit(sprites.background, (0, 0))

        # drawing player
        game_display.blit(player.current, (player.x, player.y))

        # drawing enemy rocket
        game_display.blit(enemy_ufo.current, (enemy_ufo.x, enemy_ufo.y))

        # drawing spaceship
        game_display.blit(sprites.spaceship, (spaceship_x, spaceship_y))

        # drawing alien
        game_display.blit(sprites.alien, (alien.x, alien.y))

        # enabling movement and animations
        player.player_init()
        enemy_ufo.init()
        alien.init()

        # rendering bullets
        if not player.wreck_start and not player.wrecked:
            for draw_bullet in bullets:
                pygame.draw.rect(game_display, white, (draw_bullet[0]+130, draw_bullet[1]+92.5, 20, 10))
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] += 40
            for del_bullet in bullets:
                if del_bullet[0] >= 800:
                    bullets.remove(del_bullet)

        # rendering bombs
        if not player.wreck_start and not player.wrecked:
            for draw_bomb in bombs:
                pygame.draw.rect(game_display, white, (draw_bomb[0]+55, draw_bomb[1]+70, 20, 20))
            for move_bomb in range(len(bombs)):
                bombs[move_bomb][1] += 20
            for del_bomb in bombs:
                if del_bomb[1] > 600:
                    bombs.remove(del_bomb)

        # rendering enemy bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_ufo.bullets:
                pygame.draw.rect(game_display, white, (draw_bullet[0], draw_bullet[1]+90, 40, 10))
                pygame.draw.rect(game_display, red, (draw_bullet[0]+30, draw_bullet[1]+90, 10, 10))
            for move_bullet in range(len(enemy_ufo.bullets)):
                enemy_ufo.bullets[move_bullet][0] -= 15
            for del_bullet in enemy_ufo.bullets:
                if del_bullet[0] <= -40:
                    enemy_ufo.bullets.remove(del_bullet)

        # rendering alien bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in alien.bullets:
                pygame.draw.rect(game_display, white, (draw_bullet[0]+40, draw_bullet[1]+60, 20, 20))
            for move_bullet in range(len(alien.bullets)):
                alien.bullets[move_bullet][0] -= 10
                alien.bullets[move_bullet][1] -= 10
            for del_bullet in alien.bullets:
                if del_bullet[1] < -40:
                    alien.bullets.remove(del_bullet)

        # draw randomly positioned asteroids, pop if they hit any bullet or bombs
        for pop_asteroid in bullets:
            if asteroid_x < pop_asteroid[0]+90 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+40 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_asteroid)
                asteroid_x = -200
                score += 50
            elif asteroid_x < pop_asteroid[0]+100 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+50 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_asteroid)
                asteroid_x = -200
                score += 50

        for pop_asteroid in bombs:
            if asteroid_x < pop_asteroid[0]+55 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+70 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_asteroid)
                asteroid_x = -200
                score += 50
            elif asteroid_x < pop_asteroid[0]+75 < asteroid_x+70 and asteroid_y < pop_asteroid[1]+90 < asteroid_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_asteroid)
                asteroid_x = -200
                score += 50

        # spawn spaceship randomly
        if score >= 450:
            spaceship_spawn_num = random.randint(0, 200)
            if spaceship_spawn_num == 50 and not spaceship_alive:
                warning = True
        if score >= 2500:
            spaceship_spawn_num = random.randint(0, 100)
            if spaceship_spawn_num == 50 and not spaceship_alive:
                warning = True
        if score >= 5000:
            spaceship_spawn_num = random.randint(0, 50)
            if spaceship_spawn_num == 50 and not spaceship_alive:
                warning = True

        # show warning before spaceship spawning
        if warning:
            if warning_once:
                pygame.mixer.Sound.play(alert)
                warning_once = False
            game_display.blit(warning_message, (750, spaceship_y-15))
            if warning_counter > 45:
                pygame.mixer.Sound.play(whoosh)
                spaceship_alive = True
                warning_counter = 0
                warning = False
                warning_once = True
            else:
                warning_counter += 1

        # spaceship movement
        if spaceship_alive:
            spaceship_x -= 30
        if spaceship_x < 0-100:
            spaceship_hit_player = False
            spaceship_alive = False
            spaceship_x = 800
            spaceship_y = random.randint(0, 400)

        # spawn enemy rocket randomly
        if 250 <= score < 2000:
            enemy_spawn_num = random.randint(1, 100)
            if not enemy_ufo_alive and enemy_spawn_num == 50:
                enemy_ufo_alive = True
                enemy_ufo.x = 800
        # difficulty increase
        if 2000 <= score < 4000:
            enemy_spawn_num = random.randint(1, 75)
            if not enemy_ufo_alive and enemy_spawn_num == 50:
                enemy_ufo_alive = True
                enemy_ufo.x = 800
        if score >= 4000:
            enemy_spawn_num = random.randint(1, 50)
            if not enemy_ufo_alive and enemy_spawn_num == 50:
                enemy_ufo_alive = True
                enemy_ufo.x = 800

        # spawn alien randomly
        if 700 <= score < 1500:
            alien_spawn_num = random.randint(1, 250)
            if score > 700 and alien_spawn_num == 100 and not alien_alive:
                alien.x = 800
                alien_alive = True
        if score >= 1500:
            alien_spawn_num = random.randint(1, 150)
            if score > 700 and alien_spawn_num == 100 and not alien_alive:
                alien.x = 800
                alien_alive = True

        if alien.x <= -110:
            alien_alive = False

        # enemy-player bullet collision detection
        for hit_enemy_ufo in bullets:
            if enemy_ufo.x < hit_enemy_ufo[0]+90 < enemy_ufo.x+100 \
               or enemy_ufo.x < hit_enemy_ufo[0]+100 < enemy_ufo.x+100:
                if enemy_ufo.y < hit_enemy_ufo[1]+15 < enemy_ufo.y+60 \
                   or enemy_ufo.y < hit_enemy_ufo[1]-10 < enemy_ufo.y+40:
                    if not enemy_ufo.x > 600:
                        pygame.mixer.Sound.play(explosion2)
                        score += 150
                        bullets.remove(hit_enemy_ufo)
                        enemy_ufo.x = -200
                        enemy_ufo_alive = False

        # spaceship-player bullet/bomb collision detection
        for hit_spaceship in bullets:
            if spaceship_x < hit_spaceship[0]+90 < spaceship_x+100 \
               or spaceship_x < hit_spaceship[0]+100 < spaceship_x+100:
                if spaceship_y < hit_spaceship[1]+40 < spaceship_y+80 \
                   or spaceship_y < hit_spaceship[1]+50 < spaceship_y+80:
                    if not spaceship_x > 700:
                        pygame.mixer.Sound.play(explosion2)
                        bullets.remove(hit_spaceship)
                        score += 200
                        spaceship_hit_player = False
                        spaceship_alive = False
                        spaceship_x = 800
                        spaceship_y = random.randint(0, 400)

        for hit_spaceship in bombs:
            if spaceship_x < hit_spaceship[0]+55 < spaceship_x+100 \
               or spaceship_x < hit_spaceship[0]+65 < spaceship_x+100:
                if spaceship_y < hit_spaceship[1]+70 < spaceship_y+80 \
                   or spaceship_y < hit_spaceship[1]+80 < spaceship_y+80:
                    if not spaceship_x > 700:
                        pygame.mixer.Sound.play(explosion2)
                        bombs.remove(hit_spaceship)
                        score += 200
                        spaceship_hit_player = False
                        spaceship_alive = False
                        spaceship_x = 800
                        spaceship_y = random.randint(0, 400)

        # alien-player bullet/bomb collision detection
        for hit_alien in bullets:
            if alien.x < hit_alien[0] < alien.x+180 or alien.x < hit_spaceship[0]+100 < alien.x+110:
                if alien.y < hit_alien[1]-30 < alien.y+300 or alien.y < hit_alien[1] < alien.y+250:
                    if not alien.x > 780:
                        pygame.mixer.Sound.play(explosion2)
                        bullets.remove(hit_alien)
                        score += 200
                        alien_alive = False
                        alien.x = -200

        for hit_alien in bombs:
            if alien.x < hit_alien[0]+55 < alien.x+110 or alien.x < hit_spaceship[0]+75 < alien.x+110:
                if alien.y < hit_alien[1]-30 < alien.y+300 or alien.y < hit_alien[1]-60 < alien.y+250:
                    if not alien.x > 780:
                        pygame.mixer.Sound.play(explosion2)
                        bombs.remove(hit_alien)
                        score += 200
                        alien_alive = False
                        alien.x = -200

        # player-asteroid collision detection
        if asteroid_x < player.x < asteroid_x+70 or asteroid_x < player.x+100 < asteroid_x+70:
            if asteroid_y < player.y < asteroid_y+80 or asteroid_y < player.y+80 < asteroid_y+80:
                pygame.mixer.Sound.play(explosion)
                player.damaged = True
                player.health -= 1
                asteroid_x = -200

        # player-extralife collision detection
        if extra_life_x < player.x < extra_life_x + 70 or extra_life_x < player.x + 100 < extra_life_x + 70:
            if extra_life_y < player.y < extra_life_y + 80 or extra_life_y < player.y + 80 < extra_life_y + 80:
                pygame.mixer.Sound.play(oneup)
                player.health += 1
                extra_life_x = -200

        # player-enemy rocket collision detection
        for hit_player in enemy_ufo.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    enemy_ufo.bullets.remove(hit_player)

        # player-alien bullet collision detection
        for hit_player in alien.bullets:
            if player.x < hit_player[0] < player.x+70 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                    if not alien.alien_hit_player:
                        player.damaged = True
                        player.health -= 1
                        alien.bullets.remove(hit_player)

        # player-alien collision detection
        if alien.x < player.x < alien.x+70 or alien.x < player.x+100 < alien.x+70:
            if alien.y < player.y < alien.y+80 or alien.y < player.y+80 < alien.y+80:
                if not alien.alien_hit_player:
                    pygame.mixer.Sound.play(explosion)
                    alien.x = -200
                    player.damaged = True
                    player.health -= 1
                    alien.alien_hit_player = True

        # player-spaceship collision detection
        if spaceship_x < player.x < spaceship_x+200 or spaceship_x < player.x+100 < spaceship_x+95:
            if spaceship_y < player.y < spaceship_y+65 or spaceship_y < player.y+95 < spaceship_y+100:
                if not spaceship_hit_player:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    spaceship_hit_player = True

        game_display.blit(sprites.asteroid, (asteroid_x, asteroid_y))
        if asteroid_x <= -200:
            asteroid_x = 800
            asteroid_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                asteroid_x -= 7

        game_display.blit(sprites.extra_life, (extra_life_x, extra_life_y))
        if extra_life_x <= -200 and score == 5000 or score == 15000:
            extra_life_x = 800
            extra_life_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                extra_life_x -= 7

        # draw score
        game_display.blit(message_to_screen("SCORE: {0}".format(score), font, 50, white), (10, 10))

        # draw high score
        if score < highscore_int:
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, white)
        else:
            highscore_file = open('highscore.dat', "w")
            highscore_file.write(str(score))
            highscore_file.close()
            highscore_file = open('highscore.dat', "r")
            highscore_int = int(highscore_file.read())
            highscore_file.close()
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, yellow)

        hi_score_message_rect = hi_score_message.get_rect()

        game_display.blit(hi_score_message, (800-hi_score_message_rect[2]-10, 10))

        # draw health
        if player.health >= 1:
            game_display.blit(sprites.icon, (0, 30))
            if player.health >= 2:
                game_display.blit(sprites.icon, (35+10, 30))
                if player.health >= 3:
                    game_display.blit(sprites.icon, (35+10+35+10, 30))
                    if player.health >= 4:
                        game_display.blit(sprites.icon, (35+10+35+10+45, 30))
                        if player.health >= 5:
                            game_display.blit(sprites.icon, (35+10+35+10+45+45, 30))

        # god-mode (for quicker testing)
        if godmode:
            score = 1000
            player.health = 3

        pygame.display.update()



main_menu()
game_loop()
pygame.quit()
quit()
