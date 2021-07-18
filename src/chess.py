# coding: utf-8
import json
class Chess:
    def __init__(self, variant):
        with open(variant) as f:
            settings = json.loads(f.read())
            self.__dict__ = settings
            start_fen = settings['start_fen']
            row = settings['offset'] + 2
            self.board = list((row * ' ' + '\n') * 2 + ' ' + ''.join([
                '.' * int(c) if c.isdigit() else c
                for c in start_fen.split()[0].replace('/', ' \n ')
            ]) + ' \n' + (row * ' ' + '\n') * 2)
            for piece, offsets in settings['directions'].items():
                directions = (
                    offsets.replace('N', str(-(row + 1)))
                           .replace('S', str(row + 1))
                           .replace('E', '1')
                           .replace('W', '-1')
                ).split()
                self.directions[piece] = [eval(d) for d in directions]
            self.N, self.S, self.E, self.W = -(row + 1), row + 1, 1, -1
    
    def rotate(self):
        self.board = list(''.join(self.board)[::-1].swapcase())
    
    def generate_moves(self):
        move_list = []
        for square in range(len(self.board)):
            piece = self.board[square]
            if piece not in ' .\n' and piece.isupper():
                for piece_type, offsets in self.directions.items():
                    if piece == piece_type:
                        for offset in offsets:
                            target_square = square
                            while True:
                                target_square += offset
                                captured_piece = self.board[target_square]
                                if captured_piece == ' ' or captured_piece.isupper(): break
                                if captured_piece == 'k': return []
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
                                if captured_piece.islower(): break
                                if piece in self.leapers: break
        return move_list
                                
    def make_move(self, move):
        self.board[move['target']] = move['piece']
        self.board[move['source']] = '.'
        if move['piece'] == 'P' and move['source'] in self.rank_7:
            self.board[move['target']] = 'Q'
        print(''.join(self.board)); input()
        self.rotate()
    
    def take_back(self, move):
        self.rotate()
        self.board[move['target']] = move['captured']
        self.board[move['source']] = move['piece']
        print(''.join(self.board)); input()
        
    def search(self, alpha, beta, depth):
        if depth == 0: self.evaluate()
        old_alpha = alpha
        temp_source = -1
        temp_target = -1
        for move in self.generate_moves():
            self.make_move(move)
            score = self.search(-beta, -alpha, depth - 1)
            self.take_back(move)
            self.best_source = move['source']
            self.best_target = move['target']
            if score >= beta: return beta
            if score > alpha:
                alpha = score
                temp_source = move['source']
                temp_target = move['target']
        if alpha != old_alpha:
            self.best_source = temp_source;
            self.best_target = temp_target;
        return alpha
    
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
        for move in self.generate_moves():
            self.make_move(move)
            self.take_back(move)
        
        

if __name__ == '__main__':
    chess = Chess('chess.json')
    chess.game_loop()
    