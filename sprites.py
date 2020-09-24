import pygame

rocket_1 = pygame.image.load('data/sprites/rocket.png')
rocket_2 = pygame.image.load('data/sprites/rocket2.png')
rocket_crash_1 = pygame.image.load('data/sprites/rocketcrash1.png')
rocket_crash_2 = pygame.image.load('data/sprites/rocketcrash2.png')
rocket_crash_3 = pygame.image.load('data/sprites/rocketcrash3.png')
rocket_crash_4 = pygame.image.load('data/sprites/rocketcrash4.png')
rocket_damaged_1 = pygame.image.load('data/sprites/rocketdamage.png')
rocket_damaged_2 = pygame.image.load('data/sprites/rocketdamage2.png')

enemy_ufo_1 = pygame.image.load('data/sprites/enemy_ufo.png')
enemy_ufo_2 = pygame.image.load('data/sprites/enemy_ufo2.png')

alien = pygame.image.load('data/sprites/alien.png')

extra_life = pygame.image.load('data/sprites/extralife.png')

rocket_list = [rocket_1, rocket_2]
damaged_rocket_list = [rocket_damaged_1, rocket_damaged_2]
enemy_ufo_list = [enemy_ufo_1, enemy_ufo_2]

asteroid = pygame.image.load('data/sprites/asteroid.png')

spaceship = pygame.image.load('data/sprites/purplespaceship.png')

icon = pygame.image.load('data/sprites/icon.png')
background = pygame.image.load('data/sprites/background.png')
cloud = pygame.image.load('data/sprites/cloud.png')

all_sprites = [rocket_1, rocket_2, rocket_damaged_1, rocket_damaged_2, enemy_ufo_1,
               enemy_ufo_2, rocket_crash_1, rocket_crash_2, rocket_crash_3, rocket_crash_4,
               alien, asteroid, spaceship, icon, extra_life, background, cloud]
