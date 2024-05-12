import pygame

# Enemy class inherits properties from pygame sprite class
class Enemy(pygame.sprite.Sprite):
    # Constructor (it is used to create a clone/object of this class)
    def __init__(self, speed, health, animation_list, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.alive = True
        self.action = 0 # walk: 0, attack: 1, death: 2
        self.frame_index = 0

        # The variable that records when we last switched costume
        self.update_time = 0

        # Select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 30, 50)
        self.rect.center = (x, y)

        self.death_cooldown_counter = 0

        self.type = type
        self.last_attack = 0


    # Object methods
    def update(self, surface, target, bullet_group):

        if self.alive:
            # Check for collision with bullet clones
            # Set the third attribute to True to delete bullet clone when collision happens
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.health = self.health - 50

            # Move enemy clones
            if self.action == 0:
                self.rect.x = self.rect.x + self.speed # Change x by 1

            # To attack and deal damage to the castle
            if self.action == 1:
                # Check if enough time has passed since a clone last launched an attack
                if pygame.time.get_ticks() - self.last_attack > 1000:
                    target.health = target.health - 25

                    if target.health <= 0:
                        target.health = 0

                    # Update self .last_attack
                    # Set it to the present time stamp
                    self.last_attack = pygame.time.get_ticks()


            # Check if enemy has reached the castle
            if self.rect.right > target.rect.left:
                #print("i've reached the Castle")
                self.update_action(1)

            # Check is enemy's health has dropped to 0, switch action to death
            if self.health <= 0:
                # target = castle1
                target.money = target.money + 100
                target.exp = target.exp + 1
                self.update_action(2)
                self.alive = False

        # Update animation
        self.update_animation()

        # Draw the enemy clone and it hitbox
        # pygame.draw.rect(surface, (0,255,0), self.rect, 5)
        surface.blit(self.image, (self.rect.x - 80, self.rect.y - 20))


    def update_animation(self):

        # Define animation cooldown
        ANIIMATION_COOLDOWN = 30

        DEATH_COOLDOWN = 200
        self.death_cooldown_counter = self.death_cooldown_counter + 1

        # Update costume as per frame_index (costume number)
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since we last switched costume
        # change self.frame_index by 1
        if pygame.time.get_ticks() - self.update_time > ANIIMATION_COOLDOWN:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()

        # If the animation has run out then reset it
        if self.frame_index >= 9:
            if self.action == 2:
                self.frame_index = 9

                # Check if enough time has passed before we delete the death body
                if self.death_cooldown_counter >= DEATH_COOLDOWN:
                    self.kill()
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        # Check if the new action is better than the current action
        if new_action != self.action:
            self.action = new_action

            # To ensure it starts off the first frame whatever we switch action
            self.frame_index = 0

            # Update time stamp
            self.update_time = pygame.time.get_ticks()



# animation_list = [ [walk], [attack], [death] ] - 2D LIST