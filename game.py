import objects as ob

class Game:
    def __init__(self) -> None:
        #all groups
        self.black_figures = ob.FigureGroup()
        self.white_figures = ob.FigureGroup()
        self.active_figures = ob.FigureGroup()
        self.pressed_figures = ob.FigureGroup()
        self.jump_figures = ob.FigureGroup()
        self.tiles = ob.TileGroup()
        self.jump_tiles = ob.TileGroup()

        #states of the game
        self.end_menu = None
        self.end = False
        self.pause_menu = ob.Menu(False, '', ob.Button(200, 300, 'Replay', 'assets/replay_button.png'), ob.Button(400, 300,'Quit', 'assets/quit_button.png'))
        self.pause = False
        self.quit = False

        #general game info
        self.screen_size = (800, 800)

        self.array = self._initArr()
        self.player = 'White'

    def _initArr(self):
        arr = [[None for _ in range(8)] for _ in range(8)]
        
        for col in range(8):
            for box in range(8):
                if col % 2==0:
                    if box == 1:
                        arr[col][box] = ob.BlackFigure(col*100,box*100, self.black_figures)
                    elif box == 5 or box == 7:
                        arr[col][box] = ob.WhiteFigure(col*100, box*100, self.white_figures)
                else:
                    if box == 0 or box == 2:
                        arr[col][box] = ob.BlackFigure(col*100,box*100, self.black_figures)
                    elif box == 6:
                        arr[col][box] = ob.WhiteFigure(col*100, box*100, self.white_figures)


        self.white_figures.add_figures_to(self.active_figures)
        self.active_figures.set_active(True)
        return arr
    
    def move_in_array(self, pre_pos, new_pos):
        figure = self.array[pre_pos[0]][pre_pos[1]]
        if figure is not None:
            self.array[pre_pos[0]][pre_pos[1]] = None
            self.array[new_pos[0]][new_pos[1]] = figure

    def erase_in_array(self, x, y):
        self.array[x][y] = None
    
    def delete_tiles(self):
        self.tiles.empty()
        self.jump_tiles.empty()
    
    # search for jump (and add figures them to group jump_figures) and possible moves
    def search_moves_in_array(self, group):
        can_play = False #returns if player is able to play
        for figure in group.sprites():
            jump, free_figure = figure.search_for_play(False, self)
            if free_figure:
                can_play = free_figure
            if jump:
                self.jump_figures.add(figure)
        return can_play

    def switch_player(self):
        self.active_figures.set_active(False)
        self.active_figures.empty()
        self.jump_figures.set_active(False)
        self.jump_figures.empty()

        if self.player == 'White':
            self.player = 'Black'
            can_continue = self.search_moves_in_array(self.black_figures)
            if can_continue:
                if not self.jump_figures.sprites():
                    self.black_figures.add_figures_to(self.active_figures)
                    self.active_figures.set_active(True)
                else:
                    self.jump_figures.set_active(True)
            else:
                self.end_game('White')
        else:
            self.player = 'White'
            can_continue = self.search_moves_in_array(self.white_figures)
            if can_continue:
                if not self.jump_figures.sprites():
                    self.white_figures.add_figures_to(self.active_figures)
                    self.active_figures.set_active(True)
                else:
                    self.jump_figures.set_active(True)
            else:
                self.end_game('Black')
        
    # checks if figure can jump again
    def continue_playing(self, figure):
        jump, _ = figure.search_for_play(False, self)
        if jump:
            #erase jump figures, when there were more of them
            self.jump_figures.empty()
            self.jump_figures.add(figure)
        else:
            self.switch_player()
    
    #move figures between pressed and their normal group
    def set_pressed(self, figure, bool):
        if bool:
            self.pressed_figures.add(figure)
            self.active_figures.remove(figure)
        else:
            self.active_figures.add(figure)
            self.pressed_figures.remove(figure)
        self.active_figures.set_active(not bool)
        self.pressed_figures.set_active(bool)

    def valid_indexes(self, x, y):
        return x in range(self.screen_size[0]) and y in range(self.screen_size[1])
    
    def end_game(self, winner):
        self.end = True
        self.end_menu = ob.Menu(True, winner, ob.Button(200, 300, 'Replay', 'assets/replay_button.png'), ob.Button(400, 300,'Quit', 'assets/quit_button.png'))
    
    def reset_game(self):
        self.black_figures = ob.FigureGroup()
        self.white_figures = ob.FigureGroup()
        self.active_figures = ob.FigureGroup()
        self.pressed_figures = ob.FigureGroup()
        self.jump_figures = ob.FigureGroup()
        self.tiles = ob.TileGroup()
        self.jump_tiles = ob.TileGroup()

        self.end_menu = None
        self.end = False
        self.pause = False

        self.array = self._initArr()
        self.player = 'White'

    def quit_game(self):
        self.quit = True
    
    def pause_game(self):
        self.pause = not self.pause
        
    def _print_game(self):
        print('+--------+')
        for col in range(8):
            print('|', end='')
            for box in range(8):
                if self.array[col][box] == None:
                    print(' ', end='')
                elif type(self.array[col][box]) == ob.BlackFigure:
                    print('b', end='')
                else:
                    print('w', end='')
            print('|')
        print('+--------+')

            
        
