import pygame, sys, math, random

pygame.init()

pygame.display.set_caption("Python Invader")                  # Window
pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((800, 600))                   # Screen

clock = pygame.time.Clock()                 # Clock
FPS = 30

background_pos = [pygame.math.Vector2(0, 0), pygame.math.Vector2(0, -600)]             # Background
bg_file = [["background\\back", "1", ".png"], ["background\\back", "2", ".png"]]

player_file = ["icon\\player", "1", ".png"]                 # Player
player_img = pygame.image.load("".join(player_file))
player_pos = pygame.math.Vector2(300, 300)
player_size = [[33, 24], [0, 0], [0, 0], [0, 0], [0, 0]]
player = {"speed":30, "power":1, "timer":30, "level":1, "score":0}
player_shoot_count = []

enemy_file = ["icon\\alien", "1", "1", ".png"]          # Enemy
enemy = {"speed":50, "timer": 50, "limit": 5}
enemy_size = [[33, 33], [30, 33], [33, 33], [30, 33], [27, 33], [30, 33], [33, 33], [30, 33]]
enemy_pos = []

font = {"32":pygame.font.Font("font.ttf", 32), "16":pygame.font.Font("font.ttf", 16)}             # Fonts
score = 0

def col(score, enemy_pos, player_shoot_count):

    if len(player_shoot_count) > 0:
        for n in reversed(player_shoot_count):
            for k in reversed(enemy_pos):
                distance = math.sqrt(math.pow(n[0] - (k[0] + int(enemy_size[k[3]-1][0]/2)), 2) + math.pow(n[1] - (k[1] + int(enemy_size[k[3]-1][1]/2)), 2))
                if distance < int(enemy_size[k[3]-1][1]/2):
                    enemy_pos.pop(enemy_pos.index(k))
                    player_shoot_count.pop(player_shoot_count.index(n))
                    player["score"] += 1


def player_def(player_img, player_pos, player_lvl, player_size):

    player_pos.x = pygame.mouse.get_pos()[0]
    player_pos.y = pygame.mouse.get_pos()[1]

    select = player_lvl - 1
    x_distance = 795 - player_size[select][0]
    y_distance = 590 - player_size[select][1]

    if player_pos.x <= 5:
        player_pos.x = 5
    elif player_pos.x >= x_distance:
        player_pos.x = x_distance
    if player_pos.y <= 15:
        player_pos.y = 15
    elif player_pos.y >= y_distance:
        player_pos.y = y_distance

    screen.blit(player_img, player_pos)

def player_bullet(player_pos, player_size, player_shoot_count, player):

    select = player["level"] - 1

    player["timer"] = player["timer"] + 1 if player["timer"] < player["speed"] else player["speed"]
    if pygame.mouse.get_pressed()[0]:
        if player["timer"] >= player["speed"]:
            player_shoot_count.append([player_pos.x + int(player_size[select][0] / 2) + 1, player_pos.y])
            player["timer"] = 0

    for n in range(len(player_shoot_count) - 1, -1, -1):
        if player_shoot_count[n][1] <= -5:
            player_shoot_count.pop(n)
            continue
        pygame.draw.circle(screen, (255, 100, 0), (int(player_shoot_count[n][0]), int(player_shoot_count[n][1])), 4)
        player_shoot_count[n][1] -= 15

def enemy_bullet():
    pass

def enemy_def(enemy_file, enemy_pos, enemy):

    enemy["timer"] = enemy["timer"] + 1 if enemy["timer"] < enemy["speed"] else enemy["speed"]

    if len(enemy_pos) < enemy["limit"]:
        if enemy["timer"] >= enemy["speed"]:
            enemy_pos.append([random.randint(5, 760), -33, random.randrange(-1, 2, 2), random.randint(1, 8)])
            enemy["timer"] = 0

    for n in reversed(enemy_pos):
        n[0] += n[2]
        n[1] += 1

        if n[0] <= 5:
            n[2] = 1
        elif n[0] >= 730:
            n[2] = -1
        if n[1] >= 633:
            enemy_pos.pop(enemy_pos.index(n))

        load = enemy_file
        load[1] = str(n[3])
        screen.blit(pygame.image.load("".join(load)), (n[0], n[1]))

def background(background_pos, bg_file):

    if background_pos[0].y >= 600:
        background_pos[0].y -= 1200
        bg_file[0][1] = str(random.randint(1, 5))
    if background_pos[1].y >= 600:
        background_pos[1].y -= 1200
        bg_file[1][1] = str(random.randint(1, 5))

    screen.blit(pygame.image.load("".join(bg_file[0])), background_pos[0])
    screen.blit(pygame.image.load("".join(bg_file[1])), background_pos[1])

    background_pos[0].y += 1
    background_pos[1].y += 1

def font_def(font, player):

    score = font["32"].render("Score: " + str(player["score"]), True, (255, 255, 255))
    power = font["16"].render("Power: " + str(player["power"]), True, (255, 255, 255))
    speed = font["16"].render("Attack speed: " + str(abs(player["speed"]-31)), True, (255, 255, 255))
    screen.blit(score, (10, 10))
    screen.blit(power, (10, 548))
    screen.blit(speed, (10, 574))

while True:

    clock.tick(FPS)         # FPS

    for event in pygame.event.get():            # Events
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill((0, 0, 0))                  # Background
    background(background_pos, bg_file)

    col(player, enemy_pos, player_shoot_count)

    player_bullet(player_pos, player_size, player_shoot_count, player)        # Player
    player_def(player_img, player_pos, player["level"], player_size)

    enemy_def(enemy_file, enemy_pos, enemy)

    font_def(font, player)

    pygame.display.flip()
