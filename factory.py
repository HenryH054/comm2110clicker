import pygame
from objects import Spout, Brick, Employee

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
frame = 0
font = pygame.font.Font(None, 40)

spout = Spout(100, 100, 300, 200, (200, 200, 0), 'Click Me')
brick: [Brick] = []
belt = pygame.Rect(130, 500, screen.get_width(), 100)
money = 0
score_board = pygame.Rect(screen.get_width()-300, 35, 0, 0)
employees: [Employee] = []

for i in range(3):
    employees.append(Employee((i*200)+650, 475))

# have "people" impact the value based on trait that has a multiplier
# add upgrades that allow more powerful clicks and passive cube generation
# add upgrades to people that allow altering of traits

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if spout.is_clicked(event.pos):
                spout.perform_action()
            for i in employees:
                if i.is_clicked(event.pos):
                    i.perform_action()
    if frame == 60:
        brick.append(spout.spawn_brick())
        brick = [x for x in brick if x is not None]
        frame = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((50, 50, 50))
    spout.draw(screen)

    if brick:
        for i in brick:
            i.draw(screen)
            if i.move(100*dt) >= screen.get_width():
                money += i.value
                brick.remove(i)

    for i in employees:
        i.draw(screen)

    pygame.draw.rect(screen, "black", belt)

    text_surface = font.render(f"${money}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=score_board.center)
    screen.blit(text_surface, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    frame += 1

pygame.quit()
