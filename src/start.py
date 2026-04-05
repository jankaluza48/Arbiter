from game import Game

def main():
    g = Game()

    while g.running:
        g.main_menu.display_menu()
        g.game_loop()