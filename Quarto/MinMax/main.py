# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
from quarto.objects import *
from copy import deepcopy


class RandomPlayer(Player):
    """Random player"""

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)


class MinMaxPlayer(Player):
    """Evolved player"""

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.__quarto = quarto

    def minmaxChoose(self, quarto: Quarto, depth, isMaximizing, alpha, beta):
        if isMaximizing:
            bestVal = float('-inf')
            bestP = -1
            if depth > 4:
                return bestP, bestVal
            steps = 0
            for p in range(16):
                tmp = deepcopy(quarto)
                if tmp.select(p):
                    steps += 1
                    x, y, val = self.minmaxPlace(tmp, depth+1, False, alpha, beta)
                    if val > bestVal:
                        bestVal = val
                        bestP = p
                    alpha = max(alpha, bestVal)
                    if beta <= alpha or steps > 3:
                        return bestP, bestVal
                      
            return bestP, bestVal
        
        else :
            bestVal = float('inf')
            bestP = -1
            if depth > 4:
                return bestP, bestVal
            steps = 0
            for p in range(16):
                tmp = deepcopy(quarto)
                if tmp.select(p):
                    steps += 1
                    x, y, val = self.minmaxPlace(tmp, depth+1, True, alpha, beta)
                    if val < bestVal:
                        bestVal = val
                        bestP = p
                    beta = min(beta, bestVal)
                    if beta <= alpha or steps > 3:
                        return bestP, bestVal
                    
            return bestP, bestVal

    def choose_piece(self) -> int:
        p, _ = self.minmaxChoose(self.__quarto, 0, True, float('-inf'), float('inf'))
        return p

    def minmaxPlace(self, quarto: Quarto, depth, isMaximizing, alpha, beta):
        if isMaximizing:
            bestVal = float('-inf')
            bestX = -1
            bestY = -1
            if depth > 4:
                return bestX, bestY, bestVal
            steps = 0
            for x in range(4):
                for y in range(4):
                    tmp = deepcopy(quarto)
                    if tmp.place(x, y):
                        steps += 1
                        if tmp.check_finished():
                            return x, y, 1
                        p, val = self.minmaxChoose(tmp, depth+1, False, alpha, beta)
                        if val > bestVal:
                            bestVal = val
                            bestX = x
                            bestY = y
                        alpha = max(alpha, bestVal)
                        if beta <= alpha or steps > 3:
                            return bestX, bestY, bestVal
                
                return bestX, bestY, bestVal
        
        else :
            bestVal = float('inf')
            bestX = -1
            bestY = -1
            if depth > 4:
                return bestX, bestY, bestVal
            steps = 0
            for x in range(4):
                for y in range(4):
                    tmp = deepcopy(quarto)
                    if tmp.place(x, y):
                        steps += 1
                        if tmp.check_finished():
                            return x, y, 1
                        p, val = self.minmaxChoose(tmp, depth+1, True, alpha, beta)
                        if val < bestVal:
                            bestVal = val
                            bestX = x
                            bestY = y
                        beta = min(beta, bestVal)
                        if beta <= alpha or steps > 3:
                            return bestX, bestY, bestVal
                
                return bestX, bestY, bestVal
                
        

    def place_piece(self) -> tuple[int, int]:
        x, y, _ = self.minmaxPlace(self.__quarto, 0, True, float('-inf'), float('inf'))
        return x, y


def main():
    game = Quarto()
    game.set_players((MinMaxPlayer(game), RandomPlayer(game)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()