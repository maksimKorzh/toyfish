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
            
if __name__ == '__main__':
    chess = Chess('chess.json')
    print(''.join(chess.board))
    
