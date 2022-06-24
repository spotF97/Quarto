from quarto.state import State
from quarto import player


GAMES = 10000

attr1 = 1
attr2 = 2
BOARD_SIZE = 4


class Game:
    def __init__(self, firstPlayer: player.Player, secondPlayer: player.Player):
        self.firstPlayer = firstPlayer
        self.secondPlayer = secondPlayer

    def play(self, n_games):

        for i in range(n_games):
            state = State()
            state.initialize()

            print(i)

            while True:

                print(state)

                if state.is_done():
                    if state.is_draw():
                        print("引き分け")
                    elif state.is_first_player() and state.is_lose():
                        print("後手の勝ち")
                    else:
                        print("先手の勝ち")

                    break

                if state.is_first_player():
                    print('先手')
                    action = self.firstPlayer.select_action(state)
                else:
                    print('後手')
                    action = self.secondPlayer.select_action(state)

                state = state.next(action)


def main():

    # first_player = player.MCTSPlayer(expand_base=10, simulation=100)
    first_player = player.HumanPlayer()
    second_player = player.RandomPlayer()
    second_player = player.MCTSPlayer(expand_base=10, simulation=100)
    n_games = 1

    game = Game(firstPlayer=first_player, secondPlayer=second_player)
    game.play(n_games)


if __name__ == '__main__':
    main()