import pygame, sys
import random

pygame.init()

#akna suurused ja teised seaded
width = 600
height = 400
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
player_color = red
player_size = 20
player_speed = 5

#algpositsioon
player_pos = [width // 2, height // 2]

#takistused
num_obstacles = 14
obstacle_size = 30
obstacles = []

for _ in range(num_obstacles):
    obs_x = random.randint(0, width - obstacle_size)
    obs_y = random.randint(0, height - obstacle_size)
    obstacles.append([obs_x, obs_y])

#mäng algab
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Takistuse Mäng")  # Muudetud akna nimi
clock = pygame.time.Clock()

def reset_game():
    global player_pos, obstacles, game_over, player_color
    player_pos = [width // 2, height // 2]
    obstacles = []
    for _ in range(num_obstacles):
        obs_x = random.randint(0, width - obstacle_size)
        obs_y = random.randint(0, height - obstacle_size)
        obstacles.append([obs_x, obs_y])
    player_color = red
    game_over = False

game_over = False
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  #kui vajutad enterit hakkab mäng uuesti
            reset_game()

    else:
        #siin liigun nooltega paremale, vasakule, alla, ülesse
        keys = pygame.key.get_pressed()
        player_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
        player_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

        #teeb nii et ma ei lähe ekraanist välja
        player_pos[0] = max(0, min(width - player_size, player_pos[0]))
        player_pos[1] = max(0, min(height - player_size, player_pos[1]))

        #kontrollib kas ruut puutub takistust
        for obs in obstacles:
            if (player_pos[0] < obs[0] + obstacle_size and
                    player_pos[0] + player_size > obs[0] and
                    player_pos[1] < obs[1] + obstacle_size and
                    player_pos[1] + player_size > obs[1]):
                player_color = red
                game_over = True

    #uuendab ekraani
    screen.fill(white)
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    #joonistab takistust
    for obs in obstacles:
        pygame.draw.rect(screen, black, (obs[0], obs[1], obstacle_size, obstacle_size))

    #kui mäng saab läbi tuleb ekraanile teade et "Mäng läbi!" Vajuta Enterit"
    if game_over:
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render("Mäng läbi! Vajuta Enterit", True, (0, 0, 0))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 30))

    pygame.display.update()

pygame.quit()