import sys
import random
import pygame
from pygame.locals import *

window_width = 600
window_height = 500

window = pygame.display.set_mode((window_width, window_height))

# Độ cao khu vực bay
elevation = window_height * 0.8

# Khung hình/giây
fps = 32

# Ảnh
game_images = {}
pipe_image = "images/pipe.png"
bg_image = "images/background.jpg"
bird_image = "images/bird.png"
sea_image = "images/base.jfif"


# Tạo ống
def Pipes():
    # Khoảng trống
    offset = window_height / 3

    pipeHeight = game_images["pipe"][0].get_height()

    # Độ dài của ống dưới
    y2 = offset + random.randrange(
        0, int(window_height - game_images["sea"].get_height() - 1.2 * offset)
    )
    pipeX = window_width + 10

    # Độ dài ống trên
    y1 = pipeHeight - y2 + offset

    pipe = [{"x": pipeX, "y": -y1}, {"x": pipeX, "y": y2}]
    return pipe


# Thua
def gameOver(horizontal, vertical, up_pipes, down_pipes):
    
    if vertical > elevation - 25 or vertical < 0:
        return True

    # Chạm ống trên
    for pipe in up_pipes:
        pipeHeight = game_images["pipe"][0].get_height()
        if (vertical < pipeHeight + pipe["y"]) and (
            abs(horizontal - pipe["x"]) < game_images["pipe"][0].get_width()
        ):
            return True

    # Chạm ống dưới
    for pipe in down_pipes:
        if (vertical + game_images["bird"].get_height() > pipe["y"]) and (
            abs(horizontal - pipe["x"]) < game_images["pipe"][0].get_width()
        ):
            return True

    return False


def playGame():
    score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_height / 2)
    ground = 0
    myHeight = 100

    first_pipe = Pipes()
    second_pipe = Pipes()

    down_pipes = [
        {"x": window_width + 300 - myHeight, "y": first_pipe[1]["y"]},
        {
            "x": window_width + 300 - myHeight + (window_width / 2),
            "y": second_pipe[1]["y"],
        },
    ]

    up_pipes = [
        {"x": window_width + 300 - myHeight, "y": first_pipe[0]["y"]},
        {
            "x": window_width + 300 - myHeight + (window_width / 2),
            "y": second_pipe[0]["y"],
        },
    ]

    # Vận tốc x của ống
    pipe_Vx = -4

    # Vận tốc y của chim
    bird_Vy = -9
    bird_Vy_max = 10

    # Gia tốc của chim
    birdAcceleration = 1

    bird_flap_V = -8
    birdFlap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (
                event.key == K_SPACE or event.key == K_ESCAPE
            ):
                if vertical > 0:
                    bird_Vy = bird_flap_V
                    birdFlap = True
        over = gameOver(horizontal, vertical, up_pipes, down_pipes)
        if over:
            return

        birdPosition = horizontal + game_images["bird"].get_width() / 2
        for pipe in up_pipes:
            pipePosition = pipe["x"] + game_images["pipe"][0].get_width() / 2
            if pipePosition <= birdPosition < pipePosition + 4:
                score += 1

        if bird_Vy < bird_Vy_max and not birdFlap:
            bird_Vy += birdAcceleration

        if birdFlap:
            birdFlap = False
        birdHeight = game_images["bird"].get_height()
        vertical += min(bird_Vy, elevation - vertical - birdHeight)

        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe["x"] += pipe_Vx
            lowerPipe["x"] += pipe_Vx

        if 0 < up_pipes[0]["x"] < 5:
            newPipe = Pipes()
            up_pipes.append(newPipe[0])
            down_pipes.append(newPipe[1])

        if up_pipes[0]["x"] < -game_images["pipe"][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        window.blit(game_images["background"], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            window.blit(game_images["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))

        window.blit(game_images["sea"], (ground, elevation))
        window.blit(game_images["bird"], (horizontal, vertical))

        numbers = [int(x) for x in list(str(score))]
        width = 0

        for num in numbers:
            width += game_images["score"][num].get_width()
        offsetX = (window_width - width) / 1.1

        for num in numbers:
            window.blit(game_images["score"][num], (offsetX, window_width * 0.02))
            offsetX += game_images["score"][num].get_width()

        pygame.display.update()
        time.tick(fps)


if __name__ == "__main__":
    pygame.init()
    time = pygame.time.Clock()
    pygame.display.set_caption("Flappy bird")
    pygame.mixer.music.load("sounds/flappy_bg_music.mp3")
    pygame.mixer.music.play(-1, 0)

    game_images["score"] = (
        pygame.image.load("images/0.png").convert_alpha(),
        pygame.image.load("images/1.png").convert_alpha(),
        pygame.image.load("images/2.png").convert_alpha(),
        pygame.image.load("images/3.png").convert_alpha(),
        pygame.image.load("images/4.png").convert_alpha(),
        pygame.image.load("images/5.png").convert_alpha(),
        pygame.image.load("images/6.png").convert_alpha(),
        pygame.image.load("images/7.png").convert_alpha(),
        pygame.image.load("images/8.png").convert_alpha(),
        pygame.image.load("images/9.png").convert_alpha(),
    )
    game_images["bird"] = pygame.image.load(bird_image).convert_alpha()
    game_images["sea"] = pygame.image.load(sea_image).convert_alpha()
    game_images["background"] = pygame.image.load(bg_image).convert_alpha()
    game_images["pipe"] = (
        pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
        pygame.image.load(pipe_image).convert_alpha(),
    )

    print("WELCOME TO FLAPPY BIRD")
    print("Press space or enter to start")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images["bird"].get_height()) / 2)

        ground = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP
                ):
                    playGame()

                else:
                    window.blit(game_images["background"], (0, 0))
                    window.blit(game_images["bird"], (horizontal, vertical))
                    window.blit(game_images["sea"], (ground, elevation))
                    font = pygame.font.SysFont("arial", 40)
                    line = font.render("To play press Enter or Space", True, (0, 0, 0))
                    window.blit(line, (window_width / 6, window_height / 3))

                    pygame.display.update()
                    time.tick(fps)
