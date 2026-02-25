import os; os.environ['SDL_VIDEODRIVER'] = 'cocoa'

import math

# 1. Setup & Constants
BOARD_SIZE = 8
SQUARE = 80
SIDEBAR = 200
WIDTH = (BOARD_SIZE * SQUARE) + SIDEBAR
HEIGHT = (BOARD_SIZE * SQUARE) + 80

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (170, 210, 110, 150)


# -----------------------------------
# Game State Initialization
# -----------------------------------
def reset_game():
    global board, turn, selected, game_over, winner, white_time, black_time
    global history, moved_pieces, en_passant_target

    turn = "white"
    selected = None
    game_over = False
    winner = ""
    white_time = 300
    black_time = 300
    history = []
    moved_pieces = set()
    en_passant_target = None

    board = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp"] * 8,
        [".."] * 8,
        [".."] * 8,
        [".."] * 8,
        [".."] * 8,
        ["wp"] * 8,
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]


# Run once at startup
reset_game()


# -----------------------------------
# Logic Helpers
# -----------------------------------

def path_clear(sr, sc, tr, tc):
    dr, dc = tr - sr, tc - sc
    steps = max(abs(dr), abs(dc))
    if steps == 0: return True
    step_r, step_c = dr // steps, dc // steps
    for i in range(1, steps):
        if board[sr + i * step_r][sc + i * step_c] != "..":
            return False
    return True


def can_piece_reach_basic(sr, sc, tr, tc):
    p = board[sr][sc][1]
    dr, dc = tr - sr, tc - sc
    if p == "p":
        color = board[sr][sc][0]
        direction = -1 if color == "w" else 1
        return abs(dc) == 1 and dr == direction
    if p == "r": return (sr == tr or sc == tc) and path_clear(sr, sc, tr, tc)
    if p == "b": return abs(dr) == abs(dc) and path_clear(sr, sc, tr, tc)
    if p == "q": return (sr == tr or sc == tc or abs(dr) == abs(dc)) and path_clear(sr, sc, tr, tc)
    if p == "n": return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]
    if p == "k": return max(abs(dr), abs(dc)) == 1
    return False


def is_square_attacked(row, col, by_color):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = board[r][c]
            if p != ".." and p[0] == by_color:
                if can_piece_reach_basic(r, c, row, col):
                    return True
    return False


def find_king(color_name):
    char = "w" if color_name == "white" else "b"
    for r in range(8):
        for c in range(8):
            if board[r][c] == char + "k":
                return (r, c)
    return None


def is_in_check(color_name):
    king_pos = find_king(color_name)
    if not king_pos: return False
    opponent = "b" if color_name == "white" else "w"
    return is_square_attacked(king_pos[0], king_pos[1], opponent)


# -----------------------------------
# Special Moves Logic
# -----------------------------------

def can_castle(color, side):
    if is_in_check(color): return False
    r = 7 if color == "white" else 0
    if (r, 4) in moved_pieces: return False

    rook_col = 7 if side == "king" else 0
    if (r, rook_col) in moved_pieces or board[r][rook_col][1] != 'r': return False

    cols = [5, 6] if side == "king" else [1, 2, 3]
    for c in cols:
        if board[r][c] != "..": return False
        if c in [2, 3, 5, 6]:
            if is_square_attacked(r, c, "b" if color == "white" else "w"): return False
    return True


def valid_move(sr, sc, tr, tc):
    piece = board[sr][sc]
    target = board[tr][tc]
    if piece == "..": return False
    color = piece[0]
    p_type = piece[1]

    if target != ".." and target[0] == color: return False

    dr, dc = tr - sr, tc - sc
    legal = False

    if p_type == "p":
        direction = -1 if color == "w" else 1
        start_row = 6 if color == "w" else 1
        if dc == 0 and dr == direction and target == "..":
            legal = True
        elif dc == 0 and sr == start_row and dr == 2 * direction and board[sr + direction][
            sc] == ".." and target == "..":
            legal = True
        elif abs(dc) == 1 and dr == direction and (target != ".." or (tr, tc) == en_passant_target):
            legal = True
    elif p_type == "r":
        legal = (sr == tr or sc == tc) and path_clear(sr, sc, tr, tc)
    elif p_type == "b":
        legal = abs(dr) == abs(dc) and path_clear(sr, sc, tr, tc)
    elif p_type == "q":
        legal = (sr == tr or sc == tc or abs(dr) == abs(dc)) and path_clear(sr, sc, tr, tc)
    elif p_type == "n":
        legal = (abs(dr), abs(dc)) in [(2, 1), (1, 2)]
    elif p_type == "k":
        if max(abs(dr), abs(dc)) == 1:
            legal = True
        elif sr == tr and abs(dc) == 2:
            legal = can_castle("white" if color == "w" else "black", "king" if tc > sc else "queen")

    if not legal: return False

    original_target = board[tr][tc]
    board[tr][tc], board[sr][sc] = board[sr][sc], ".."
    in_check = is_in_check("white" if color == "w" else "black")
    board[sr][sc], board[tr][tc] = board[tr][tc], original_target

    return not in_check


def has_legal_moves(color_name):
    char = "w" if color_name == "white" else "b"
    for r in range(8):
        for c in range(8):
            if board[r][c].startswith(char):
                for tr in range(8):
                    for tc in range(8):
                        if valid_move(r, c, tr, tc): return True
    return False


# -----------------------------------
# Input & Updates
# -----------------------------------

def on_key_down(key):
    if key == keys.R:
        reset_game()


def on_mouse_down(pos):
    global selected, turn, game_over, winner, en_passant_target
    if game_over or pos[0] > 640 or pos[1] > 640: return

    c, r = int(pos[0] // SQUARE), int(pos[1] // SQUARE)

    if selected is None:
        p = board[r][c]
        if p != ".." and ((turn == "white" and p[0] == "w") or (turn == "black" and p[0] == "b")):
            selected = (r, c)
    else:
        sr, sc = selected
        if valid_move(sr, sc, r, c):
            piece = board[sr][sc]
            history.append(f"{piece[1].upper()}{chr(97 + c)}{8 - r}")
            if len(history) > 18: history.pop(0)

            if piece[1] == "p" and (r, c) == en_passant_target:
                board[sr][c] = ".."

            if piece[1] == "k" and abs(sc - c) == 2:
                rook_old_c = 7 if c > sc else 0
                rook_new_c = 5 if c > sc else 3
                board[r][rook_new_c] = board[r][rook_old_c]
                board[r][rook_old_c] = ".."

            board[r][c], board[sr][sc] = board[sr][sc], ".."
            moved_pieces.add((sr, sc))

            if piece[1] == "p" and abs(r - sr) == 2:
                en_passant_target = (sr + (r - sr) // 2, sc)
            else:
                en_passant_target = None

            if piece == "wp" and r == 0: board[r][c] = "wq"
            if piece == "bp" and r == 7: board[r][c] = "bq"

            turn = "black" if turn == "white" else "white"
            if not has_legal_moves(turn):
                game_over = True
                winner = ("black" if turn == "white" else "white") if is_in_check(turn) else "draw"

        selected = None


def update():
    global white_time, black_time, game_over, winner
    if game_over: return
    if turn == "white":
        white_time -= 1 / 60
        if white_time <= 0: (game_over, winner) = (True, "black")
    else:
        black_time -= 1 / 60
        if black_time <= 0: (game_over, winner) = (True, "white")


# -----------------------------------
# Drawing
# -----------------------------------

def draw():
    screen.clear()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            rect = Rect(c * SQUARE, r * SQUARE, SQUARE, SQUARE)
            screen.draw.filled_rect(rect, LIGHT if (r + c) % 2 == 0 else DARK)
            if selected and valid_move(selected[0], selected[1], r, c):
                screen.draw.filled_circle(rect.center, 8, HIGHLIGHT)

    if selected:
        # Create the rectangle area
        sel_rect = Rect(selected[1] * SQUARE, selected[0] * SQUARE, SQUARE, SQUARE)

        # Draw the box using the basic method (no thickness or width keyword needed)
        screen.draw.rect(sel_rect, (0, 255, 0))

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece_code = board[r][c]
            if piece_code != "..":
                try:
                    screen.blit(piece_code, (c * SQUARE, r * SQUARE))
                except:
                    color = "white" if piece_code[0] == "w" else "black"
                    screen.draw.filled_circle((c * SQUARE + 40, r * SQUARE + 40), 30, color)
                    screen.draw.text(piece_code[1].upper(), center=(c * SQUARE + 40, r * SQUARE + 40), color="red")

    screen.draw.filled_rect(Rect(640, 0, SIDEBAR, 640), (40, 40, 40))
    screen.draw.text("HISTORY", (650, 20), color="gold", fontsize=25)
    for i, move in enumerate(history):
        screen.draw.text(f"{i + 1}. {move}", (660, 55 + i * 28), color="white", fontsize=20)

    screen.draw.filled_rect(Rect(0, 640, WIDTH, 80), (20, 20, 20))
    w_m, w_s = divmod(max(0, int(white_time)), 60)
    b_m, b_s = divmod(max(0, int(black_time)), 60)
    screen.draw.text(f"TURN: {turn.upper()}", (20, 675), color="white", fontsize=25)
    screen.draw.text(f"W {w_m:02}:{w_s:02} | B {b_m:02}:{b_s:02}", (320, 675), color="white", fontsize=25)
    screen.draw.text("Press 'R' to Reset", (650, 610), color="gray", fontsize=18)

    if game_over:
        txt = "STALEMATE" if winner == "draw" else f"{winner.upper()} WINS"
        screen.draw.text(txt, center=(320, 320), fontsize=70, color="yellow")
        screen.draw.text("Press R to play again", center=(320, 380), fontsize=30, color="white")

import pgzrun
pgzrun.go()
