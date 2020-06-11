class Player:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class Game:
    movements = {"a1": 0, "a2": 1, "a3": 2,
                 "b1": 3, "b2": 4, "b3": 5,
                 "c1": 6, "c2": 7, "c3": 8}
    turn = True

    def __init__(self):
        self.players = []
        self.board = [" "] * 9
        self.turn = 0

    @property
    def is_full(self):
        return len(self.players) == 2

    def join(self, *args):
        self.players.push(Player(*args))

    def log_board(self):
        pboard = "|".join(self.board[:3]) + "\n——————\n"
        pboard += "|".join(self.board[3:6]) + "\n——————\n"
        pboard += "|".join(self.board[6:])
        return pboard

    def log_start(self):
        return self.log_board()

    def log_turn(self):


    def check(self):
        # TODO: find a better way to check for three in a row
        check = [self.board[0:3], self.board[3:6], self.board[6:],
                 [self.board[0], self.board[3], self.board[6]],
                 [self.board[1], self.board[4], self.board[7]],
                 [self.board[2], self.board[5], self.board[8]],
                 [self.board[0], self.board[4], self.board[8]],
                 [self.board[2], self.board[4], self.board[6]]]
        for arr in check:
            if arr[:3] == ["x"] * 3:
                self.clear()
                return f"{self.players[0]} wins!"
            elif arr[:3] == ["o"] * 3:
                self.clear()
                return f"{self.players[1]} wins!"
        return ""
