# coding: utf-8
# %load chess.py
import json
class Chess:
    def __init__(self, variant):
        with open(variant) as f:
            settings = json.loads(f.read())
            fen = settings['fen']
            row = settings['offset'] + 2
            self.variant = settings['variant']
            self.leapers = settings['leapers']
            self.N, self.S = -(row + 1), row + 1
            self.E, self.W = 1, -1
            self.rank_2 = settings['rank_2']
            self.rank_7 = settings['rank_7']
            self.board = list((row * 'x' + '\n') * 2 + 'x' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in fen.split()[0].replace('/', 'x\nx')
            ]) + 'x\n' + (row * 'x' + '\n') * 2)
            self.directions = {}
            for piece, offsets in settings['directions'].items():
                directions = (
                    offsets.replace('N', str(-(row + 1)))
                           .replace('S', str(row + 1))
                           .replace('E', '1')
                           .replace('W', '-1')
                ).split()
                self.directions[piece] = [eval(d) for d in directions]
    
    def rotate(self):
        return list(''.join(self.board)[::-1].swapcase())
    
    def generate_moves(self):
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in '.x\n' and piece.isupper():
                for piece_type, offsets in self.directions.items():
                    if piece == piece_type:
                        for offset in offsets:
                            target_square = square
                            while True:
                                target_square += offset
                                captured = self.board[target_square]
                                if captured == 'x' or captured.isupper(): break
                                if self.variant == 'chess':
                                    if piece == 'P':
                                        if offset == self.directions['P'][0] and captured != '.': break
                                        if offset in self.directions['P'][1: -1] and captured == '.': break
                                        if offset == self.directions['P'][-1]:
                                            if square not in self.rank_2: break
                                            if self.board[target_square + self.S] != '.': break
                                            if captured != '.': break
                                        
                                      
                                self.board[target_square] = piece
                                self.board[square] = '.'
                                print(''.join(self.board)); input()
                                
                                self.board[target_square] = captured
                                self.board[square] = piece
                                print(''.join(self.board)); input()
                                
                                if piece in self.leapers: break
        
if __name__ == '__main__':
    chess = Chess('chess.json')
    chess.generate_moves()
    
