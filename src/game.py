import pygame
import json
from buttons import Button
from lib import prefc
from election import get_election_result
from lib import parties, voters

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
                self.TEXT = True
                self.LETTER = event.unicode

        
    def reset_keys(self):
        self.MOUSE_CLICK_L, self.MOUSE_CLICK_R = False, False
        self.LEFT, self.RIGHT, self.UP, self.DOWN = False, False, False, False
        self.ENTER, self.SPACE, self.BACKSPACE, self.ESC = False, False, False, False
        self.TEXT = False

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

            self.PLAY_BUTTON = Button(image=self.menu_button, pos=(width // 2, (height // 2) - 150), text_input = "HRÁT", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
            self.OPTIONS_BUTTON = Button(image=self.menu_button, pos=(width // 2, height // 2), text_input = "NASTAVENÍ", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
            self.QUIT_BUTTON = Button(image=self.menu_button, pos=(width // 2, (height // 2) + 150), text_input = "OPUSTIT", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.menu_button_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

            for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.change_color(self.game.MENU_MOUSE_POS)
                button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    
    def check_input(self):
        if self.game.MOUSE_CLICK_L:
            if self.PLAY_BUTTON.check_input(self.game.MENU_MOUSE_POS):
                self.run_display = False
                pygame.display.set_caption("Game")
                pregame = PreGame(self.game)
                pregame.display_play()
                
            if self.OPTIONS_BUTTON.check_input(self.game.MENU_MOUSE_POS):
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

        self.party_name_writing = False

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.button_clicked = pygame.image.load("../img/election_button_done.png")
        self.button_clicked_hover = pygame.image.load("../img/election_button_done_hover.png")
        self.button_1 = pygame.image.load("../img/election_button_1.png")
        self.button_1_hover = pygame.image.load("../img/election_button_1_hover.png")
        self.button_2 = pygame.image.load("../img/election_button_2.png")
        self.button_2_hover = pygame.image.load("../img/election_button_2_hover.png")
        self.button_3 = pygame.image.load("../img/election_button_3.png")
        self.button_3_hover = pygame.image.load("../img/election_button_3_hover.png")
        self.button_4 = pygame.image.load("../img/election_button_4.png")
        self.button_4_hover = pygame.image.load("../img/election_button_4_hover.png")
        self.button_5 = pygame.image.load("../img/election_button_5.png")
        self.button_5_hover = pygame.image.load("../img/election_button_5_hover.png")

        self.start_x = 420
        self.start_y = 130
        x = self.start_x
        y = self.start_y 
        self.max_x, self.max_y = self.game.screen.get_size()
        
        self.prefc = prefc
        self.election_data = {}
        self.election_buttons = {}
        self.election_labels = []
        for one_prefer in prefc:
            repeating = prefc[one_prefer]["point_class"]["max_rest_count"] + 1
            one_element = {one_prefer : 1}
            self.election_data.update(one_element)
            buttons = {}
            if repeating == 5:
                buttons.update({1 : Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({2 : Button(image=self.button_2, pos=(x+40, y), text_input = "2", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_2_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({3 : Button(image=self.button_3, pos=(x+80, y), text_input = "3", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_3_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({4 : Button(image=self.button_4, pos=(x+120, y), text_input = "4", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_4_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({5 : Button(image=self.button_5, pos=(x+160, y), text_input = "5", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_5_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            if repeating == 4:
                buttons.update({1 : Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({2 : Button(image=self.button_2, pos=(x+40, y), text_input = "2", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_2_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({3 : Button(image=self.button_4, pos=(x+80, y), text_input = "3", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_4_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({4 : Button(image=self.button_5, pos=(x+120, y), text_input = "4", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_5_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            self.election_labels.append((x, y, prefc[one_prefer]["name"]))
            y+=60
            if y >= (self.max_y):
                y = self.start_y
                x += 250
            self.election_buttons.update({one_prefer : buttons})
        self.save_button_img = pygame.image.load("../img/election_save.png")
        self.save_button_img_hover = pygame.image.load("../img/election_save_hover.png")
        self.save_button = Button(image=self.save_button_img, pos=(self.max_x-150, self.max_y-90), text_input = "Uložit", font = get_font_michroma(40), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.save_button_img_hover, clicked_color="#eaeaea", clicked_image=None, clicked_color_hover="#ffffff", clicked_image_hover=None)
        with open('../txt/first_election.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        self.small_map = pygame.image.load("../img/map_small_button.png")
        self.map_button = Button(image=self.small_map, pos=(175, 125), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.big_map_status = False
        self.big_map_picture_og = pygame.image.load("../img/map_big.jpg")
        self.close_big_map_picture = pygame.image.load("../img/close_map_big.jpg")
        self.close_big_map = Button(image=self.close_big_map_picture, pos=(55, 55), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
    def display_play(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        
        self.party_name = ''
        self.party_name_input = pygame.Rect(400, 50, 140, 32)

        self.party_name_input_color_active = pygame.Color(240, 240, 240)
        self.party_name_input_color_pasive = pygame.Color(140, 140, 140)
        self.party_name_input_color = self.party_name_input_color_pasive

        while self.run_display:
            self.game.screen.fill((0,0,0))
            self.map_button.update(self.game.screen)
            width, height = self.game.screen.get_size()
            self.par_box = pygame.Rect(0, 250, 350, height-250)
            pygame.draw.rect(self.game.screen, (240, 240, 240), self.par_box, 3) 
            
            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 390, 600, 10, 80, "Název strany:", get_font_michroma(30), (240, 240, 240))

            if self.party_name_writing:
                self.party_name_input_color = self.party_name_input_color_active
            else:
                self.party_name_input_color = self.party_name_input_color_pasive
            
            self.PARTY_NAME_BOX = get_font_michroma(30).render(self.party_name, True, (self.party_name_input_color))

            pygame.draw.rect(self.game.screen, (self.party_name_input_color), self.party_name_input, 2) 
            self.game.screen.blit(self.PARTY_NAME_BOX, (self.party_name_input.x + 5, self.party_name_input.y + 5))
            self.party_name_input.w = max(100, self.PARTY_NAME_BOX.get_width() + 10)


            for group in self.election_buttons:
                for button in self.election_buttons[group]:
                    self.election_buttons[group][button].change_color(pygame.mouse.get_pos())
                    self.election_buttons[group][button].update(self.game.screen)
            
            for x, y, text in self.election_labels:
                display_text_in_box(self.game.screen, x-30, x+250, y-40, y+50, text, get_font_michroma(20), (240, 240, 240))

            self.save_button.change_color(pygame.mouse.get_pos())
            self.save_button.update(self.game.screen)

            if self.big_map_status:
                self.big_map_picture = pygame.transform.smoothscale(self.big_map_picture_og, (width, height))
                self.big_map = Button(image=self.big_map_picture, pos=(width // 2, height // 2), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
                self.big_map.change_color(pygame.mouse.get_pos())
                self.big_map.update(self.game.screen)

                self.close_big_map.change_color(pygame.mouse.get_pos())
                self.close_big_map.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.game.MOUSE_CLICK_L:
            if self.party_name_input.collidepoint(pygame.mouse.get_pos()):
                self.party_name_writing = True
            else:
                self.party_name_writing = False
            for group in self.election_buttons:
                for button in self.election_buttons[group]:
                    if self.election_buttons[group][button].check_input(pygame.mouse.get_pos()):
                        self.election_buttons[group][button].click_button()
                        self.election_buttons[group][button].update(self.game.screen)
                        self.election_data[group] = button
                        for button_selected in self.election_buttons[group]:
                            if button_selected != button:
                                self.election_buttons[group][button_selected].reset_click_button()
            if self.save_button.check_input(pygame.mouse.get_pos()):
                get_election_result(self.party_name, self.election_data)
                data = {
                    "party_name" : self.party_name,
                    "election_data" : self.election_data,
                    "parties" : parties,
                    "voters" : voters
                }
                with open('../txt/data/first_election_data.txt', "w", encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                self.run_display = False
                second_play = SecondPlay(self.game)
                second_play.display_play()
            if self.map_button.check_input(pygame.mouse.get_pos()):
                self.big_map_status = True
            if self.big_map_status:
                if self.close_big_map.check_input(pygame.mouse.get_pos()):
                    self.big_map_status = False

        if self.party_name_writing:
            if self.game.TEXT and not self.game.BACKSPACE:
                self.party_name += self.game.LETTER
            if self.game.BACKSPACE:
                self.party_name = self.party_name[:-1]

class SecondPlay(Part):
    def __init__(self, game):
        Part.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

     
        with open('../txt/second_play.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        self.small_map = pygame.image.load("../img/map_small_button.png")
        self.map_button = Button(image=self.small_map, pos=(175, 125), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.big_map_status = False
        self.big_map_picture_og = pygame.image.load("../img/map_big.jpg")
        self.close_big_map_picture = pygame.image.load("../img/close_map_big.jpg")
        self.close_big_map = Button(image=self.close_big_map_picture, pos=(55, 55), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
    def display_play(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        
        while self.run_display:
            self.game.screen.fill((0,0,0))
            self.map_button.update(self.game.screen)
            width, height = self.game.screen.get_size()
            self.par_box = pygame.Rect(0, 250, 350, height-250)
            pygame.draw.rect(self.game.screen, (240, 240, 240), self.par_box, 3) 
            
            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 500, 900, 250, 500, "Výsledky voleb byly uloženy. Pane učiteli, můžete si je prohlédnout v first_election_data.txt.", get_font_michroma(30), (240, 240, 240))

            if self.big_map_status:
                self.big_map_picture = pygame.transform.smoothscale(self.big_map_picture_og, (width, height))
                self.big_map = Button(image=self.big_map_picture, pos=(width // 2, height // 2), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
                self.big_map.change_color(pygame.mouse.get_pos())
                self.big_map.update(self.game.screen)

                self.close_big_map.change_color(pygame.mouse.get_pos())
                self.close_big_map.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.game.MOUSE_CLICK_L:
            if self.map_button.check_input(pygame.mouse.get_pos()):
                self.big_map_status = True
            if self.big_map_status:
                if self.close_big_map.check_input(pygame.mouse.get_pos()):
                    self.big_map_status = False

  

def display_text_in_box(screen, start_w, end_w, start_h, end_h, text, font, color):
    par = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    start_w += 10
    end_w -= 10
    start_h += 10
    end_h -= 10
    old_w = start_w
    for lines in par:
        for words in lines:
            words_box = font.render(words, True, color)
            word_width, word_height = words_box.get_size()
            if start_w + word_width >= end_w:
                start_w = old_w
                start_h += word_height
            screen.blit(words_box, (start_w, start_h))
            start_w += word_width + space
        start_w = old_w
        start_h += word_height