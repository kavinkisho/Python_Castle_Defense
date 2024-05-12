# import libraries
import pygame
import math
import random
from enemy import Enemy
from buttons import Buttons

# Initialize pygame
pygame.init()

# Define some game variables
wave = 1
wave_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.2
game_over = False
next_wave = False
enemies_alive = 0

ENEMY_TIMER = 1000

# last_enemy is used to record when did it last clone an enemy
# get_ticks() returns the current time stamp registered in pygame
last_enemy = pygame.time.get_ticks()

# Define the dimension of game screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# FPS Settings
# create an internal clock object
clock = pygame.time.Clock()
FPS = 60

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
bg = pygame.transform.scale(pygame.image.load("PygameAssets/bg/bg1.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
castle_img_100 = pygame.image.load("PygameAssets/castle/Asset 24.png")
castle_img_60 = pygame.image.load("PygameAssets/castle/Asset 25.png")
castle_img_30 = pygame.image.load("PygameAssets/castle/Asset 26.png")

bullet_img = pygame.image.load("PygameAssets/weapon/Bullet1.png")
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.5), int(b_h * 0.5)))

# Play background audio
pygame.mixer.music.load("PygameAssets/background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)

# Heads up display
font_HUD = pygame.font.Font("PygameAssets/font.TTF", 45)


# Define a custom function to display text on screen
def draw_text(text, font, color, x, y):
    # Render text using render() function in pygame's font module
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


animation_types = ['walk', 'attack', 'death']
enemy_types = ['1_KNIGHT', '2_KNIGHT', '3_KNIGHT']
master_animation_list = []  # 3D list

for eachEnemyType in enemy_types:
    animation_list = []
    for animationType in animation_types:
        # Load all enemy images using nested loops
        temp_list = []
        for eachImage in range(0, 10, 1):
            img = pygame.image.load(f"PygameAssets/enemies/{eachEnemyType}/{animationType}/{eachImage}.png")
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.1), int(e_h * 0.1)))
            temp_list.append(img)
            # By the end of this for loop, 10 images are loaded and saved in temp_list

        animation_list.append(temp_list)
        # By the end of this for loop, 30 images of an enemy type will be loaded

    master_animation_list.append(animation_list)

"""
temp_list = [0, 1, ..., 9.png] - 1D LIST
animation_list = [ [walk], [attack], [death] ] - 2D LIST
master_animation_list = [ [ [walk], [attack], [death] ], [ [walk], [attack], [death] ], [ [walk], [attack], [death] ] ] - 3D LIST
"""


# Object-Oriented Programming (OOP)
# To represent real-life objects
class Castle():
    # Constructor - it is used to create a castle instance/object/clone
    def __init__(self, image100, image60, image30, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        width = image100.get_width()
        height = image100.get_height()
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image60 = pygame.transform.scale(image60, (int(width * scale), int(height * scale)))
        self.image30 = pygame.transform.scale(image30, (int(width * scale), int(height * scale)))

        # Define hitbox for collision detection
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isFiring = False
        self.money = 1000
        self.exp = 0

    # Object method (Certain actions a castle clone can perform)
    # All castle clones can have access to this function
    def draw(self):
        # Check which costume to be loaded based on self.health
        if self.health > 600:
            self.image = self.image100
        elif 300 <= self.health <= 600:
            self.image = self.image60
        else:
            self.image = self.image30

        screen.blit(self.image, self.rect)

    def shoot(self):
        pos = pygame.mouse.get_pos()
        # print(pos)

        # Calculate vertical and horizontal distance
        # between laser's origin and pos
        x_dist = pos[0] - self.rect.center[0]
        y_dist = -(pos[1] - self.rect.center[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        red = 0
        green = random.randint(200, 255)
        blue = 0
        if pygame.mouse.get_pressed()[2]:
            pygame.draw.line(screen, (red, green, blue), (self.rect.center[0], self.rect.center[1]), pos,
                             width=random.randint(0, 15))

        # Check if LMB is clicked
        if pygame.mouse.get_pressed()[0]:
            # Create a bullet clone
            bullet = Bullet(bullet_img, self.rect.center[0], self.rect.center[1], self.angle)
            bullet_group.add(bullet)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health = self.health + 500
            self.money = self.money - 1000
            if self.health > self.max_health:
                self.health = self.max_health

    def armour(self):
        if self.money >= 500:
            self.max_health = self.max_health + 250
            self.money = self.money - 500


# Bullet Class - this class inherits properties from Pygame sprite class
class Bullet(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10  # Initial speed of a projectile clone
        self.gravity_included_speed = 0
        self.vel_x = 1  # Initial horizontal speed component
        self.vel_y = 0  # Initial vertical speed component

    def update(self):
        # Move bullet clone here
        self.vel_x = self.speed * math.cos(self.angle)
        self.vel_y = -(self.speed * math.sin(self.angle))

        # Changing x-coordinate by horizontal speed component
        self.rect.x = self.rect.x + self.vel_x

        # Changing y-coordinate by horizontal speed component
        self.rect.y = self.rect.y + self.vel_y + (self.vel_y + self.gravity_included_speed)

        # Object gains speed under the influence of gravity
        self.gravity_included_speed += 0.2


class Crosshair():
    def __init__(self, scale):
        image = pygame.image.load('PygameAssets/utility/crosshair.png')
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)


# Create a Crosshair clone
crosshair1 = Crosshair(1.0)

# Create the bullet_group (list)
bullet_group = pygame.sprite.Group()

castle1 = Castle(castle_img_100, castle_img_60, castle_img_30, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, 0.1)

# create an enemy group (list) to store all enemy clones
enemy_group = pygame.sprite.Group()

# Define button images
repair_img = pygame.image.load("PygameAssets/utility/repair.png")
armour_img = pygame.image.load("PygameAssets/utility/armour.png")

# Create two button clones
repair_button = Buttons(620, 80, repair_img, 0.2)
armour_button = Buttons(720, 80, armour_img, 0.8)

############### MAIN GAME LOOP ####################
run = True
while run:
    clock.tick(FPS)

    screen.blit(bg, (0, 0))

    if repair_button.draw(screen) == True:
        castle1.repair()

    if repair_button.draw(screen) == True:
        castle1.armour()

    armour_button.draw(screen)

    castle1.draw()
    castle1.shoot()

    crosshair1.draw()

    # Draw bullet clones
    bullet_group.update()
    bullet_group.draw(screen)

    draw_text("Money " + str(castle1.money), font_HUD, (0, 255, 0), 10, 10)
    draw_text("Exp " + str(castle1.exp), font_HUD, (0, 255, 0), 350, 10)
    draw_text("Wave " + str(wave), font_HUD, (0, 255, 0), 650, 10)
    draw_text(str(castle1.health) + '  ' + str(castle1.max_health), font_HUD, (0, 255, 0), 10, 50)

    if castle1.health > 0:
        # draw_text("Health " + str(castle1.health), font_HUD, (0, 255, 0), 500, 400)

        # Health bar bg
        health_rect_max = pygame.Rect(650, 450, (castle1.max_health / 7), 5)
        pygame.draw.rect(screen, (255, 255, 255), health_rect_max)

        if castle1.health > 600:
            color = (0, 255, 0)
        elif 300 <= castle1.health <= 600:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        # Green overlay
        health_rect = pygame.Rect(650, 450, (castle1.health / 7), 5)
        pygame.draw.rect(screen, color, health_rect)
    else:
        draw_text("YOU LOSE", font_HUD, (255, 0, 0), 500, 400)
        run = False

    # create enemy clone
    # Check if the target difficulty has been reached
    if wave_difficulty < target_difficulty:
        # Check if enough time has passed since we last cloned an enemy
        if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
            e_type = random.randint(0, 2)
            e_speed = random.randint(1, 3)
            enemy = Enemy(e_speed, 100, master_animation_list[e_type], 50, SCREEN_HEIGHT - 50, e_type)

            # Update last_enemy variable (to record the time at which an enemy clone is created)
            last_enemy = pygame.time.get_ticks()

            enemy_group.add(enemy)

            # Increase wave difficulty
            wave_difficulty += 100

    # Check if all enemies of a wave have been spawned
    if wave_difficulty >= target_difficulty:
        # Check how many enemy clones are still alive
        enemies_alive = 0
        for e in enemy_group:
            if e.alive == True:
                enemies_alive += 1

        # if there are none alive then wave is cleared
        if enemies_alive == 0 and next_wave == False:
            next_wave = True
            # Register the time stamp as soon as the wave is cleared
            level_reset_time = pygame.time.get_ticks()

    # Move on to the next wave
    if next_wave == True:
        draw_text('Wave' + str(wave) + 'cleared', font_HUD, (0, 255, 0), 200, 300)
        # Check if sufficient time has passed since we cleared a wave
        if pygame.time.get_ticks() - level_reset_time > 5000:
            next_wave = False
            wave = wave + 1

            # Reset wave parameters
            last_enemy = pygame.time.get_ticks()
            wave_difficulty = 0
            target_difficulty *= DIFFICULTY_MULTIPLIER
            enemy_group.empty()

    enemy_group.update(screen, castle1, bullet_group)
    # print(len(enemy_group))

    # Event handler to quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display window in every frame
    pygame.display.update()

pygame.quit()
