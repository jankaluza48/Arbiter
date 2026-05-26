from game import Game

"""spouštěcí soubor pro hru"""

def main():
    g = Game()

    while g.running:
        g.main_menu.display_menu()
        g.game_loop()

main()