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


class Employee():
    # adolescent - attention seeking
    # bully - demeans and takes credit
    # mild annoyance - just annoying
    # independent self promoter - only does things if they get credit
    # pushy play-boy make someone do a useless tak
    # independent other - someone who is different
    # abrasive incompetent harrasser - all around terrible and tends to do no work
    # epic co-worker - buff everyone
    names = ["Eleanor", "Alexander", "Sophia", "Mason", "Olivia", "Liam", "Ava", "Jackson",
             "Isabella", "Lucas", "Mia", "Aiden", "Emma", "Carter", "Charlotte", "Logan", "Amelia",
             "Elijah", "Harper", "Caleb", "Aria", "Makayla", "Henry", "Abigail", "Owen", "Layla",
             "Wyatt", "Ella", "Gabriel", "Chloe", "Grace", "Zoey", "Nathan", "Lily", "Matthew",
             "Hudson", "Luna", "Avery", "David", "Elena", "Daniel", "Nora", "Julian", "Riley",
             "Isaac", "Scarlett", "Levi", "Peyton", "Leo", "Sofia"]

    debuffs = ["Adolescent", "Bully", "Mild Annoyance", "Independent Self Promoter", "Pushy Play-Boy",
               "Independent Other", "Abrasive Incompetent Harasser", "Epic Colleague"]
    # "on/off task" - generate things
    # display showing morale & task status
    # click for credit

    def __init__(self, x, y):
        self.name = Employee.names[randint(0, 49)]
        self.debuff_id = randint(0, 7)
        self.debuff = Employee.debuffs[self.debuff_id]
        self.status = True
        self.multiplier = randint(5, 50)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.center = (x,y)
        self.size = randint(60, 100)
        self.rect = pygame.Rect(x-self.size, y-self.size, self.size*2, self.size*2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.size)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def perform_action(self):
        print(f"You clicked {self.name} who is a {self.debuff}")

    def effect(self) -> (int, int):
        match self.debuff_id:
            case 0 | 2:
                #if adolescent or mild annoyance nerf multiplier by random integer
                return (0, randint(5,10) / 10)
            case 1 | 3 | 4 | 6:
                #if bully randomally or pushy play boy or abrasive harasser or independent set status to false
                return (1, randint(0,1))
            case 5:
                # if independent other nerf all employees by a little
                return (0, randint(8,10) / 10)
            case 7:
                # epic employee which buffs everyone cause it's a game
                return (2, randint(2,5))


    def update_employees(employees: ["Employee"]):
        for i in employees:
            effect, value = i.effect()
            length = len(employees)
            match effect:
                case 0:
                    person = employees[randint(0, length-1)]
                    person.multiplier = person.multiplier * value
                case 1:
                    person = employees[randint(0, length-1)]
                    if effect == 1:
                        person.status = True
                    else:
                        person.status = False
                case 2:
                    for i in employees:
                        i.multiplier = i.multiplier * value