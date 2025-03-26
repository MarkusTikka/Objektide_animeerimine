import pygame
import random

# Mängu akna suurus
WIDTH, HEIGHT = 640, 480

# Laadi pildid
bg_image = pygame.image.load("bg_rally.jpg")
red_car = pygame.image.load("f1_red.png")
blue_car = pygame.image.load("f1_blue.png")

# Auto suuruse kohandamine
car_width, car_height = 50, 100
red_car = pygame.transform.scale(red_car, (car_width, car_height))
blue_car = pygame.transform.scale(blue_car, (car_width, car_height))

# Pygame algväärtustused
pygame.init()

# Ekraan ja font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")
font = pygame.font.Font(None, 36)

def reset_game():
    global red_x, red_y, blue_cars, score, running
    red_x, red_y = WIDTH // 2 - car_width // 2, HEIGHT - car_height - 10
    blue_cars = []
    for i in range(3):
        x = random.choice([WIDTH//4 - car_width//2, WIDTH//2 - car_width//2, 3*WIDTH//4 - car_width//2])
        y = random.randint(-300, -50)
        blue_cars.append([x, y])
    score = 0

reset_game()
clock = pygame.time.Clock()

while True:
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Klahvivajutuste kontroll
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and red_x > WIDTH//4 - car_width//2:
        red_x -= 5
    if keys[pygame.K_d] and red_x < 3*WIDTH//4 - car_width//2:
        red_x += 5

    # Siniste autode liikumine ja kokkupõrke tuvastamine
    for car in blue_cars:
        car[1] += 5
        if car[1] > HEIGHT:
            car[1] = random.randint(-300, -50)
            car[0] = random.choice([WIDTH//4 - car_width//2, WIDTH//2 - car_width//2, 3*WIDTH//4 - car_width//2])
            score += 1
        screen.blit(blue_car, (car[0], car[1]))

        # Kokkupõrke kontroll
        if red_x < car[0] + car_width and red_x + car_width > car[0] and red_y < car[1] + car_height and red_y + car_height > car[1]:
            game_over_text = font.render("Mäng läbi! Vajuta ENTER, et uuesti alustada", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        reset_game()
                        waiting = False

    # Joonista punane auto
    screen.blit(red_car, (red_x, red_y))

    # Kuva skoor
    score_text = font.render("Skoor: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)
