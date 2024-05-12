import pygame

# Define Button class
class Buttons():
    # Create a constructor that has 4 parameters
    # x, y, image, scale
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    # Draw a button on the screen
    def draw(self, screen):

        action = False

        # Read mouse position
        pos = pygame.mouse.get_pos()

        # Check if mouse cursor is hovering a button
        if self.rect.collidepoint(pos):
            # if the LMB is pressed
            # and the button is not already being pressed
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True

        # To reset the button when the LMB is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Return the status of a button
        return action
