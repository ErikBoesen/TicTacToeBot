class Player:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class Game:
    movements = {"a1": 0, "a2": 1, "a3": 2,
                 "b1": 3, "b2": 4, "b3": 5,
                 "c1": 6, "c2": 7, "c3": 8}
    PIECES = ["X", "O"]


    def __init__(self):
        self.players = []
        self.board = [" "] * 9
        self.turn = 0

    @property
    def is_full(self):
        return len(self.players) == 2

    def join(self, *args):
        self.players.push(Player(*args))

    # Methods for executing a turn

    def get_position(self, number: str):
        return ((ord(number[0]) - ord('a')) * 3) + (int(number[1]) - 1)

    def is_occupied(self, position: int) -> bool:
        return not self.board[position] == " "

    # Methods for outputting information in string form

    def log_board(self):
        with open("board.txt") as f:
            board = f.read()
        board = board % self.board
        return board

    def log_start(self):
        return (
            self.log_board() + '\n\n' +
            ("It is %s's turn (%s). To take a turn, say # followed by the number for the square to play in, like A1." % self.PIECES[self.turn], self.players[self.turn])
        )

    # Completion checking

    def winner(self):
        # TODO: find a better way to check for three in a row
        check = [self.board[0:3], self.board[3:6], self.board[6:],
                 [self.board[0], self.board[3], self.board[6]],
                 [self.board[1], self.board[4], self.board[7]],
                 [self.board[2], self.board[5], self.board[8]],
                 [self.board[0], self.board[4], self.board[8]],
                 [self.board[2], self.board[4], self.board[6]]]
        for arr in check:
            if arr[:3] == ["X"] * 3:
                return 0
            elif arr[:3] == ["O"] * 3:
                return 1
        return None
