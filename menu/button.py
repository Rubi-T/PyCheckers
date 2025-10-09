class Button:
    def __init__(self, image, hover_image, pos):
        self.image = image
        self.hover_image = hover_image
        self.current_image = self.image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.current_image, self.rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeImageOnHover(self, position):
        if self.rect.collidepoint(position):
            self.current_image = self.hover_image
        else:
            self.current_image = self.image