###################################
#
#      Helper script to encode
#    game rules into piece codes
#
#                by
#
#         Code Monkey King
#
###################################

# rule of chess
rules = {
    "pieces": "PNBRQKpnbrqk",
    "directions": {
        "P": [10, 20, 9, 11],
        "N": [19, 21, 12, 8],
        "B": [11, 9],
        "R": [1, 10,],
        "Q": [1, 10, 11, 9],
        "K": [1, 10, 11, 9],
        "p": [10, 20, 9, 11],
        "n": [19, 21, 12, 8],
        "b": [11, 9],
        "r": [1, 10],
        "q": [1, 10, 11, 9],
        "k": [1, 10, 11, 9]
    },
    "double_offset": {
        "P": 1, "N": 1, "B": 0, "R": 0, "Q": 1, "K": 1,
        "p": 1, "n": 1, "b": 0, "r": 0, "q": 1, "k": 1,
    },
    "colors": {
        "P": 0, "N": 0, "B": 0, "R": 0, "Q": 0, "K": 0,
        "p": 1, "n": 1, "b": 1, "r": 1, "q": 1, "k": 1
    },
    "weights": {
        "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0,
        "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0
    },
}

# piece codes
codes = {
    "P": 0, "N": 0, "B": 0, "R": 0, "Q": 0, "K": 0,
    "p": 0, "n": 0, "b": 0, "r": 0, "q": 0, "k": 0,
}

# encode chess rules to piece codes
print('Encoding pieces...')
for piece in rules['pieces']:
    for offset in range(4 if rules['double_offset'][piece] else 2):
        codes[piece] <<= 5
        codes[piece] |= rules['directions'][piece][offset]
    codes[piece] <<= 1
    codes[piece] |= rules['double_offset'][piece]
    codes[piece] <<= 4
    codes[piece] |= rules['weights'][piece]
    codes[piece] <<= 1
    codes[piece] |= rules['colors'][piece]
    codes[piece] <<= 7
    codes[piece] |= ord(piece)
    print(piece, codes[piece])

# decode chess rules from piece codes
print('\nDecoding pieces...')
for piece in codes.values():
    print(chr(piece & 127),
         (piece >> 7) & 1,
         (piece >> (7 + 1)) & 15,
         (piece >> (7 + 1 + 4) & 1),
         end=' ')
    double_offset = piece >> (7 + 1 + 4) & 1
    directions = piece >> (7 + 1 + 4 + 1)
    for offset in range(4 if double_offset else 2):
        print(directions & 31, end=' ')
        directions >>= 5
    print()

