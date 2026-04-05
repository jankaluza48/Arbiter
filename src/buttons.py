class Button():
    def __init__(self, image, pos, text_input, font, base_color, hover_color, hover_image, clicked_color, clicked_image, clicked_color_hover, clicked_image_hover):
        self.old_image = image
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font 
        self.base_color, self.hover_color = base_color, hover_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.hover_image = hover_image
        self.clicked_color, self.clicked_image = clicked_color, clicked_image
        self.clicked_color_hover, self.clicked_image_hover = clicked_color_hover, clicked_image_hover
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.click_status = False

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if self.click_status:
                self.text = self.font.render(self.text_input, True, self.clicked_color_hover)
                if self.clicked_image_hover is not None:
                    self.image = self.clicked_image_hover
            else:
                self.text = self.font.render(self.text_input, True, self.hover_color)
                if self.hover_image is not None:
                    self.image = self.hover_image
        else: 
            if self.click_status:
                self.text = self.font.render(self.text_input, True, self.clicked_color)  
                if self.clicked_image is not None:
                    self.image = self.clicked_image
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)  
                if self.old_image is not None:
                    self.image = self.old_image
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def click_button(self):
        if self.click_status:
            self.text = self.font.render(self.text_input, True, self.clicked_color)
            if self.old_image is not None:
                self.image = self.old_image
            
            self.click_status = False
        else:
            self.text = self.font.render(self.text_input, True, self.clicked_color)
            if self.clicked_image is not None:
                self.image = self.clicked_image
            self.click_status = True
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def reset_click_button(self):
        if self.click_status:
            self.text = self.font.render(self.text_input, True, self.clicked_color)
            if self.old_image is not None:
                self.image = self.old_image
            
            self.click_status = False
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
class Par():
    def __init__(self, image, color, pos, hover_image, hover_color, w, h, text, font, text_color):
        self.old_image = image
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.hover_image = hover_image
        self.color, self.hover_color = color, hover_color
        self.w = w  
        self.h = h
        self.text = font.render(text, True, text_color)
        if self.image is None:
            self.image = self.text

    def update(self, screen):       
        if self.image is not None:
            screen.blit(self.image, (self.x_pos, self.y_pos))
    def check_input(self, position):
        if position[0] in range(self.x_pos, self.x_pos + self.w) and position[1] in range(self.y_pos, self.y_pos + self.h):
            return True
        return False
    def change_color(self, position):
        if position[0] in range(self.x_pos, self.x_pos + self.w) and position[1] in range(self.y_pos, self.y_pos + self.h):
            if self.hover_image is not None:
                self.image = self.hover_image
        else: 
            if self.old_image is not None:
                self.image = self.old_image

            