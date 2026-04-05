from game import Game

g = Game()

while g.running:
    g.main_menu.display_menu()
    g.game_loop()