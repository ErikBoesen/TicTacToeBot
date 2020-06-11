class Player:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class Game:
    PIECES = ["X", "O"]

    def __init__(self):
        self.players = []
        self.board = [" "] * 9
        self.turn = 0

    @property
    def is_full(self):
        return len(self.players) == 2

    def join(self, name, user_id):
        for player in self.players:
            if player.user_id == user_id:
                return False
        self.players.append(Player(name, user_id))
        return True

    # Methods for executing a turn

    def is_valid_position(self, position: str):
        return len(position) == 2 and position[0] in "abc" and position[1] in "123"

    def get_index(self, position: str):
        return ((int(position[1]) - 1) * 3 + (ord(position[0]) - ord('a')))

    def is_occupied(self, index: int) -> bool:
        return not self.board[index] == " "

    def in_turn(self, user_id):
        return self.players[self.turn].user_id == user_id

    def take_turn(self, index: int):
        self.board[index] = self.PIECES[self.turn]
        self.turn = not self.turn

    # Methods for outputting information in string form

    def safe_spaces(self, text):
        return text.replace(" ", "\u2004")

    def log_board(self):
        with open("board.txt") as f:
            board = f.read()
        board = board % tuple(self.board)
        return self.safe_spaces(board)

    def log_turn(self):
        return (
            self.log_board() + '\n\n' +
            ("It is %s's turn (%s). To take a turn, say # followed by the position for the square to play in, like A1." % (self.PIECES[self.turn], self.players[self.turn].name))
        )

    def log_win(self, winner: int):
        return (
            self.log_board() + '\n\n' +
            ("🎉 %s (%s) wins! Say #start to play again." % (self.PIECES[winner], self.players[winner].name))
        )

    def log_tie(self):
        return (
            self.log_board() + '\n\n' +
            "It's a tie! Say #start to play again."
        )

    # Completion checking

    def tied(self):
        return all([is_occupied(i) for i in range(0, 9)])

    def winner(self):
        runs = [
            slice(0, 3), slice(3, 6), slice(6, 9),
            slice(0, 9, 3), slice(1, 9, 3), slice(2, 9, 3),
            # Diagonals
            slice(0, 9, 4), slice(2, 7, 2)
        ]
        for run in runs:
            if self.board[run] == [self.PIECES[0]] * 3:
                return 0
            if self.board[run] == [self.PIECES[1]] * 3:
                return 1
        return None
