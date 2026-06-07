import random
import pygame
import json
import sys
from buttons import Button
from lib import prefc, player_history, game_variables, parties, voters, setting
from function import get_election_result, restart_game, change_game_variables, get_variables_regions, get_variables_subsidy, update_setting, display_text_in_box, play_background_music, stop_background_music, get_final_result

""""classy pro jednolivé části hry"""

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

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
                pygame.quit()
                sys.exit()
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

class OnePlay(Part):
    def __init__(self, game):
        Part.__init__(self, game)
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        self.big_map_status = False

        self.small_map = pygame.image.load("../img/map_small_button.png")
        self.map_button = Button(image=self.small_map, pos=(175, 125), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        
        self.big_map_picture_og = pygame.image.load("../img/map_big.jpg")
        self.close_big_map_picture = pygame.image.load("../img/close_map_big.jpg")
        self.close_big_map = Button(image=self.close_big_map_picture, pos=(55, 55), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
    def display_base(self):
        """zobrazení mapy a boxu pro text"""
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(40)
        self.game.screen.fill((0, 0, 0))
        self.map_button.update(self.game.screen)
        width, height = self.game.screen.get_size()
        self.par_box = pygame.Rect(0, 250, 350, height-250)
        pygame.draw.rect(self.game.screen, (240, 240, 240), self.par_box, 3) 
        if self.big_map_status:
            self.big_map_picture = pygame.transform.smoothscale(self.big_map_picture_og, (width, height))
            self.big_map = Button(image=self.big_map_picture, pos=(width // 2, height // 2), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=None, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
            self.big_map.change_color(pygame.mouse.get_pos())
            self.big_map.update(self.game.screen)

            self.close_big_map.change_color(pygame.mouse.get_pos())
            self.close_big_map.update(self.game.screen)
    def check_map_input(self):
        """otevírání a zavírání mapy"""
        if self.game.MOUSE_CLICK_L:
            pos = pygame.mouse.get_pos()
            if self.big_map_status and self.close_big_map.check_input(pos):
                self.big_map_status = False
                return True
            if self.map_button.check_input(pos):
                self.big_map_status = True
                return True
        return False

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
        stop_background_music()
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
                self.run_display = False
                pygame.display.set_caption("Options")
                options = Options(self.game)
                options.display_options()
            if self.QUIT_BUTTON.check_input(self.game.MENU_MOUSE_POS):
                self.game.running = False
                self.run_display = False

        if self.game.ESC:
            self.game.running = False
            self.run_display = False


def get_font_michroma(size):
    return pygame.font.SysFont('Michroma', size)

class Options(Part):
    def __init__(self, game):
        Part.__init__(self, game)
        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.start_x = 375
        self.start_y = 230
        x = self.start_x
        y = self.start_y 
        self.max_x, self.max_y = self.game.screen.get_size()

        self.button_1 = pygame.image.load("../img/false_button.png")
        self.button_1_hover = pygame.image.load("../img/false_button_hover.png")
        self.button_clicked = pygame.image.load("../img/true_button.png")
        self.button_clicked_hover = pygame.image.load("../img/true_button_hover.png")
        self.prefc = {
            "music" : "Hudba",
        }
        self.options_data = {}
        self.options_buttons = {}
        self.options_labels = []
        for one_prefer in self.prefc:
            one_element = {one_prefer : 1}
            self.options_data.update(one_element)
            buttons = {}
            button_eins = Button(image=self.button_1, pos=(x, y), text_input = "Vypnuto", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
            button_zwei = Button(image=self.button_1, pos=(x+190, y), text_input = "Zapnuto", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
            if setting[one_prefer] == "Vypnuto":
                button_eins.click_button()
            elif setting[one_prefer] == "Zapnuto":
                button_zwei.click_button()
            buttons.update({1 : button_eins})
            buttons.update({2 : button_zwei})
            self.options_labels.append((x, y, self.prefc[one_prefer]))
            y+=100
            if y >= (self.max_y):
                y = self.start_y
                x += 250
            self.options_buttons.update({one_prefer : buttons})

    def display_options(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        
        while self.run_display:
            self.game.screen.fill((0,0,0))
            for group in self.options_buttons:
                for button in self.options_buttons[group]:
                    self.options_buttons[group][button].change_color(pygame.mouse.get_pos())
                    self.options_buttons[group][button].update(self.game.screen)

            for x, y, text in self.options_labels:
                display_text_in_box(self.game.screen, x-100, x+250, y-100, y+80, text, get_font_michroma(40), (240, 240, 240))

            display_text_in_box(self.game.screen, 220, 1000, 60, 500, "Nastavení", get_font_michroma(50), (240, 240, 240))
            
            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.game.MOUSE_CLICK_L:
            for group in self.options_buttons:
                for button in self.options_buttons[group]:
                    if self.options_buttons[group][button].check_input(pygame.mouse.get_pos()):
                        self.options_buttons[group][button].click_button()
                        self.options_buttons[group][button].update(self.game.screen)
                        self.options_data[group] = button
                        for button_selected in self.options_buttons[group]:
                            if button_selected != button:
                                self.options_buttons[group][button_selected].reset_click_button()
                                update_setting(group, self.options_buttons[group][button].text_input)



class PreGame(Part):
    def __init__(self, game):
        Part.__init__(self, game)
        if setting["music"] == "Zapnuto":
            play_background_music("../sound/Arbiter.mp3")
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

class FirstPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

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
                button_eins = Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
                button_eins.click_button()
                buttons.update({1 : button_eins})
                buttons.update({2 : Button(image=self.button_2, pos=(x+40, y), text_input = "2", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_2_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({3 : Button(image=self.button_3, pos=(x+80, y), text_input = "3", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_3_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({4 : Button(image=self.button_4, pos=(x+120, y), text_input = "4", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_4_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
                buttons.update({5 : Button(image=self.button_5, pos=(x+160, y), text_input = "5", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_5_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            if repeating == 4:
                button_eins = Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
                button_eins.click_button()
                buttons.update({1 : button_eins})
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
        with open('../txt/text/first_election/first_election.txt', encoding='utf-8') as text:
            self.text = json.load(text)

    def display_play(self):
        
        self.party_name = ''
        self.party_name_input = pygame.Rect(400, 50, 140, 32)

        self.party_name_input_color_active = pygame.Color(240, 240, 240)
        self.party_name_input_color_pasive = pygame.Color(140, 140, 140)
        self.party_name_input_color = self.party_name_input_color_pasive

        
        while self.run_display:

            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()
            
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


            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
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
                self.party_name.strip()
                if self.party_name == "":
                    self.party_name = "Bezejmenná Strana Asociálů"
                get_election_result(self.party_name, self.election_data)

                data = {
                    "party_name" : self.party_name,
                    "election_data" : self.election_data,
                    "parties" : parties,
                    "voters" : voters
                }
                player_history["first_election"] = data
                with open('../txt/user_data/first_election_data.txt', "w", encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                self.run_display = False
                second_play = SecondPlay(self.game)
                second_play.display_play()

        if self.party_name_writing:
            if self.game.TEXT and not self.game.BACKSPACE:
                self.party_name += self.game.LETTER
            if self.game.BACKSPACE:
                self.party_name = self.party_name[:-1]

class SecondPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()
     

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.party_name = self.data["party_name"]

        if (
            self.party_name in self.data["parties"]
            and self.data["parties"][self.party_name]["seats"] == 101
        ):
            with open('../txt/text/first_election/win.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/first_election/lose.txt', encoding='utf-8') as text:
                self.text = json.load(text)
            
        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.new_game = pygame.image.load("../img/new_game_button.png")
        self.new_game_hover = pygame.image.load("../img/new_game_button_hover.png")
        self.new_game_button = Button(image=self.new_game, pos=(500, 500), text_input = "Nová hra", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.new_game_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()
            if (
                self.party_name in self.data["parties"]
                and self.data["parties"][self.party_name]["seats"] == 101
            ):
                text_color = (0, 133, 22)
                text_text = "Vyhrál jste volby!"
                
                self.next_button.update(self.game.screen)
                self.next_button.change_color(pygame.mouse.get_pos())
            else:
                text_color = (143, 3, 3)
                text_text = "Nevyhrál jste volby..."
                
                self.new_game_button.update(self.game.screen)
                self.new_game_button.change_color(pygame.mouse.get_pos())
            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 500, 900, 250, 500, text_text, get_font_michroma(90), text_color)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if (
                self.party_name in self.data["parties"]
                and self.data["parties"][self.party_name]["seats"] == 101
            ):
                if self.next_button.check_input(pygame.mouse.get_pos()):
                    player_history["media_independence"] = "yes"
                    self.run_display = False
                    third_play = ThirdPlay(self.game)
                    third_play.display_play()
            else:
                if self.new_game_button.check_input(pygame.mouse.get_pos()):
                    restart_game()
                    self.run_display = False
                    first_play = FirstPlay(self.game)
                    first_play.display_play()

class ThirdPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        with open('../txt/collaborator.txt', encoding='utf-8') as text:
            self.text = json.load(text)
     

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.person_one = pygame.image.load("../img/person_one_button.png")
        self.person_one_hover = pygame.image.load("../img/person_one_button_hover.png")
        self.person_one_button = Button(image=self.person_one, pos=(700, 220), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.person_one_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        
        self.person_two = pygame.image.load("../img/person_two_button.png")
        self.person_two_hover = pygame.image.load("../img/person_two_button_hover.png")
        self.person_two_button = Button(image=self.person_two, pos=(700, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.person_two_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            self.person_one_button.update(self.game.screen)
            self.person_one_button.change_color(pygame.mouse.get_pos())

            self.person_two_button.update(self.game.screen)
            self.person_two_button.change_color(pygame.mouse.get_pos())

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 400, 1000, 30, 500, "Vyberte si spolupracovníka", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.person_one_button.check_input(pygame.mouse.get_pos()):
                player_history["collaborator"] = "person_one"
                change_game_variables({"economy" : 1, "diplomacy_alliance" : 1})
                self.run_display = False
                next_play = FourthPlay(self.game)
                next_play.display_play()
            if self.person_two_button.check_input(pygame.mouse.get_pos()):
                player_history["collaborator"] = "person_two"
                change_game_variables({"army" : 1, "diplomacy_enemy" : 1})
                self.run_display = False
                next_play = FourthPlay(self.game)
                next_play.display_play()


class FourthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()
     
        with open('../txt/text/first_diplomatic_route/first_diplomatic_route.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.state_one = pygame.image.load("../img/paper_blue_button.png")
        self.state_one_hover = pygame.image.load("../img/paper_blue_button_hover.png")
        self.state_one_button = Button(image=self.state_one, pos=(500, 300), text_input = "Lupanar (hlavní stát Aliance)", font = get_font_michroma(20), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_one_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        self.state_two = pygame.image.load("../img/paper_yellow_button.png")
        self.state_two_hover = pygame.image.load("../img/paper_yellow_button_hover.png")
        self.state_two_button = Button(image=self.state_two, pos=(800, 300), text_input = "Parsko (nejbližší spojenec)", font = get_font_michroma(20), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_two_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        self.state_three = pygame.image.load("../img/paper_red_button.png")
        self.state_three_hover = pygame.image.load("../img/paper_red_button_hover.png")
        self.state_three_button = Button(image=self.state_three, pos=(1100, 300), text_input = "Sámova říše (nepřítel)", font = get_font_michroma(20), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_three_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)



    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            self.state_one_button.change_color(pygame.mouse.get_pos())
            self.state_one_button.update(self.game.screen)
            self.state_two_button.change_color(pygame.mouse.get_pos())
            self.state_two_button.update(self.game.screen)
            self.state_three_button.change_color(pygame.mouse.get_pos())
            self.state_three_button.update(self.game.screen)

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 400, 1200, 30, 500, "Kam povede první diplomatická cesta", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.state_one_button.check_input(pygame.mouse.get_pos()):
                player_history["first_diplomatic_route"] = "state_one"
                change_game_variables({"diplomacy_alliance" : 2})
                self.run_display = False
                next_play = FifthPlay(self.game)
                next_play.display_play()
            if self.state_two_button.check_input(pygame.mouse.get_pos()):
                player_history["first_diplomatic_route"] = "state_two"
                change_game_variables({"diplomacy_alliance" : 1})
                self.run_display = False
                next_play = FifthPlay(self.game)
                next_play.display_play()
            if self.state_three_button.check_input(pygame.mouse.get_pos()):
                player_history["first_diplomatic_route"] = "state_three"
                change_game_variables({"diplomacy_enemy" : 1, "diplomacy_alliance" : -1})
                self.run_display = False
                next_play = FifthPlay(self.game)
                next_play.display_play()

class FifthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        route = player_history["first_diplomatic_route"]

        with open(f'../txt/text/first_diplomatic_route/first_diplomatic_route_{route}_reaction.txt', encoding='utf-8') as reaction:
            self.reaction = json.load(reaction)

        with open(f'../txt/text/first_diplomatic_route/first_diplomatic_route_{route}.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Přijmout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Nabídka", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                if player_history["first_diplomatic_route"] == "state_one":
                    change_game_variables({"diplomacy_alliance" : 2, "economy" : 1, "social" : 1, "radicalization" : 1, "army" : 1})
                    player_history["first_diplomatic_route_offer"] = "yes"
                    next_play = SixthPlay(self.game)
                elif player_history["first_diplomatic_route"] == "state_two":
                    change_game_variables({"diplomacy_alliance" : 1, "economy" : -1, "social" : 1})
                    player_history["first_diplomatic_route_offer"] = "yes"
                    next_play = SixthPlay(self.game)
                elif player_history["first_diplomatic_route"] == "state_three":
                    change_game_variables({"diplomacy_enemy" : 2, "diplomacy_alliance" : -1, "crime" : 1, "economy" : -1, "radicalization" : 1})
                    player_history["first_diplomatic_route_offer"] = "yes"
                    next_play = SeventhPlay(self.game)
                else:
                    change_game_variables({"diplomacy_alliance" : 2, "economy" : 1, "social" : 1, "radicalization" : 1, "army" : 1})
                    player_history["first_diplomatic_route_offer"] = "yes"
                    next_play = SixthPlay(self.game)
                self.run_display = False
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                if player_history["first_diplomatic_route"] == "state_one":
                    change_game_variables({"diplomacy_alliance" : -1, "economy" : -1, "radicalization" : 2, "diplomacy_enemy" : 1})
                elif player_history["first_diplomatic_route"] == "state_two":
                    change_game_variables({"diplomacy_alliance" : -1, "social" : -1, "radicalization" : -1})
                elif player_history["first_diplomatic_route"] == "state_three":
                    change_game_variables({"diplomacy_enemy" : -1, "diplomacy_alliance" : 1, "economy" : 1, "radicalization" : 1})
                else:
                    change_game_variables({"diplomacy_alliance" : -1, "economy" : -1, "radicalization" : 2, "diplomacy_enemy" : 1})
                player_history["first_diplomatic_route_offer"] = "no"
                self.run_display = False
                next_play = SixthPlay(self.game)
                next_play.display_play()

class SixthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.button_clicked = pygame.image.load("../img/election_button_done.png")
        self.button_clicked_hover = pygame.image.load("../img/election_button_done_hover.png")
        self.button_1 = pygame.image.load("../img/election_button_1.png")
        self.button_1_hover = pygame.image.load("../img/election_button_1_hover.png")
        self.button_2 = pygame.image.load("../img/election_button_3.png")
        self.button_2_hover = pygame.image.load("../img/election_button_3_hover.png")
        self.button_3 = pygame.image.load("../img/election_button_5.png")
        self.button_3_hover = pygame.image.load("../img/election_button_5_hover.png")

        self.start_x = 480
        self.start_y = 230
        x = self.start_x
        y = self.start_y 
        self.max_x, self.max_y = self.game.screen.get_size()

        
        if player_history["first_diplomatic_route"] == "state_one" and player_history["first_diplomatic_route_offer"] == "yes":
            self.old_count = 12
            with open('../txt/text/first_diplomatic_route/state_one_yes_alliance_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        elif player_history["first_diplomatic_route"] == "state_one" and player_history["first_diplomatic_route_offer"] == "no":
            self.old_count = 8
            with open('../txt/text/first_diplomatic_route/state_one_no_alliance_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        elif player_history["first_diplomatic_route"] == "state_two" and player_history["first_diplomatic_route_offer"] == "yes":
            self.old_count = 6
            with open('../txt/text/first_diplomatic_route/state_two_yes_alliance_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        elif player_history["first_diplomatic_route"] == "state_two" and player_history["first_diplomatic_route_offer"] == "no":
            self.old_count = 8
            with open('../txt/text/first_diplomatic_route/state_two_no_alliance_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        elif player_history["first_diplomatic_route"] == "state_three" and player_history["first_diplomatic_route_offer"] == "yes":
            self.old_count = 0
            self.text = "No, tak to je v prdeli."
        else:                
            self.old_count = 8
            with open('../txt/text/first_diplomatic_route/state_three_no_alliance_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        self.prefc = {
            "industry" : "Průmysl",
            "defense" : "Armáda",
            "infrastructure" : "Doprava",
            "housing" : "Bydlení",
            "healthcare" : "Zdravotnictví"
        }
        self.decision_data = {}
        self.decision_buttons = {}
        self.decision_labels = []
        for one_prefer in self.prefc:
            one_element = {one_prefer : 1}
            self.decision_data.update(one_element)
            buttons = {}
            button_eins = Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
            button_eins.click_button()
            buttons.update({1 : button_eins})
            buttons.update({2 : Button(image=self.button_2, pos=(x+40, y), text_input = "2", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_2_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            buttons.update({3 : Button(image=self.button_3, pos=(x+80, y), text_input = "3", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_3_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            self.decision_labels.append((x, y, self.prefc[one_prefer]))
            y+=60
            if y >= (self.max_y):
                y = self.start_y
                x += 250
            self.decision_buttons.update({one_prefer : buttons})
        self.save_button_img = pygame.image.load("../img/election_save.png")
        self.save_button_img_hover = pygame.image.load("../img/election_save_hover.png")
        self.save_button = Button(image=self.save_button_img, pos=(self.max_x-150, self.max_y-90), text_input = "Potvrdit", font = get_font_michroma(40), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.save_button_img_hover, clicked_color="#eaeaea", clicked_image=None, clicked_color_hover="#ffffff", clicked_image_hover=None)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()
            for group in self.decision_buttons:
                for button in self.decision_buttons[group]:
                    self.decision_buttons[group][button].change_color(pygame.mouse.get_pos())
                    self.decision_buttons[group][button].update(self.game.screen)

            self.count = self.old_count
            for group in self.decision_data:
                self.count -= self.decision_data[group]

            self.count_text = "Množství zbývajících peněz: "+str(self.count)

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Dotace od aliance", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 440, 1200, 130, 500, self.count_text, get_font_michroma(30), (240, 240, 240))
            
            for x, y, text in self.decision_labels:
                display_text_in_box(self.game.screen, x-30, x+250, y-40, y+50, text, get_font_michroma(20), (240, 240, 240))

            self.save_button.change_color(pygame.mouse.get_pos())
            self.save_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            for group in self.decision_buttons:
                for button in self.decision_buttons[group]:
                    if self.decision_buttons[group][button].check_input(pygame.mouse.get_pos()):
                        self.decision_buttons[group][button].click_button()
                        self.decision_buttons[group][button].update(self.game.screen)
                        self.decision_data[group] = button
                        for button_selected in self.decision_buttons[group]:
                            if button_selected != button:
                                self.decision_buttons[group][button_selected].reset_click_button()
            if self.save_button.check_input(pygame.mouse.get_pos()):   
                if self.count >= 0:
                    player_history["alliance_subsidy"] = self.decision_data 
                    get_variables_subsidy(self.decision_data)            
                    self.run_display = False
                    next_play = SeventhPlay(self.game)
                    next_play.display_play()

class SeventhPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Přijmout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        with open('../txt/text/media_funding/media_funding.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        if player_history["first_diplomatic_route"] == "state_three" and player_history["first_diplomatic_route_offer"] == "yes":
            with open('../txt/text/media_funding/state_three_media_funding.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/media_funding/normal_media_funding.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()
            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Jak dál financovat média", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : 1, "radicalization" : -1})
                player_history["media_funding"] = "yes"
                self.run_display = False
                next_play = TenthPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : -1, "radicalization" : 1})
                player_history["media_funding"] = "no"
                self.run_display = False
                next_play = EighthPlay(self.game)
                next_play.display_play()

class EighthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.first = pygame.image.load("../img/medium_button.png")
        self.first_hover = pygame.image.load("../img/medium_button_hover.png")
        self.first_button = Button(image=self.first, pos=(1050, 300), text_input = "Nastavit poplatky", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.second = pygame.image.load("../img/medium_button.png")
        self.second_hover = pygame.image.load("../img/medium_button_hover.png")
        self.second_button = Button(image=self.second, pos=(1050, 450), text_input = "Nechat z daní", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.second_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.third = pygame.image.load("../img/medium_button.png")
        self.third_hover = pygame.image.load("../img/medium_button_hover.png")
        self.third_button = Button(image=self.third, pos=(1050, 600), text_input = "Vyhodit ředitele", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.third_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        with open('../txt/text/media_funding/board_reaction.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/text/media_funding/board_reaction_medium.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Reakce na představenstvo", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : -1, "radicalization" : -1})
                player_history["board_reaction"] = "first"
                self.run_display = False
                next_play = TenthPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"radicalization" : 1, "diplomacy_enemy" : 1})
                player_history["board_reaction"] = "second"
                self.run_display = False
                next_play = NinthPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : 1, "radicalization" : 2, "diplomacy_enemy" : 1, "crime" : 2, "control_system" : 1})
                player_history["board_reaction"] = "third"
                player_history["media_independence"] = "no"
                self.run_display = False
                next_play = NinthPlay(self.game)
                next_play.display_play()

class NinthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "no":
            with open('../txt/text/media_funding/demonstration_no_independence.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            with open('../txt/text/media_funding/demonstration_no_independence_medium.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/media_funding/demonstration_yes_independence.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            with open('../txt/text/media_funding/demonstration_yes_independence_medium.txt', encoding='utf-8') as text:
                self.text = json.load(text)


        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.choice_one = pygame.image.load("../img/paper_blue_button.png")
        self.choice_one_hover = pygame.image.load("../img/paper_blue_button_hover.png")
        self.choice_one_button = Button(image=self.choice_one, pos=(500, 600), text_input = "Omluvit se", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.choice_one_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.choice_two = pygame.image.load("../img/paper_yellow_button.png")
        self.choice_two_hover = pygame.image.load("../img/paper_yellow_button_hover.png")
        self.choice_two_button = Button(image=self.choice_two, pos=(800, 600), text_input = "Ohradit se", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.choice_two_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.choice_three = pygame.image.load("../img/paper_red_button.png")
        self.choice_three_hover = pygame.image.load("../img/paper_red_button_hover.png")
        self.choice_three_button = Button(image=self.choice_three, pos=(1100, 600), text_input = "Zakázat demonstrovat", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.choice_three_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Velká demonstrace", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 1200, 150, height-450, self.text2, get_font_michroma(30), (240, 240, 240))

            self.choice_one_button.change_color(pygame.mouse.get_pos())
            self.choice_one_button.update(self.game.screen)
            self.choice_two_button.change_color(pygame.mouse.get_pos())
            self.choice_two_button.update(self.game.screen)
            self.choice_three_button.change_color(pygame.mouse.get_pos())
            self.choice_three_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.choice_one_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 2, "social" : -1, "radicalization" : 1})
                player_history["media_independence"] = "yes"
                player_history["demonstration_reaction"] = "choice_one"
                self.run_display = False
                next_play = TenthPlay(self.game)
                next_play.display_play()
            if self.choice_two_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"social" : 1, "radicalization" : 1, "diplomacy_enemy" : 1, "control_system" : 1})
                player_history["demonstration_reaction"] = "choice_two"
                self.run_display = False
                next_play = TenthPlay(self.game)
                next_play.display_play()
            if self.choice_three_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : -1, "radicalization" : 2, "diplomacy_enemy" : 1, "crime" : 2, "control_system" : 2})
                player_history["media_independence"] = "no"
                player_history["demonstration_reaction"] = "choice_three"
                self.run_display = False
                next_play = TenthPlay(self.game)
                next_play.display_play()

class TenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        with open('../txt/text/mafia/oligarch.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Přijmout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()
            
            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "M. Balcar chce pomoct", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 2, "social" : 1, "crime" : 2, "control_system" : -1})
                player_history["balcar_help"] = "yes"
                self.run_display = False
                next_play = EleventhPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"social" : 1, "crime" : -1, "control_system" : 1})
                player_history["balcar_help"] = "no"
                self.run_display = False
                next_play = EleventhPlay(self.game)
                next_play.display_play()
    
class EleventhPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "yes":
            with open('../txt/text/mafia/yes_independence/president_medium.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)
        else: 
            with open('../txt/text/mafia/no_independence/president_medium.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)

        with open('../txt/text/mafia/president.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Prezident", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = TwelfthPlay(self.game)
                next_play.display_play()

class TwelfthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "yes":
            with open('../txt/text/mafia/yes_independence/president_medium.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)
            with open('../txt/text/mafia/yes_independence/president_offer.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else: 
            with open('../txt/text/mafia/no_independence/president_medium.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)
            with open('../txt/text/mafia/no_independence/president_offer.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Přijmout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Prezidentova nabídka", get_font_michroma(50), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 2, "social" : 1, "radicalization" : -2, "diplomacy_alliance" : 2})
                player_history["president_offer"] = "yes"
                self.run_display = False
                next_play = ThirteenPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"social" : 1, "control_system" : 1, "radicalization" : 1, "diplomacy_enemy" : 1})
                player_history["president_offer"] = "no"
                self.run_display = False
                next_play = ThirteenPlay(self.game)
                next_play.display_play()

class ThirteenPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["collaborator"] == "person_one":
            with open('../txt/text/mafia/raid_balcar.txt', encoding='utf-8') as text:
                self.text = json.load(text)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/mafia/yes_independence/raid_balcar_medium.txt', encoding='utf-8') as reaction:
                    self.reaction = json.load(reaction)
            else:
                with open('../txt/text/mafia/no_independence/raid_medium.txt', encoding='utf-8') as reaction:
                    self.reaction = json.load(reaction)
        else:
            with open('../txt/text/mafia/raid_rukzak.txt', encoding='utf-8') as text:
                self.text = json.load(text)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/mafia/yes_independence/raid_rukzak_medium.txt', encoding='utf-8') as reaction:
                    self.reaction = json.load(reaction)
            else:
                with open('../txt/text/mafia/no_independence/raid_medium.txt', encoding='utf-8') as reaction:
                    self.reaction = json.load(reaction)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Razie u kolegy", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = FourteenthPlay(self.game)
                next_play.display_play()

class FourteenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.first = pygame.image.load("../img/paper_blue_button.png")
        self.first_hover = pygame.image.load("../img/paper_blue_button_hover.png")
        self.first_button = Button(image=self.first, pos=(500, 600), text_input = "Nechat být", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.second = pygame.image.load("../img/paper_yellow_button.png")
        self.second_hover = pygame.image.load("../img/paper_yellow_button_hover.png")
        self.second_button = Button(image=self.second, pos=(800, 600), text_input = "Kritizovat", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.second_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.third = pygame.image.load("../img/paper_red_button.png")
        self.third_hover = pygame.image.load("../img/paper_red_button_hover.png")
        self.third_button = Button(image=self.third, pos=(1100, 600), text_input = "Zlikvidovat", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.third_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        
        if player_history["media_independence"] == "yes":
            with open('../txt/text/mafia/yes_independence/demonstration.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/mafia/no_independence/demonstration.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/mafia/demonstration.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Co s demonstranty", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 1200, 150, height-450, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.big_map_status:
                if self.close_big_map.check_input(pygame.mouse.get_pos()):
                    self.big_map_status = False
            if self.map_button.check_input(pygame.mouse.get_pos()):
                self.big_map_status = True
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : -2, "radicalization" : -2, "diplomacy_alliance" : 1})
                player_history["demonstration_action"] = "first"
                self.run_display = False
                next_play = FifteenthPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"social" : 1, "control_system" : 1, "radicalization" : 2, "diplomacy_enemy" : 1})
                player_history["demonstration_action"] = "second"
                self.run_display = False
                next_play = FifteenthPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"radicalization" : 3, "diplomacy_enemy" : 2, "crime" : 2, "control_system" : 3})
                player_history["demonstration_action"] = "third"
                self.run_display = False
                next_play = FifteenthPlay(self.game)
                next_play.display_play()

class FifteenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["demonstration_action"] == "third":
            with open('../txt/text/mafia/justicy_big.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/mafia/yes_independence/justicy_state_three.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
            else:
                with open('../txt/text/mafia/no_independence/justicy.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
        else: 
            with open('../txt/text/mafia/justicy.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/mafia/yes_independence/justicy_state_normal.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
            else:
                with open('../txt/text/mafia/no_independence/justicy.txt', encoding='utf-8') as text:
                    self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
        self.first = pygame.image.load("../img/medium_button.png")
        self.first_hover = pygame.image.load("../img/medium_button_hover.png")
        self.first_button = Button(image=self.first, pos=(1050, 300), text_input = "Uznat pravomoce", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.second = pygame.image.load("../img/medium_button.png")
        self.second_hover = pygame.image.load("../img/medium_button_hover.png")
        self.second_button = Button(image=self.second, pos=(1050, 450), text_input = "Zpochybnit", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.second_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.third = pygame.image.load("../img/medium_button.png")
        self.third_hover = pygame.image.load("../img/medium_button_hover.png")
        self.third_button = Button(image=self.third, pos=(1050, 600), text_input = "Vyměnit soudce", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.third_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Ministerstvo Spravedlnosti", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : -2, "radicalization" : -2, "diplomacy_alliance" : 1})
                player_history["justice_ministry_decision"] = "first"
                self.run_display = False
                next_play = SixteenthPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"social" : 1, "control_system" : 1, "radicalization" : 2, "diplomacy_enemy" : 1})
                player_history["justice_ministry_decision"] = "second"
                self.run_display = False
                next_play = SixteenthPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"radicalization" : 3, "diplomacy_enemy" : 2, "crime" : 2, "control_system" : 3})
                player_history["justice_ministry_decision"] = "third"
                self.run_display = False
                next_play = SixteenthPlay(self.game)
                next_play.display_play()

class SixteenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Konat", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Nekonat", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/mafia/yes_independence/olympic.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/mafia/no_independence/olympic.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/mafia/olympic.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Sportovní hry", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -2, "social" : 1, "radicalization" : -1, "diplomacy_alliance" : 1})
                player_history["sport_games_decision"] = "yes"
                self.run_display = False
                next_play = SeventeenthPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 2, "social" : -1, "radicalization" : 1})
                player_history["sport_games_decision"] = "no"
                self.run_display = False
                next_play = SeventeenthPlay(self.game)
                next_play.display_play()

class SeventeenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/start.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)
        else:
            with open('../txt/text/war/no_independence/start.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)

        with open('../txt/text/war/start.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Vypukla válka", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = EighteenthPlay(self.game)
                next_play.display_play()

class EighteenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.first = pygame.image.load("../img/paper_red_button.png")
        self.first_hover = pygame.image.load("../img/paper_red_button_hover.png")

        self.first_button = Button(image=self.first, pos=(500, 600), text_input = "Přijmout", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.second_button = Button(image=self.first, pos=(800, 600), text_input = "Kritizovat", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.third_button = Button(image=self.first, pos=(1100, 600), text_input = "Uzavřít hranice", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/migration.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:  
            with open('../txt/text/war/no_independence/migration.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/war/migration.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Migrace na hranicích", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 1200, 150, height-450, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : 1, "radicalization" : -3, "diplomacy_alliance" : 2})
                player_history["migration_decision"] = "first"
                self.run_display = False
                next_play = NineteenthPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : -1, "radicalization" : 2, "diplomacy_enemy" : 1})
                player_history["migration_decision"] = "second"
                self.run_display = False
                next_play = NineteenthPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({ "social" : 1, "radicalization" : 3, "diplomacy_alliance" : -2, "diplomacy_enemy" : 2, "crime" : 2, "control_system" : 3})
                player_history["migration_decision"] = "third"
                self.run_display = False
                next_play = NineteenthPlay(self.game)
                next_play.display_play()

class NineteenthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.first = pygame.image.load("../img/medium_button.png")
        self.first_hover = pygame.image.load("../img/medium_button_hover.png")
        self.first_button = Button(image=self.first, pos=(1050, 150), text_input = "Ubrat peníze", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.second_button = Button(image=self.first, pos=(1050, 300), text_input = "Nechat být", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.third_button = Button(image=self.first, pos=(1050, 450), text_input = "Trochu zvýšit", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.fourth_button = Button(image=self.first, pos=(1050, 600), text_input = "Zvýšit výrazně", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/army.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:  
            with open('../txt/text/war/no_independence/army.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/war/army.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Armáda", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-450, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.fourth_button.change_color(pygame.mouse.get_pos())
            self.fourth_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"army" : -2, "diplomacy_alliance" : -3, "diplomacy_enemy" : 1, "radicalization" : 1, "control_system" : 1})
                player_history["army_decision"] = "first"
                self.run_display = False
                next_play = TwentiethPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -1, "diplomacy_enemy" : 1, "radicalization" : 2})
                player_history["army_decision"] = "second"
                self.run_display = False
                next_play = TwentiethPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"army" : 1, "diplomacy_alliance" : 1, "diplomacy_enemy" : -1, "radicalization" : 1, "control_system" : -1})
                player_history["army_decision"] = "third"
                self.run_display = False
                next_play = TwentiethPlay(self.game)
                next_play.display_play()
            if self.fourth_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"army" : 2, "economy" : 1, "diplomacy_alliance" : 2, "diplomacy_enemy" : -2, "radicalization" : 1, "control_system" : 1})
                player_history["army_decision"] = "fourth"
                self.run_display = False
                next_play = TwentiethPlay(self.game)
                next_play.display_play()

class TwentiethPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Pomoct", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Nepomoct", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/inflation.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:  
            with open('../txt/text/war/no_independence/inflation.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/war/inflation.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Inflace", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 2, "social" : 1, "radicalization" : -2, "crime" : -1})
                player_history["inflation_decision"] = "yes"
                self.run_display = False
                next_play = TwentyfirstPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -2, "social" : -3, "radicalization" : 2, "crime" : 1})
                player_history["inflation_decision"] = "no"
                self.run_display = False
                next_play = TwentysecondPlay(self.game)
                next_play.display_play()

class TwentyfirstPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.button_clicked = pygame.image.load("../img/election_button_done.png")
        self.button_clicked_hover = pygame.image.load("../img/election_button_done_hover.png")
        self.button_1 = pygame.image.load("../img/election_button_1.png")
        self.button_1_hover = pygame.image.load("../img/election_button_1_hover.png")
        self.button_2 = pygame.image.load("../img/election_button_3.png")
        self.button_2_hover = pygame.image.load("../img/election_button_3_hover.png")
        self.button_3 = pygame.image.load("../img/election_button_5.png")
        self.button_3_hover = pygame.image.load("../img/election_button_5_hover.png")

        self.start_x = 480
        self.start_y = 230
        x = self.start_x
        y = self.start_y 
        self.max_x, self.max_y = self.game.screen.get_size()

        self.prefc = {
            "tutus" : "Tutus (hlavní město)",
            "foramen" : "Foramen (okolí hlavního města)",
            "parvus" : "Parvus (nejchudší region)",
            "altus" : "Altus (druhý nejbohatší region, nejmenší podpora premiéra)"
        }
        self.decision_data = {}
        self.decision_buttons = {}
        self.decision_labels = []
        for one_prefer in self.prefc:
            one_element = {one_prefer : 1}
            self.decision_data.update(one_element)
            buttons = {}
            button_eins = Button(image=self.button_1, pos=(x, y), text_input = "1", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_1_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)
            button_eins.click_button()
            buttons.update({1 : button_eins})
            buttons.update({2 : Button(image=self.button_2, pos=(x+40, y), text_input = "2", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_2_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            buttons.update({3 : Button(image=self.button_3, pos=(x+80, y), text_input = "3", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.button_3_hover, clicked_color="#eaeaea", clicked_image=self.button_clicked, clicked_color_hover="#ffffff", clicked_image_hover=self.button_clicked_hover)})
            self.decision_labels.append((x, y, self.prefc[one_prefer]))
            y+=60
            if y >= (self.max_y):
                y = self.start_y
                x += 250
            self.decision_buttons.update({one_prefer : buttons})
        self.save_button_img = pygame.image.load("../img/election_save.png")
        self.save_button_img_hover = pygame.image.load("../img/election_save_hover.png")
        self.save_button = Button(image=self.save_button_img, pos=(self.max_x-150, self.max_y-90), text_input = "Potvrdit", font = get_font_michroma(40), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.save_button_img_hover, clicked_color="#eaeaea", clicked_image=None, clicked_color_hover="#ffffff", clicked_image_hover=None)

        self.old_count = 10

        if player_history["media_independence"] == "yes":
             with open('../txt/text/war/yes_independence/region_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/war/no_independence/region_subsidy.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Dotace regionům", get_font_michroma(50), (240, 240, 240))
            
            for group in self.decision_buttons:
                for button in self.decision_buttons[group]:
                    self.decision_buttons[group][button].change_color(pygame.mouse.get_pos())
                    self.decision_buttons[group][button].update(self.game.screen)

            self.count = self.old_count
            for group in self.decision_data:
                self.count -= self.decision_data[group]

            self.count_text = "Množství zbývajících peněz: "+str(self.count)

            display_text_in_box(self.game.screen, 440, 1200, 130, 500, self.count_text, get_font_michroma(30), (240, 240, 240))
            
            for x, y, text in self.decision_labels:
                display_text_in_box(self.game.screen, x-30, x+450, y-40, y+50, text, get_font_michroma(20), (240, 240, 240))

            self.save_button.change_color(pygame.mouse.get_pos())
            self.save_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            for group in self.decision_buttons:
                for button in self.decision_buttons[group]:
                    if self.decision_buttons[group][button].check_input(pygame.mouse.get_pos()):
                        self.decision_buttons[group][button].click_button()
                        self.decision_buttons[group][button].update(self.game.screen)
                        self.decision_data[group] = button
                        for button_selected in self.decision_buttons[group]:
                            if button_selected != button:
                                self.decision_buttons[group][button_selected].reset_click_button()
            if self.save_button.check_input(pygame.mouse.get_pos()):   
                if self.count >= 0:
                    player_history["region_subsidies_decision"] = self.decision_data  
                    get_variables_regions(self.decision_data)           
                    self.run_display = False
                    next_play = TwentysecondPlay(self.game)
                    next_play.display_play()
class TwentysecondPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/alliance_problems.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)
        else:  
            with open('../txt/text/war/no_independence/alliance_problems.txt', encoding='utf-8') as reaction:
                self.reaction = json.load(reaction)

        with open('../txt/text/war/alliance_problems.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.reaction, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Problémy v alianci", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = TwentythirdPlay(self.game)
                next_play.display_play()

class TwentythirdPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Bude", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Nebude", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/war/yes_independence/referendum.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/war/no_independence/referendum.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/war/referendum.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Bude referendum?", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : 1, "radicalization" : -1, "crime" : -1})
                player_history["referendum_decision"] = "yes"
                self.run_display = False
                next_play = TwentyfourthPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : -1, "radicalization" : 2, "crime" : 2, "control_system" : 1})
                player_history["referendum_decision"] = "no"
                self.run_display = False
                next_play = TwentyseventhPlay(self.game)
                next_play.display_play()

class TwentyfourthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        with open('../txt/text/war/campaign.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
        self.first = pygame.image.load("../img/medium_button.png")
        self.first_hover = pygame.image.load("../img/medium_button_hover.png")
        self.first_button = Button(image=self.first, pos=(1050, 300), text_input = "Pro vystoupení", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.second = pygame.image.load("../img/medium_button.png")
        self.second_hover = pygame.image.load("../img/medium_button_hover.png")
        self.second_button = Button(image=self.second, pos=(1050, 450), text_input = "Neutralita", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.second_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.third = pygame.image.load("../img/medium_button.png")
        self.third_hover = pygame.image.load("../img/medium_button_hover.png")
        self.third_button = Button(image=self.third, pos=(1050, 600), text_input = "Pro zůstání", font = get_font_michroma(30), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.third_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Kampaň", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                player_history["campaign_decision"] = "first"
                self.run_display = False
                next_play = TwentyfifthPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                player_history["campaign_decision"] = "second"
                self.run_display = False
                next_play = TwentyfifthPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                player_history["campaign_decision"] = "third"
                self.run_display = False
                next_play = TwentyfifthPlay(self.game)
                next_play.display_play()

class TwentyfifthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()
        
        results = ["yes", "no"]

        result = random.choices(results, weights=(0.4, 0.6), k=1)[0]

        if player_history["campaign_decision"] == "first":
            if result == "yes":
                change_game_variables({"economy" : 2, "social" : 1, "radicalization" : -2, "crime" : -1})
                player_history["referundum_result"] = "win"
            else:
                change_game_variables({"economy" : -2, "social" : -3, "radicalization" : 2, "crime" : 1})
                player_history["referundum_result"] = "lose"
        else:
            if result == "yes":
                change_game_variables({"economy" : -1, "social" : -1, "radicalization" : 1, "crime" : 1})
                player_history["referundum_result"] = "lose"
            else:
                change_game_variables({"economy" : 1, "social" : 1, "radicalization" : -1, "crime" : -1})
                player_history["referundum_result"] = "win"

        if result == "yes":
            with open('../txt/text/war/referendum_results_yes.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/war/referendum_results_no.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Výsledky referenda", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = TwentysixthPlay(self.game)
                next_play.display_play()

class TwentysixthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Přijmout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        if player_history["referundum_result"] == "win":
            with open('../txt/text/war/result_confirm_yes.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/war/yes_independence/result_confirm_yes.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
            else:
                 with open('../txt/text/war/no_independence/result_confirm.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
        else:
            with open('../txt/text/war/result_confirm_no.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
            if player_history["media_independence"] == "yes":
                with open('../txt/text/war/yes_independence/result_confirm_no.txt', encoding='utf-8') as text:
                    self.text = json.load(text)
            else:
                 with open('../txt/text/war/no_independence/result_confirm.txt', encoding='utf-8') as text:
                    self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Schválit referendum", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : 1, "social" : -1, "radicalization" : 1, "crime" : 1})
                player_history["confirm_referendum"] = "yes"
                self.run_display = False
                next_play = TwentyseventhPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"economy" : -1, "social" : 1, "radicalization" : 2, "crime" : 2, "control_system" : 1})
                player_history["confirm_referendum"] = "no"
                self.run_display = False
                next_play = TwentyseventhPlay(self.game)
                next_play.display_play()

class TwentyseventhPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        with open('../txt/text/civil_war/start.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Občanská válka", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = TwentyeighthPlay(self.game)
                next_play.display_play()

class TwentyeighthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Ano", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Ne", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/civil_war/yes_independence/reaction.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:  
            with open('../txt/text/civil_war/no_independence/reaction.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/civil_war/reaction.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Reagovat", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -1, "social" : 1, "radicalization" : 1, "control_system" : 1})
                player_history["civil_war_decision"] = "yes"
                self.run_display = False
                next_play = TwentyNinethPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : 1, "social" : -1, "radicalization" : 2, "control_system" : -3})
                player_history["civil_war_decision"] = "no"
                self.run_display = False
                next_play = ThirtythirdPlay(self.game)
                next_play.display_play()

class TwentyNinethPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["media_independence"] == "yes":
            with open('../txt/text/civil_war/yes_independence/how.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:  
            with open('../txt/text/civil_war/no_independence/how.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.state_one = pygame.image.load("../img/paper_blue_button.png")
        self.state_one_hover = pygame.image.load("../img/paper_blue_button_hover.png")
        self.state_one_button = Button(image=self.state_one, pos=(500, 300), text_input = "Příměří", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_one_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.state_two = pygame.image.load("../img/paper_yellow_button.png")
        self.state_two_hover = pygame.image.load("../img/paper_yellow_button_hover.png")
        self.state_two_button = Button(image=self.state_two, pos=(800, 300), text_input = "Zajmout vůdce", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_two_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.state_three = pygame.image.load("../img/paper_red_button.png")
        self.state_three_hover = pygame.image.load("../img/paper_red_button_hover.png")
        self.state_three_button = Button(image=self.state_three, pos=(1100, 300), text_input = "Zlikvidovat", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_three_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            self.state_one_button.change_color(pygame.mouse.get_pos())
            self.state_one_button.update(self.game.screen)
            self.state_two_button.change_color(pygame.mouse.get_pos())
            self.state_two_button.update(self.game.screen)
            self.state_three_button.change_color(pygame.mouse.get_pos())
            self.state_three_button.update(self.game.screen)

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 400, 1200, 30, 500, "Jak bojovat", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.state_one_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : 1, "social" : 1, "radicalization" : -3, "control_system" : -2})
                player_history["civil_war_strategy"] = "state_one"
                self.run_display = False
                next_play = ThirtythPlay(self.game)
                next_play.display_play()
            if self.state_two_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({ "social" : 1, "radicalization" : 1, "control_system" : 1})
                player_history["civil_war_strategy"] = "state_two"
                self.run_display = False
                next_play = ThirtythPlay(self.game)
                next_play.display_play()
            if self.state_three_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -2, "social" : -2, "radicalization" : 2, "control_system" : 3})
                player_history["civil_war_strategy"] = "state_three"
                self.run_display = False
                next_play = ThirtythPlay(self.game)
                next_play.display_play()

class ThirtythPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.first = pygame.image.load("../img/medium_button.png")
        self.first_hover = pygame.image.load("../img/medium_button_hover.png")
        self.first_button = Button(image=self.first, pos=(1050, 150), text_input = "Balcar", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.second_button = Button(image=self.first, pos=(1050, 300), text_input = "Rukzak", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.third_button = Button(image=self.first, pos=(1050, 450), text_input = "Lidé", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)
        self.fourth_button = Button(image=self.first, pos=(1050, 600), text_input = "Aliance", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.first_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/civil_war/yes_independence/with.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/civil_war/no_independence/with.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        with open('../txt/text/civil_war/with.txt', encoding='utf-8') as text2:
            self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "S kým bojovat", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-450, self.text2, get_font_michroma(30), (240, 240, 240))

            self.first_button.change_color(pygame.mouse.get_pos())
            self.first_button.update(self.game.screen)

            self.second_button.change_color(pygame.mouse.get_pos())
            self.second_button.update(self.game.screen)

            self.third_button.change_color(pygame.mouse.get_pos())
            self.third_button.update(self.game.screen)

            self.fourth_button.change_color(pygame.mouse.get_pos())
            self.fourth_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.first_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -1, "social" : -2, "radicalization" : 2, "control_system" : -2, "crime" : 2, "economy" : 1})
                player_history["civil_war_supporter"] = "state_one"
                self.run_display = False
                next_play = ThirtyfirstPlay(self.game)
                next_play.display_play()
            if self.second_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -4, "social" : -1, "radicalization" : 3, "control_system" : -2, "crime" : 1, "army" : 1, "diplomacy_enemy" : 3})
                player_history["civil_war_supporter"] = "state_two"
                self.run_display = False
                next_play = ThirtyfirstPlay(self.game)
                next_play.display_play()
            if self.third_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({ "social" : 3, "radicalization" : -2, "control_system" : 1, "crime" : -1, "economy" : 1})
                player_history["civil_war_supporter"] = "state_three"
                self.run_display = False
                next_play = ThirtyfirstPlay(self.game)
                next_play.display_play()
            if self.fourth_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : 4, "social" : -2, "radicalization" : -3, "control_system" : -5, "crime" : -2, "economy" : 1, "diplomacy_enemy" : -4})
                player_history["civil_war_supporter"] = "state_four"
                self.run_display = False
                next_play = ThirtyfirstPlay(self.game)
                next_play.display_play()

class ThirtyfirstPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Souhlasit", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Odmítnout", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        if player_history["media_independence"] == "yes":
            with open('../txt/text/civil_war/yes_independence/collaborator.txt', encoding='utf-8') as text:
                self.text = json.load(text)
        else:
            with open('../txt/text/civil_war/no_independence/collaborator.txt', encoding='utf-8') as text:
                self.text = json.load(text)

        if player_history["collaborator"] == "person_one":
            with open('../txt/text/civil_war/collaborator_balcar.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)
        else:
            with open('../txt/text/civil_war/collaborator_rukzak.txt', encoding='utf-8') as text2:
                self.text2 = json.load(text2)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Spor se spolupracovníkem", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : -2, "social" : -3, "radicalization" : 4, "control_system" : -2, "economy" : -1})
                player_history["conflict_with_collaborator"] = "yes"
                self.run_display = False
                next_play = ThirtythirdPlay(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"diplomacy_alliance" : 1, "social" : 2, "radicalization" : -2, "control_system" : 2, "economy" : 1})
                player_history["conflict_with_collaborator"] = "no"
                self.run_display = False
                next_play = ThirtysecondPlay(self.game)
                next_play.display_play()
    
class ThirtysecondPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()
     
        with open('../txt/text/civil_war/collaborator_solution.txt', encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.state_one = pygame.image.load("../img/paper_blue_button.png")
        self.state_one_hover = pygame.image.load("../img/paper_blue_button_hover.png")
        self.state_one_button = Button(image=self.state_one, pos=(500, 300), text_input = "Předat vládu", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_one_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)


        self.state_two = pygame.image.load("../img/paper_yellow_button.png")
        self.state_two_hover = pygame.image.load("../img/paper_yellow_button_hover.png")
        self.state_two_button = Button(image=self.state_two, pos=(800, 300), text_input = "Vyhodit", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_two_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.state_three = pygame.image.load("../img/paper_red_button.png")
        self.state_three_hover = pygame.image.load("../img/paper_red_button_hover.png")
        self.state_three_button = Button(image=self.state_three, pos=(1100, 300), text_input = "Zastřelit", font = get_font_michroma(25), base_color = "#1c1c1c", hover_color = "#282828", hover_image=self.state_three_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            self.state_one_button.change_color(pygame.mouse.get_pos())
            self.state_one_button.update(self.game.screen)
            self.state_two_button.change_color(pygame.mouse.get_pos())
            self.state_two_button.update(self.game.screen)
            self.state_three_button.change_color(pygame.mouse.get_pos())
            self.state_three_button.update(self.game.screen)

            display_text_in_box(self.game.screen, 0, 350, 250, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 400, 1200, 30, 500, "Co s ním?", get_font_michroma(50), (240, 240, 240))

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.state_one_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"control_system" : -8, "crime" : -1})
                player_history["conflict_with_collaborator_solution"] = "state_one"
                self.run_display = False
                next_play = ThirtythirdPlay(self.game)
                next_play.display_play()
            if self.state_two_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"crime" : 2, "control_system" : 1})
                player_history["conflict_with_collaborator_solution"] = "state_two"
                self.run_display = False
                next_play = ThirtythirdPlay(self.game)
                next_play.display_play()
            if self.state_three_button.check_input(pygame.mouse.get_pos()):
                change_game_variables({"control_system" : 2, "crime" : 4})
                player_history["conflict_with_collaborator_solution"] = "state_three"
                self.run_display = False
                next_play = ThirtythirdPlay(self.game)
                next_play.display_play()

class ThirtythirdPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        if player_history["civil_war_decision"] == "yes":
            if player_history["conflict_with_collaborator"] == "no":
                if player_history["conflict_with_collaborator_solution"] == "state_one":
                    text_path = '../txt/text/ends/collaborator_betrayer.txt'
                else:
                    if game_variables["army"] * round(random.uniform(0.80, 1.00), 2) >= 5:
                        text_path = '../txt/text/ends/good_army.txt'
                    else:
                        text_path = '../txt/text/ends/bad_army.txt'
            else:
                text_path = '../txt/text/ends/rentier.txt'
        else:
            if player_history["media_independence"] == "yes":
                text_path = '../txt/text/ends/no_reaction_yes_liberty.txt'
            else:
                if game_variables["radicalization"] * round(random.uniform(0.80, 1.00), 2) >= 10:
                    text_path = '../txt/text/ends/no_reaction_no_liberty_sad.txt'
                else:
                    text_path = '../txt/text/ends/no_reaction_no_liberty_happy.txt'

        with open(text_path, encoding='utf-8') as text:
            self.text = json.load(text)

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)

        self.next = pygame.image.load("../img/next_button.png")
        self.next_hover = pygame.image.load("../img/next_button_hover.png")
        self.next_button = Button(image=self.next, pos=(800, 500), text_input = None, font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.next_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text, get_font_michroma(30), (240, 240, 240))
            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Poslední pomazání", get_font_michroma(50), (240, 240, 240))
            
            self.next_button.update(self.game.screen)
            self.next_button.change_color(pygame.mouse.get_pos())

            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = ThirtyfourthPlay(self.game)
                next_play.display_play()

class ThirtyfourthPlay(OnePlay):
    def __init__(self, game):
        OnePlay.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.next_button = Button(image=self.yes, pos=(1050, 450), text_input = "Ukončit", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.text2 = get_final_result()

        with open('../txt/user_data/first_election_data.txt', encoding='utf-8') as data:
            self.data = json.load(data)
            
    def display_play(self):
        while self.run_display:
            OnePlay.display_base(self)
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "Jak jsi skončil", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 450, 900, 150, height-250, self.text2, get_font_michroma(30), (240, 240, 240))

            self.next_button.change_color(pygame.mouse.get_pos())
            self.next_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.check_map_input():
            return
        if self.game.MOUSE_CLICK_L:
            if self.next_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = EndPlay(self.game)
                next_play.display_play()

class EndPlay(Part):
    def __init__(self, game):
        Part.__init__(self, game)

        self.game.screen.fill((0,0,0))
        self.game.reset_keys()

        self.yes = pygame.image.load("../img/true_button.png")
        self.yes_hover = pygame.image.load("../img/true_button_hover.png")
        self.yes_button = Button(image=self.yes, pos=(1050, 450), text_input = "Hrát znovu", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.yes_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

        self.no = pygame.image.load("../img/false_button.png")
        self.no_hover = pygame.image.load("../img/false_button_hover.png")
        self.no_button = Button(image=self.no, pos=(1050, 600), text_input = "Ukončit hru", font = get_font_michroma(50), base_color = "#eaeaea", hover_color = "#ffffff", hover_image=self.no_hover, clicked_color=None, clicked_image=None, clicked_color_hover=None, clicked_image_hover=None)

    def display_play(self):
        self.run_display = True
        self.clock = pygame.time.Clock()
        self.clock.tick(20)
        
        while self.run_display:
            self.game.screen.fill((0,0,0))
            width, height = self.game.screen.get_size()

            display_text_in_box(self.game.screen, 430, 1200, 60, 500, "KONEC", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 300, 900, 200, 600, "Vytvořil: Jan Kaluža", get_font_michroma(50), (240, 240, 240))
            display_text_in_box(self.game.screen, 300, 900, 340, 700, "Hudba: Soňa Švíková", get_font_michroma(50), (240, 240, 240))

            self.yes_button.change_color(pygame.mouse.get_pos())
            self.yes_button.update(self.game.screen)
            self.no_button.change_color(pygame.mouse.get_pos())
            self.no_button.update(self.game.screen)

            self.game.check_events()
            self.check_input()
            self.blit_screen()
    def check_input(self):
        if self.game.ESC:
            self.run_display = False
        if self.game.MOUSE_CLICK_L:
            if self.yes_button.check_input(pygame.mouse.get_pos()):
                self.run_display = False
                next_play = PreGame(self.game)
                next_play.display_play()
            if self.no_button.check_input(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()   