# coding: utf-8
import json
class Chess:
    def __init__(self, variant):
        with open(variant) as f:
            settings = json.loads(f.read())
            fen = settings['fen']
            row = settings['offset'] + 2
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
        board, directions = self.board, self.directions
        for square in range(len(board)):
            piece = board[square]
            if piece not in '.x\n' and piece.isupper():
                for piece_type, offsets in directions.items():
                    if piece == piece_type:
                        for offset in offsets:
                            target_square = square
                            while True:
                                target_square += offset
                                captured_piece = board[target_square]
                                if captured_piece == 'x': break
                                
                                board[target_square] = piece
                                board[square] = '.'
                                print(''.join(self.board)); input()
                                
                                board[target_square] = captured_piece
                                board[square] = piece
                                print(''.join(self.board)); input()
        
if __name__ == '__main__':
    chess = Chess('chess.json')
    chess.generate_moves()
    
