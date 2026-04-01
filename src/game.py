import pygame
import json
from buttons import Button

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False

        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.reset_keys()

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.main_menu = Main_Menu(self)

    def game_loop(self):
        while self.playing:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.check_events()
            if self.ENTER:
                self.playing = False
            self.screen.fill((0,0,0))

            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     self.running, self.playing = False, False
            #     self.main_menu.run_display = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RETURN:
            #         self.START_KEY = True
            #     if event.key == pygame.K_BACKSPACE:
            #         self.BACK_KEY = True
            #     if event.key == pygame.K_UP:
            #         self.UP_KEY = True
            #     if event.key == pygame.K_DOWN:
            #         self.DOWN_KEY = True
            #     if event.key == pygame.K_ESCAPE:
            #         self.running, self.playing = False, False
            #         self.main_menu.run_display = False
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.main_menu.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    self.MOUSE_CLICK_L = True
                elif event.button == 3:
                    self.MOUSE_CLICK_R = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER = True
                if event.key == pygame.K_LEFT:
                    self.LEFT = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT = True
                if event.key == pygame.K_UP:
                    self.UP = True
                if event.key == pygame.K_DOWN:
                    self.DOWN = True
                if event.key == pygame.K_SPACE:
                    self.SPACE = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACKSPACE = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC = True

        
    def reset_keys(self):
        self.MOUSE_CLICK_L, self.MOUSE_CLICK_R = False, False
        self.LEFT, self.RIGHT, self.UP, self.DOWN = False, False, False, False
        self.ENTER, self.SPACE, self.BACKSPACE, self.ESC = False, False, False, False

class Part():
    def __init__(self, game): 
        self.game = game
        self.run_display = True
    
    def blit_screen(self):
        pygame.display.update()
        self.game.reset_keys()

class Main_Menu(Part):
    def __init__(self, game):
        Part.__init__(self, game)
        pygame.display.set_caption("Menu")

        self.menu_bg_og = pygame.image.load("../img/menu_bg.png")

        self.menu_text = get_font_michroma(400).render("ARBITER", True, "#660619")

        self.menu_button = pygame.image.load("../img/menu_button.png")
        self.menu_button_hover = pygame.image.load("../img/menu_button_hover.png")

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.width, self.height = self.game.screen.get_size()
            self.menu_bg = pygame.transform.smoothscale(self.menu_bg_og, (self.width, self.height))
            self.game.screen.blit(self.menu_bg, (0, 0))

            width, height = self.game.screen.get_size()
            self.menu_rect = self.menu_text.get_rect(center=(width // 2, height // 2))
            self.game.screen.blit(self.menu_text, self.menu_rect)

            self.PLAY_BUTTON = Button(image=self.menu_button, pos=(width // 2, (height // 2) - 150), text_input = "HRÁT", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover)
            self.OPTIONS_BUTTON = Button(image=self.menu_button, pos=(width // 2, height // 2), text_input = "NASTAVENÍ", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover)
            self.QUIT_BUTTON = Button(image=self.menu_button, pos=(width // 2, (height // 2) + 150), text_input = "OPUSTIT", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover)

            for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.change_color(self.game.MENU_MOUSE_POS)
                button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    
    def check_input(self):
        if self.game.MOUSE_CLICK_L:
            if self.PLAY_BUTTON.check_input(self.game.MENU_MOUSE_POS):
                print("Play clicked")
                self.run_display = False
                pygame.display.set_caption("Game")
                pregame = PreGame(self.game)
                pregame.display_play()
                
            if self.OPTIONS_BUTTON.check_input(self.game.MENU_MOUSE_POS):
                print("Options clicked")
                pygame.display.set_caption("Options")

            if self.QUIT_BUTTON.check_input(self.game.MENU_MOUSE_POS):
                self.game.running = False
                self.run_display = False

        if self.game.ESC:
            self.game.running = False
            self.run_display = False


def get_font_michroma(size):
    return pygame.font.SysFont('Michroma', size)


class PreGame(Part):
    def __init__(self, game):
        Part.__init__(self, game)

        self.game.screen.fill((0,0,0))

        self.speed_typing = 6
        self.counter = 0
        self.active_message = 0

        with open('../txt/pregame.txt', encoding='utf-8') as text:
            self.messages = json.load(text)

        self.message = self.messages[self.active_message]

        self.game.reset_keys()

    def display_play(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)

        while self.run_display:
            self.game.screen.fill((0,0,0))

            if self.counter < self.speed_typing * len(self.message):
                self.counter += 1 

            self.text1 = get_font_michroma(30).render(self.message[0:self.counter//self.speed_typing], True, "#fafafa")
            width, height = self.game.screen.get_size()
            self.text1_rect = self.text1.get_rect(center=(width // 2, height // 2))
            self.game.screen.blit(self.text1, self.text1_rect)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    
    def check_input(self):
        if (self.game.MOUSE_CLICK_L or self.game.ENTER or self.game.SPACE or self.game.RIGHT):
            if self.counter < self.speed_typing * len(self.message):
                self.counter = self.speed_typing * len(self.message)
            else:
                self.active_message += 1
                if self.active_message == len(self.messages):
                    self.run_display = False
                    print("pregame ukončen")
                    first_play = FirstPlay(self.game)
                    first_play.display_play()
                    
                else: 
                    self.message = self.messages[self.active_message]   
                    self.counter = 0
        elif (self.game.MOUSE_CLICK_R or self.game.LEFT or self.game.BACKSPACE) and self.active_message > 0:
            self.active_message -= 1
            self.message = self.messages[self.active_message]
            self.counter = 0
        elif self.game.ESC:
            self.run_display = False

class FirstPlay(Part):
    def __init__(self, game):
        Part.__init__(self, game)

        self.game.screen.fill((0,0,0))

        self.game.reset_keys()

    def display_play(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        self.small_map = pygame.image.load("../img/map_small_button.png")

        while self.run_display:
            self.map_button = Button(image=self.small_map, pos=(175, 125), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None)
            self.game.screen.fill((0,0,0))
            self.map_button.update(self.game.screen)
            width, height = self.game.screen.get_size()
            self.par_box = pygame.Rect(0, 250, 350, height-250)

            pygame.draw.rect(self.game.screen, (240, 240, 240), self.par_box, 3) 
            with open('../txt/first_election.txt', encoding='utf-8') as text:
                self.text = json.load(text)
            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False

def display_text_in_box(screen, start_w, end_w, start_h, end_h, text, font, color):
    par = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    start_w += 10
    end_w -= 10
    old_w = start_w
    for lines in par:
        for words in lines:
            words_box = font.render(words, True, color)
            word_width, word_height = words_box.get_size()
            if start_w + word_width >= end_w:
                start_w = old_w
                start_h += word_height
            if start_h >= end_h:
                return
            screen.blit(words_box, (start_w, start_h))
            start_w += word_width + space
        start_w = old_w
        start_h += word_height
 


            

# display_text_in_box(0, "ahoj, je den 49 a nemam kraten a ro je to \n a totot 5dak 2 nemsm halda totot 5dak 2 nemsm halda totot 5dak 2 nemsm hald", 0, 0, 0)