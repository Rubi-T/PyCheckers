import pygame

class Button:
    def __init__(self, text, pos, font, text_color=(0,0,0), bg_color=(255,255,255),
                 hover_bg=(200,200,200), padding=(20,10)):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg = hover_bg
        self.padding = padding
        self.pos = pos  # center position (x,y)
        self._render_text()
        self.rect = self.surface.get_rect(center=self.pos)
        self.hover = False

    def _render_text(self):
        self.text_surf = self.font.render(self.text, True, self.text_color)
        w = self.text_surf.get_width() + self.padding[0]*2
        h = self.text_surf.get_height() + self.padding[1]*2
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        # draw background in update() so hover can change it

    def changeImageOnHover(self, mouse_pos):
        # kept for compatibility with your existing code
        self.hover = self.rect.collidepoint(mouse_pos)

    def update(self, window):
        bg = self.hover_bg if getattr(self, "hover", False) else self.bg_color
        # rounded rect background
        pygame.draw.rect(window, bg, self.rect, border_radius=8)
        # thin border
        pygame.draw.rect(window, (0,0,0), self.rect, width=1, border_radius=8)
        # blit text centered
        text_pos = (self.rect.left + self.padding[0], self.rect.top + self.padding[1])
        window.blit(self.text_surf, text_pos)

    def checkForInput(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
