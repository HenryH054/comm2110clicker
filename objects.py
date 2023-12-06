import pygame
from random import randint


class Spout:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.polygon = ((x, y+height), (x+width, y+height),
                        (x + width - width*.2, y+height*(3/2)), (x + width*.2, y+height*(3/2)))
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.value = 0
        self.click_power = 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.polygon(screen, self.color, self.polygon)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def perform_action(self):
        self.value += self.click_power

    def spawn_brick(self) -> "Brick":
        if self.value > 0:
            brick = Brick(self.value, self.polygon[3])
            self.value = 0
            return brick
        return None


class Brick():
    def __init__(self, value, xy) -> None:
        self.value = value
        self.rect = pygame.Rect(xy[0], xy[1], 40, 20)
        self.font = pygame.font.Font(None, 25)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(str(self.value), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def move(self, distance):
        if self.rect.bottom >= 500:
            self.rect.left += distance
            self.rect.right += distance
        else:
            self.rect.top += distance
            self.rect.bottom += distance

        return self.rect.left
