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
                for offset in self.directions[piece]:
                    target_square = square
                    while True:
                        target_square += offset
                        captured_piece = self.board[target_square]
                        if captured_piece in ' \n': break
                        if self.colors[captured_piece] == self.side: break
                        if piece in 'Pp' and offset in [9, 11, -9, -11] and captured_piece == '.': break
                        if piece in 'Pp' and offset in [10, 20, -10, -20] and captured_piece != '.': break
                        if piece == 'P' and offset == -20:
                            if square not in self.rank_2: break
                            if self.board[square - 10] != '.': break
                        if piece == 'p' and offset == 20:
                            if square not in self.rank_7: break
                            if self.board[square + 10] != '.': break
                        move_list.append({
                            'source': square, 'target': target_square,
                            'piece': piece, 'captured': captured_piece
                        })
                        if self.colors[captured_piece] == (self.side ^ 1): break
                        if piece in 'PpNnKk': break
        return move_list          

    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        #if move['piece'] == 'P' and move['source'] in self.rank_7:
        #    self.board[move['target']] = 'Q'
        #print(''.join(chess.board), 'side:', chess.side); input()
        self.side ^= 1    

    def take_back(self, move):
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        #print(''.join(chess.board), 'side:', chess.side); input()
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
        
        return -score if self.side else score
    
    def game_loop(self):
        while True:
            score = self.search(2)
            self.make_move({
                'source': self.best_source, 'target': self.best_target,
                'piece': self.board[self.best_source], 'captured': self.board[self.best_target]
            })
            print(''.join(chess.board), 'side:', self.side)
            input()

if __name__ == '__main__':
    chess = Chess('settings.json')
    print(''.join(chess.board), 'side:', chess.side)
    score = chess.search(4)
    print(chess.best_source, chess.best_target)
    #chess.game_loop()
    
