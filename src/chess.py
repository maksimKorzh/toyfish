# coding: utf-8
# %load chess.py
import json
class Chess:
    def __init__(self, variant):
        with open(variant) as f:
            settings = json.loads(f.read())
            start_fen = settings['start_fen']
            row = settings['offset'] + 2
            self.variant = settings['variant']
            self.leapers = settings['leapers']
            self.N, self.S, self.E, self.W = -(row + 1), row + 1, 1, -1
            self.rank_2 = settings['rank_2']
            self.rank_7 = settings['rank_7']
            self.board = list((row * 'x' + '\n') * 2 + 'x' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in start_fen.split()[0].replace('/', 'x\nx')
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
        self.board = list(''.join(self.board)[::-1].swapcase())
    
    def generate_moves(self):
        move_list = []
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in '.x\n' and piece.isupper():
                for piece_type, offsets in self.directions.items():
                    if piece == piece_type:
                        for offset in offsets:
                            target_square = square
                            while True:
                                target_square += offset
                                captured_piece = self.board[target_square]
                                if captured_piece == 'x' or captured_piece.isupper(): break
                                if self.variant == 'chess':
                                    if piece == 'P':
                                        if offset == self.directions['P'][0] and captured_piece != '.': break
                                        if offset in self.directions['P'][1: -1] and captured_piece == '.': break
                                        if offset == self.directions['P'][-1]:
                                            if square not in self.rank_2: break
                                            if self.board[target_square + self.S] != '.': break
                                            if captured_piece != '.': break
                                move_list.append({
                                    "source": square,
                                    "target": target_square,
                                    "piece": piece,
                                    "captured": captured_piece
                                })
                                if piece in self.leapers: break
        return move_list
                                
    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        print(''.join(self.board)); input()
        self.rotate()
    
    def take_back(self, move):
        self.rotate()
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        print(''.join(self.board)); input()
        
    def search(self, depth):
        if depth == 0: return
        move_list = self.generate_moves()
        for move in move_list:
            self.make_move(move)
            self.search(depth - 1)
            self.take_back(move)

if __name__ == '__main__':
    chess = Chess('chess.json')
    chess.search(2)
    
