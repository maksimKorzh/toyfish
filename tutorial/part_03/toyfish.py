import json
class Chess:
    def __init__(self, filename):
        with open(filename) as f:
            self.__dict__ = json.loads(f.read())
            self.board = list('         \n' * 2 + ' ' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in self.fen.split()[0].replace('/', '\n ')
            ]) + '\n' + '         \n' * 2)
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
                        if self.colors[captured_piece] == self.side ^ 1: break                        
                        if piece in 'PpNnKk': break
        return move_list

    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        if move['piece'] == 'P' and move['source'] in self.rank_7: self.board[move['target']] = 'Q'
        if move['piece'] == 'p' and move['source'] in self.rank_2: self.board[move['target']] = 'q'
        print(''.join([' ' + chess.pieces[p] for p in ''.join(chess.board)]), chess.side); input()
        self.side ^= 1
    
    def take_back(self, move):
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        print(''.join([' ' + chess.pieces[p] for p in ''.join(chess.board)]), chess.side); input()
        self.side ^= 1

chess = Chess('settings.json')
for move in chess.generate_moves():
    chess.make_move(move)
    chess.take_back(move)
#print(''.join([' ' + chess.pieces[p] for p in ''.join(chess.board)]), chess.side)
