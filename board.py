import functools


class Board:
    player_chars = ['-', 'X', 'O', '!', '?', '$', '@', '`', '=', '%']  # 9 players max, 0-field empty

    def __init__(self, dim=3, playeres=2, field=None):
        self.dim = dim
        self.players = playeres
        if field == None:
            self.field = [[0 for i in range(self.dim)] for j in range(self.dim)]
        else:
            self.field = [field[x].copy() for x in range(self.dim)]

        self.win_cells = []
        self.win_players = []
        self.gamewin = False

    def clear(self):
        self.field = [[0 for i in range(self.dim)] for j in range(self.dim)]
        self.win_cells = []
        self.gamewin = False

    def copy(self):
        return Board(self.dim, self.players, self.field)

        # other.win_cells = self.win_cells.copy()
        # other.win_players = self.win_players.copy()
        # other.gamewin = self.gamewin


    def showch(self, val, count, winner_cell):
        if winner_cell:
            return self.player_chars[val] * 5
        if count == 0 or count == 2:
            return '-----'
        return '-' + self.player_chars[val] * 3 + '-'

    def show(self):
        print()
        for y in range(self.dim):
            for count in range(3):
                for x in range(self.dim):
                    print(self.showch(self.field[x][y], count, (x, y) in self.win_cells), end='  ')
                print()
            print()

    def _move(self, x, y, pl):
        if not self.field[x][y]:
            self.field[x][y] = pl
            return True
        else:
            return False

    def inputmove(self, pl):
        try:
            s = input(f'Player {pl} ( {self.player_chars[pl]} ), make your move (X Y): ')
            ss = s.strip().split()
            if self._move(int(ss[0]) - 1, int(ss[1]) - 1, pl):
                print('Move successful')
                return True
            else:
                print('Cell is not empty')
                return False
        except:
            print('Incorrect input')
            return False

    def dirmove(self, x, y, pl):
        return self._move(x - 1, y - 1, pl)

    def checkwinner(self, pl):
        iswin = False
        if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][x] == pl for x in range(self.dim)]):
            iswin = True
            self.gamewin = True
            self.win_cells.extend([(x, x) for x in range(self.dim)])
        if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][self.dim - x - 1] == pl for x in range(self.dim)]):
            iswin = True
            self.gamewin = True
            self.win_cells.extend([(x, self.dim - x - 1) for x in range(self.dim)])
        for c in range(self.dim):
            if functools.reduce(lambda v1, v2: v1 and v2, [self.field[c][y] == pl for y in range(self.dim)]):
                iswin = True
                self.gamewin = True
                self.win_cells.extend([(c, y) for y in range(self.dim)])
            if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][c] == pl for x in range(self.dim)]):
                iswin = True
                self.gamewin = True
                self.win_cells.extend([(x, c) for x in range(self.dim)])
        if iswin:
            self.win_players.append(pl)
        return iswin

    def checkwinner_simple(self, pl):
        if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][x] == pl for x in range(self.dim)]):
            return True
        if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][self.dim - x - 1] == pl for x in range(self.dim)]):
            return True
        for c in range(self.dim):
            if functools.reduce(lambda v1, v2: v1 and v2, [self.field[c][y] == pl for y in range(self.dim)]):
                return True
            if functools.reduce(lambda v1, v2: v1 and v2, [self.field[x][c] == pl for x in range(self.dim)]):
                return True
        return False

    def checkwin_all_players(self, players):
        iswin = False
        for player in range(1, players + 1):
            iswin = self.checkwinner(player) or iswin
        return iswin

    def display_winners(self):
        if self.gamewin:
            print()
            print('We have our champion!!!')
            for winnner in self.win_players:
                print(f'Congratulation player {winnner} ( {self.player_chars[winnner]} ) !')

    def __getitem__(self, item):
        return self.field[item]

    def computer_move(self, comp_player, silent=False):
        max = None
        check_cells = {}
        if not silent:
            print('Recursive scores on all moves:')
        for x in range(self.dim):
            for y in range(self.dim):
                if self[x][y]==0:
                    if not silent: print(f'[{x+1}][{y+1}] -> ', end='')
                    if self.check_win_move(x,y,comp_player):
                        if not silent: print('WIN MOVE!!')
                        return [(x,y)]
                    check_cells[(x, y)] = self.check_move(x, y, comp_player)
                    if not silent: print(f'{check_cells[(x,y)]} ', end='\t')
                    if max==None or max < check_cells[(x, y)]:
                        max = check_cells[(x, y)]
        # if not silent:
        #     print('Results on moves:')
        #     print({(x+1,y+1):check_cells[(x,y)] for (x,y) in check_cells})
        best_cells = [(x, y) for (x, y) in check_cells if check_cells[(x, y)] == max]
        if not silent:
            print('\nBest results:')
            print([(x+1,y+1) for (x,y) in best_cells])
        return best_cells


    def check_win_move(self,x,y,pl):
        if self[x][y] != 0:
            return False
        check_board = self.copy()
        check_board[x][y] = pl
        return check_board.checkwinner_simple(pl)

    def check_move(self, x, y, pl):  # 2 player version
        deep_variant = 0
        if self[x][y] != 0:
            return 0
        check_board = self.copy()
        check_board[x][y] = pl
        if check_board.checkwinner_simple(pl):
            return self.dim
        other_pl = 1 if pl == 2 else 2
        value = 1
        other_win=False
        if deep_variant:
            # this variant dont work!
            best_other_cells = check_board.computer_move(other_pl, silent=True)
            for (x, y) in best_other_cells:
                if check_board[x][y] == 0:
                    recurtion_check_board = check_board.copy()
                    recurtion_check_board._move(x, y, other_pl)
                    if not recurtion_check_board.checkwinner_simple(other_pl):
                        for xx in range(self.dim):
                            for yy in range(self.dim):
                                if recurtion_check_board.check_win_move(xx, yy, pl):
                                    value += self.dim ** 2
                                else:
                                    value += recurtion_check_board.check_move(xx, yy, pl)
                    else:
                        value-=self.dim

        else:
            #   dump recursion
            for x in range(self.dim):
                for y in range(self.dim):
                    if check_board[x][y] == 0:
                        recurtion_check_board = check_board.copy()
                        recurtion_check_board._move(x, y, other_pl)
                        if not recurtion_check_board.checkwinner_simple(other_pl):
                            for xx in range(self.dim):
                                for yy in range(self.dim):
                                    if recurtion_check_board.check_win_move(xx, yy, pl):
                                        value+=self.dim**2
                                    else:
                                        value += recurtion_check_board.check_move(xx, yy, pl)
                        else:
                            return 0
        return value

    def full(self):
        return functools.reduce(lambda x, y: x and y, [self[x][y] != 0 for x in range(self.dim) for y in range(self.dim)])

    def __str__(self):
        return str(self.field)

