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
                        if captured_piece in 'Kk': return []
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
        if move['piece'] == 'P' and move['source'] in self.rank_7: self.board[move['target']] = 'Q'
        if move['piece'] == 'p' and move['source'] in self.rank_2: self.board[move['target']] = 'q'
        self.side ^= 1    

    def take_back(self, move):
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        self.side ^= 1

    def search(self, depth):
        if depth == 0: return self.evaluate();
        best_score = -10000;
        best_source, best_target = -1, -1
        move_list = self.generate_moves()
        if not len(move_list): return 10000
        for move in move_list:
            self.make_move(move)
            score = -self.search(depth - 1)
            self.take_back(move)
            if score > best_score:
                best_score = score
                best_source = move['source']
                best_target = move['target']
        self.best_source = best_source
        self.best_target = best_target
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
        print(''.join([' ' + self.pieces[p] for p in chess.board]))
        while True:
            raw = input('   Your move: ')
            if len(raw) < 4: continue
            user_source = self.coordinates.index(raw[0] + raw[1])
            user_target = self.coordinates.index(raw[2] + raw[3])
            self.make_move({
                'source': user_source, 'target': user_target,
                'piece': self.board[user_source], 'captured': self.board[user_target]
            })
            print(''.join([' ' + self.pieces[p] for p in chess.board]))
            score = self.search(3)
            self.make_move({
                'source': self.best_source, 'target': self.best_target,
                'piece': self.board[self.best_source], 'captured': self.board[self.best_target]
            })
            print(''.join([' ' + self.pieces[p] for p in chess.board]))
            if abs(score) == 10000:
                print('   Checkmate!')
                break

if __name__ == '__main__':
    chess = Chess('settings.json')
    chess.game_loop()
    
