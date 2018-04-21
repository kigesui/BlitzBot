class Move(object):
    MOVES = {}

    def __init__(self, name):
        self.name = name
        move_info = []
        if len(Move.MOVES) == 0:
            f = open("Pokemon_moves.csv", 'r')
            for move in f:
                move = move.strip()
                moveList = move.split(",")
                Move.MOVES[moveList[0]] = moveList  # The name of the move is the key while the rest of the
            f.close()

        # Finding the matching key in the dictionary, then assigning the list to a variable called moveInfo
        for key in Move.MOVES:
            if key.lower() == self.name.lower():
                move_info = Move.MOVES[key]

        if len(move_info) == 0:
            print('I can\'t recognize' + ' ' + self.name)
            return

        self.type = move_info[1]  # Move type
        self.power = int(move_info[2])  # Can be special, physical, or stat-changing

        # For in-battle calculations
        self.duration = float(move_info[3])  # Move's base damage
        self.energy = int(move_info[4])

    def __str__(self):
        msg = self.name + '\nType:' + self.type + '\nPower:' + str(self.power) + \
            '\nDuration:' + str(self.duration) + '\nEnergy:' + str(self.energy)

        return msg
