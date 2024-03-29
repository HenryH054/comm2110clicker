import pygame
from objects import Spout, Brick, Employee, Upgrade

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
frame = 0
font = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 20)


spout = Spout(100, 100, 300, 200, (200, 200, 0), 'Click Me')
brick: [Brick] = []
belt = pygame.Rect(130, 500, screen.get_width(), 100)
money = 0
score_board = pygame.Rect(screen.get_width()-300, 35, 0, 0)
employee_info = pygame.Rect(screen.get_width()-300, 60, 0, 0)
employees: [Employee] = []
ei1 = None
ei2 = None
ei3 = None
ei4 = None
upgrade_click = Upgrade(130, 625, 200, 75, "blue", "Click Power")

for i in range(3):
    employees.append(Employee((i*200)+650, 475))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if upgrade_click.is_clicked(event.pos):
                money = upgrade_click.perform_action(spout, money)
            if spout.is_clicked(event.pos):
                spout.perform_action()
            for i in employees:
                if i.is_clicked(event.pos):
                    ei1, ei2, ei3, ei4 = i.perform_action(
                        font2, screen, employee_info)
    if frame % 60 == 0:
        brick.append(spout.spawn_brick())
        brick = [x for x in brick if x is not None]

    if frame % 30 == 0:
        for i in brick:
            i.upgrade(employees)

    if frame % 120 == 0:
        Employee.update_employees(employees)

    # fill the screen with a color to wipe away anything from last frame

    spout.draw(screen)

    for i in employees:
        i.draw(screen)

    if brick:
        for i in brick:
            i.draw(screen)
            if i.move(100*dt) >= screen.get_width():
                money += i.value
                brick.remove(i)

    pygame.draw.rect(screen, "black", belt)

    upgrade_click.draw(screen)

    text_surface = font.render(f"${money}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=score_board.center)
    screen.blit(text_surface, text_rect)
    if ei1 is not None:
        screen.blit(ei1, ei2)
        screen.blit(ei3, ei4)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    frame += 1

pygame.quit()
