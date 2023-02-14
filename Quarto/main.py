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


class HillClimberPlayer(Player):
    """Hill Climber player"""

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.__quarto = quarto
        

    def choose_piece(self) -> int:

        def pieceToindex(piece):
            binary = piece.binary
            piece_index = 0
            for i in range(4):
                piece_index += binary[i] * (2**i)
            return piece_index
    
        def evaluateChoose(piece_index):
            tmp = deepcopy(self.__quarto)
            score = 0
            n = 0
            if tmp.select(piece_index):
                score = float('-inf')
                for x in range(4):
                    for y in range(4):
                        s, high, coloured, solid, square = self.evaluatePlace(x, y, piece_index)
                        #if with the considered piece index the opponent has the chance to win in this round of the game, the piece index will be assigned the least score
                        if s == 4:
                            score = -1
                            return score, n
                        if s > score:
                            score = s
                        if score == 3:
                            #in case of score = 3, n is the number of the same attributes of the considered elements
                            n = high + coloured + solid + square

            return score, n

        def tweakChoose(piece: Piece):
            if random.random() < 0.7:
                r = random.randint(0, 3)
                if r == 0:
                    new_piece = Piece(not piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE)
                elif r == 1:
                    new_piece = Piece(piece.HIGH, not piece.COLOURED, piece.SOLID, piece.SQUARE)
                elif r == 2:
                    new_piece = Piece(piece.HIGH, piece.COLOURED, not piece.SOLID, piece.SQUARE)
                else:
                    new_piece = Piece(piece.HIGH, piece.COLOURED, piece.SOLID, not piece.SQUARE)
                return pieceToindex(new_piece)

            return pieceToindex(piece)

        board = self.get_game().get_board_status()
        current_piece = Piece(random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1))
        while True:
            current_piece_index = pieceToindex(current_piece)
            if current_piece_index not in board:
                break
            else:
                current_piece = Piece(random.randint(0, 1), random.randint(0, 1), random.randint(0, 1),
                                      random.randint(0, 1))
                
        useless_steps = 0
        while useless_steps < 5:
            useless_steps += 1
            candidate_piece_index = tweakChoose(current_piece)
            e1, n1 = evaluateChoose(current_piece_index)
            e2, n2 = evaluateChoose(candidate_piece_index)
            if e2 > e1:
                useless_steps = 0
                current_piece_index = candidate_piece_index
            #if the candidate piece index and the current piece index have the same evaluation equal to 3 and the number of the same attributes of the considered elements is greater for the candidate piece index, we choose the candidate piece index because this increses the chance that in the next round of the game, the opponent will have to choose one of the piece indexes for us to place that will make us win the game
            elif e2 == e1 and e1 == 3 and n2 > n1:
                useless_steps = 0
                current_piece_index = candidate_piece_index
                
        return current_piece_index

    def evaluatePlace(self, x, y, piece_index = None):
        tmp = deepcopy(self.__quarto)
        if piece_index != None:
            tmp.select(piece_index)
        if tmp.place(x, y):
            if tmp.check_finished():
                return 4, False, False, False, False
            else:
                #checking elements on the same row
                score = 1
                score1 = 1
                score2 = 1
                score3 = 1
                score4 = 1
                n = 1
                high = False
                coloured = False
                solid = False
                square = False
                for i in range(1,4):
                    k = (x + i) % 4
                    if tmp._board[y, k] != -1:
                        n += 1
                        if tmp._Quarto__pieces[tmp._board[y, k]].HIGH == tmp._Quarto__pieces[tmp._board[y, x]].HIGH:
                            score1 += 1
                        if tmp._Quarto__pieces[tmp._board[y, k]].COLOURED == tmp._Quarto__pieces[tmp._board[y, x]].COLOURED:
                            score2 += 1
                        if tmp._Quarto__pieces[tmp._board[y, k]].SOLID == tmp._Quarto__pieces[tmp._board[y, x]].SOLID:
                            score3 += 1
                        if tmp._Quarto__pieces[tmp._board[y, k]].SQUARE == tmp._Quarto__pieces[tmp._board[y, x]].SQUARE:
                            score4 += 1

                score = max(score, score1, score2, score3, score4)

                if score < n:
                    score = 0

                if score == 3:
                    if score == score1:
                        high = True
                    if score == score2:
                        coloured = True
                    if score == score3:
                        solid = True
                    if score == score4:
                        square = True
                
                if score == 4:
                    return score, False, False, False, False
                
                #checking elements on the same column
                score1 = 1
                score2 = 1
                score3 = 1
                score4 = 1
                n = 1
                for i in range(1,4):
                    k = (y + i) % 4
                    if tmp._board[k, x] != -1:
                        n += 1
                        if tmp._Quarto__pieces[tmp._board[k, x]].HIGH == tmp._Quarto__pieces[tmp._board[y, x]].HIGH:
                            score1 += 1
                        if tmp._Quarto__pieces[tmp._board[k, x]].COLOURED == tmp._Quarto__pieces[tmp._board[y, x]].COLOURED:
                            score2 += 1
                        if tmp._Quarto__pieces[tmp._board[k, x]].SOLID == tmp._Quarto__pieces[tmp._board[y, x]].SOLID:
                            score3 += 1
                        if tmp._Quarto__pieces[tmp._board[k, x]].SQUARE == tmp._Quarto__pieces[tmp._board[y, x]].SQUARE:
                            score4 += 1

                scoreNew = max(score1, score2, score3, score4)

                if scoreNew < n:
                    scoreNew = 0
                
                if scoreNew == 3:
                    high = False
                    coloured = False
                    solid = False
                    square = False
                    if score == score1:
                        high = True
                    if score == score2:
                        coloured = True
                    if score == score3:
                        solid = True
                    if score == score4:
                        square = True

                if scoreNew == 4:
                    return scoreNew, False, False, False, False
                
                if scoreNew > score:
                    score = scoreNew
                
                #checking elements on the same diagonal in case of the considered place on the main diagonal
                if x == y:
                    score1 = 1
                    score2 = 1
                    score3 = 1
                    score4 = 1
                    n = 1
                    for i in range(1, 4):
                        k = (x + i) % 4
                        if tmp._board[k, k] != -1:
                            n += 1
                            if tmp._Quarto__pieces[tmp._board[k, k]].HIGH == tmp._Quarto__pieces[tmp._board[y, x]].HIGH:
                                score1 += 1
                            if tmp._Quarto__pieces[tmp._board[k, k]].COLOURED == tmp._Quarto__pieces[tmp._board[y, x]].COLOURED:
                                score2 += 1
                            if tmp._Quarto__pieces[tmp._board[k, k]].SOLID == tmp._Quarto__pieces[tmp._board[y, x]].SOLID:
                                score3 += 1
                            if tmp._Quarto__pieces[tmp._board[k, k]].SQUARE == tmp._Quarto__pieces[tmp._board[y, x]].SQUARE:
                                score4 += 1
                    
                    scoreNew = max(score1, score2, score3, score4)

                    if scoreNew < n:
                        scoreNew = 0

                    if scoreNew == 3:
                        high = False
                        coloured = False
                        solid = False
                        square = False
                        if score == score1:
                            high = True
                        if score == score2:
                            coloured = True
                        if score == score3:
                            solid = True
                        if score == score4:
                            square = True
                
                    if scoreNew == 4:
                        return scoreNew, False, False, False, False
                    
                    if scoreNew > score:
                        score = scoreNew

                #checking elements on the same diagonal in case of the considered place on the secondary diagonal
                if x + y == 3:   
                    score1 = 1
                    score2 = 1
                    score3 = 1
                    score4 = 1
                    n = 1
                    for i in range(1, 4):
                        r = (y + i) % 4
                        k = 3 - r
                        if tmp._board[r, k] != -1:
                            n += 1
                            if tmp._Quarto__pieces[tmp._board[r, k]].HIGH == tmp._Quarto__pieces[tmp._board[y, x]].HIGH:
                                score1 += 1
                            if tmp._Quarto__pieces[tmp._board[r, k]].COLOURED == tmp._Quarto__pieces[tmp._board[y, x]].COLOURED:
                                score2 += 1
                            if tmp._Quarto__pieces[tmp._board[r, k]].SOLID == tmp._Quarto__pieces[tmp._board[y, x]].SOLID:
                                score3 += 1
                            if tmp._Quarto__pieces[tmp._board[r, k]].SQUARE == tmp._Quarto__pieces[tmp._board[y, x]].SQUARE:
                                score4 += 1

                    scoreNew = max(score1, score2, score3, score4)

                    if scoreNew < n:
                        scoreNew = 0

                    if scoreNew == 3:
                        high = False
                        coloured = False
                        solid = False
                        square = False
                        if score == score1:
                            high = True
                        if score == score2:
                            coloured = True
                        if score == score3:
                            solid = True
                        if score == score4:
                            square = True

                    if scoreNew > score:
                        score = scoreNew
                            
                return score, high, coloured, solid, square

        return 0, False, False, False, False

    def place_piece(self) -> tuple[int, int]:

        def tweakPlace(x, y):
            if random.random() < 0.7:
                r = random.randint(0, 1)
                t = random.randint(0, 3)
                if r == 0:
                    return t, y
                else:
                    return x, t
            return x, y

        current_x = random.randint(0, 3)
        current_y = random.randint(0, 3)
        useless_steps = 0
        while useless_steps < 5:
            useless_steps += 1
            candidate_x, candidate_y = tweakPlace(current_x, current_y)
            e1, _, _, _, _ = self.evaluatePlace(current_x, current_y)
            e2, _, _, _, _ = self.evaluatePlace(candidate_x, candidate_y)
            if e2 > e1:
                useless_steps = 0
                current_x = candidate_x
                current_y = candidate_y
        return current_x, current_y


def main():
    win = 0
    for i in range(100):
        game = Quarto()
        game.set_players((HillClimberPlayer(game), RandomPlayer(game)))
        winner = game.run()
        logging.warning(f"main: Winner: player {winner}")
        if winner == 0:
            win += 1
    logging.warning(f"HillClimberPlayer won {win} games as the first player")

    win = 0
    for i in range(100):
        game = Quarto()
        game.set_players((RandomPlayer(game), HillClimberPlayer(game)))
        winner = game.run()
        logging.warning(f"main: Winner: player {winner}")
        if winner == 1:
            win += 1
    logging.warning(f"HillClimberPlayer won {win} games as the second player")


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