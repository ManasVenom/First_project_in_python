
import pygame
import pygame_gui
import random

pygame.init()

height = 600
width = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Project")

manager = pygame_gui.UIManager((width, height))

play_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(300, 250, 200, 100),
    text="PLAY",
    manager=manager
)

retry_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(300, 400, 200, 70),
    text="RETRY",
    manager=manager
)

retry_button.hide()

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 35)
small_font = pygame.font.SysFont("Arial", 25)

background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (width, height))

apple = pygame.image.load("assets/apple.png")
apple = pygame.transform.scale(apple, (30, 30))

radius = 15
speed = 300

score = 0
max_score = 0

game_running = True
menu_running = True


def generate_apple(x, y):
    while True:
        apple_x = random.randint(30, width - 30)
        apple_y = random.randint(30, height - 30)

        distance = (apple_x - x) ** 2 + (apple_y - y) ** 2

        if distance > (radius + 25) ** 2:
            return apple_x, apple_y


while menu_running:

    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == play_button:
                menu_running = False

        elif event.type == pygame.QUIT:
            menu_running = False
            game_running = False

    manager.update(time_delta)

    screen.blit(background, (0, 0))
    manager.draw_ui(screen)

    pygame.display.flip()


play_button.hide()


while game_running:

    x = width // 2
    y = height // 2

    dx = 0
    dy = 0

    score = 0

    apple_x, apple_y = generate_apple(x, y)

    round_running = True

    while round_running and game_running:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                round_running = False
                game_running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dx = -1
                    dy = 0

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dx = 1
                    dy = 0

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dx = 0
                    dy = -1

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dx = 0
                    dy = 1

        if not game_running:
            break

        new_x = x + dx * speed * time_delta
        new_y = y + dy * speed * time_delta

        if (new_x - radius < 10 or
            new_x + radius > width - 10 or
            new_y - radius < 10 or
            new_y + radius > height - 10):

            round_running = False

        else:
            x = new_x
            y = new_y

        distance = (apple_x - x) ** 2 + (apple_y - y) ** 2

        if distance <= (radius + 15) ** 2:

            score += 1

            apple_x, apple_y = generate_apple(x, y)

        screen.blit(background, (0, 0))

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(10, 10, width - 20, height - 20),
            3
        )

        screen.blit(
            apple,
            (apple_x - 15, apple_y - 15)
        )

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (int(x), int(y)),
            radius
        )

        score_text = font.render(
            "Score: " + str(score),
            True,
            (255, 255, 255)
        )

        screen.blit(score_text, (25, 20))

        pygame.display.flip()

    max_score = max(max_score, score)

    if not game_running:
        break

    retry_button.show()

    game_over_running = True

    while game_over_running and game_running:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == retry_button:
                    game_over_running = False

            elif event.type == pygame.QUIT:
                game_over_running = False
                game_running = False

        manager.update(time_delta)

        screen.blit(background, (0, 0))

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        screen.blit(overlay, (0, 0))

        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        current_score_text = small_font.render(
            "Current Score: " + str(score),
            True,
            (255, 255, 255)
        )

        max_score_text = small_font.render(
            "Maximum Score: " + str(max_score),
            True,
            (255, 255, 255)
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(center=(width // 2, 200))
        )

        screen.blit(
            current_score_text,
            current_score_text.get_rect(center=(width // 2, 280))
        )

        screen.blit(
            max_score_text,
            max_score_text.get_rect(center=(width // 2, 330))
        )

        manager.draw_ui(screen)

        pygame.display.flip()

    retry_button.hide()


pygame.quit()
