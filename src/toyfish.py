# coding: utf-8
#####################################
# Toyfish: YOUR FIRST CHESS PROGRAM #
# Variant: Simplified western chess #
#####################################

import json
class Chess:
    def __init__(self, variant):
        with open(variant) as f:
            self.__dict__ = json.loads(f.read())
            self.board = list('         \n' * 2 + ' ' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in self.fen.split()[0].replace('/', '\n ')
            ]) + '\n' +  '         \n' * 2)
            self.side = 0 if self.fen.split()[1] == 'w' else 1

    def generate_moves(self):
        move_list = []
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in ' .\n' and self.colors[piece] == self.side:
                print(piece, end=' ')

        return move_list          

    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        if move['piece'] == 'P' and move['source'] in self.rank_7:
            self.board[move['target']] = 'Q'
        print(''.join(chess.board), 'side:', chess.side); input()
        self.side ^= 1    

    def take_back(self, move):
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        print(''.join(chess.board), 'side:', chess.side); input()
        self.side ^= 1

    def search(self, depth):
        if depth == 0: return self.evaluate();
        best_score = -10000;
        for move in self.generate_moves():
            self.make_move(move)
            score = -self.search(depth - 1)
            self.take_back(move)
            if score > best_score:
                best_score = score
                self.best_source = move['source']
                self.best_target = move['target']
        return best_score

    def evaluate(self):
        score = 0
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in ' .\n':
                score += self.weights[piece]
                if piece.islower(): score -= self.pst[square]
                if piece.isupper(): score += self.pst[square]
        
        return score
    
    def game_loop(self):
        side = 0 if self.start_fen.split()[1] == 'w' else 1
        print(side)        
        while True:
            score = self.search(3)
            self.make_move({
                'source': self.best_source, 'target': self.best_target,
                'piece': self.board[self.best_source], 'captured': self.board[self.best_target]
            })
            side ^= 1
            if side: print(''.join(self.board[::-1]).swapcase())
            else: print(''.join(self.board))
            input()

if __name__ == '__main__':
    chess = Chess('settings.json')
    chess.generate_moves()
    
