from cmath import pi
import pygame as pg

pg.init()

#====FIGURE-SECTION====
class Figure(pg.sprite.Sprite):
    def __init__(self, x, y, group, color):
        pg.sprite.Sprite.__init__(self, group)

        self.x = x
        self.y = y
        self.sizex = 100
        self.sizey = 100

        self.active = False
        self.pressed = False

        self.color = color
        self.queen = False
        self.rect = pg.Rect(self.x, self.y, self.sizex, self.sizey)
    
    def update_pos(self, x=None, y=None):
        if x != None and y != None:
            self.x = x
            self.y = y
        if self.y == self.queen_y:
            self.update_queen()
        self.rect = pg.Rect(self.x, self.y, self.sizex, self.sizey)
    
    def update_image(self, pict_path):
        self.image = pg.transform.scale(pg.image.load(pict_path), (self.sizex, self.sizey))

    def update_queen(self):
        if self.queen:
            return None
        
        pict_path = 'assets/superblack.png' if self.color == 'black' else 'assets/superwhite.png'
        
        self.queen = True
        self.moves = [(100, 100), (-100, 100),(100, -100), (-100, -100)]
        self.update_image(pict_path)
    
    # toggle images from pressed to normal and move figures between groups (to figure out if they are pressed or not)
    def update_pressed(self, bool, game):
        if self.pressed == bool:
            return

        game.set_pressed(self, bool) #function, that will move figure between groups
        if self.pressed:
            if self.queen:
                pict_path = 'assets/superblack.png' if self.color == 'black' else 'assets/superwhite.png'
            else:
                pict_path = 'assets/black.png' if self.color == 'black' else 'assets/white.png'
        else:
            if self.queen:
                pict_path = 'assets/pressed_super_black.png' if self.color == 'black' else 'assets/pressed_super_white.png'
            else:
                pict_path = 'assets/pressed_black.png' if self.color == 'black' else 'assets/pressed_white.png'
                
        self.pressed = bool
        self.update_image(pict_path)

    # function which creates tiles when you click on figure, return True when you can jump with the figure
    def search_for_play(self, create_tiles, game):
        jump = False #returns if figure can jump
        can_play = False #return if figure is able to play (is not blocked)
        for move in self.moves:
            tile_x = move[0] + self.x
            tile_y = move[1] + self.y
            jump_x = move[0] + tile_x
            jump_y = move[1] + tile_y

            if game.valid_indexes(tile_x, tile_y):
                if game.array[tile_x//100][tile_y//100] == None:
                    can_play = True
                    if create_tiles:
                        _ = Tile(tile_x, tile_y, self, False, None, game.tiles)
                elif self.valid_jump_indexes(tile_x, tile_y, jump_x, jump_y, game):
                    jump = True
                    if create_tiles:
                        to_kill = game.array[tile_x//100][tile_y//100]
                        _ = Tile(jump_x, jump_y, self, True, to_kill, game.jump_tiles)
        return jump, can_play
    
    # checks if jump_x and jump_y are valid indexes and figure can jump to position (jump_x, jump_y)
    def valid_jump_indexes(self, tile_x, tile_y, jump_x, jump_y, game):
        return game.array[tile_x//100][tile_y//100].color != self.color and game.valid_indexes(jump_x, jump_y) and game.array[jump_x//100][jump_y//100] == None

    def update(self, game):
        m_x, m_y = pg.mouse.get_pos()
        if self.rect.collidepoint(m_x, m_y):
            if self.active:
                if self.pressed:
                    game.delete_tiles()
                    self.update_pressed(False, game)
                else:
                    self.search_for_play(True, game)
                    self.update_pressed(True, game)
                            

class BlackFigure(Figure):
    def __init__(self, x, y, group) -> None:
        Figure.__init__(self, x, y, group, 'black')

        self.moves = [(100,100),(-100,100)]
        self.image = pg.transform.scale(pg.image.load('assets/black.png'), (self.sizex, self.sizey))
        self.queen_y = 700


class WhiteFigure(Figure):
    def __init__(self, x, y, group) -> None:
        Figure.__init__(self, x, y, group, 'white')

        self.moves = [(100,-100),(-100,-100)]
        self.image = pg.transform.scale(pg.image.load('assets/white.png'), (self.sizex, self.sizey))
        self.queen_y = 0

#====TILE-SECTION====
class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, parent, jump, to_kill, group) -> None:
        pg.sprite.Sprite.__init__(self, group)

        self.x = x
        self.y = y
        self.sizex = 100
        self.sizey = 100

        self.active = True
        
        self.parent = parent
        self.to_kill = to_kill
        self.jump = jump

        self.image = pg.transform.scale(pg.image.load('assets/pressed_tile.png'), (self.sizex, self.sizey))
        self.rect = pg.Rect(self.x, self.y, self.sizex, self.sizey)
    
    def update(self, game):
        m_x, m_y = pg.mouse.get_pos()
        if self.rect.collidepoint(m_x, m_y):
            if self.active:
                game.move_in_array((self.parent.x//100, self.parent.y//100),(self.x//100, self.y//100))
                self.parent.update_pos(self.x, self.y)
                game.delete_tiles()
                self.parent.update_pressed(False, game)
                if self.jump:
                    game.erase_in_array(self.to_kill.x//100, self.to_kill.y//100)
                    self.to_kill.kill()
                    game.continue_playing(self.parent)
                else:
                    game.switch_player()
                #game._print_game()

#====GROUP-SECTION====
class FigureGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def set_active(self, bool):
        for figure in self.sprites():
            figure.active = bool
    
    def add_figures_to(self, group):
        for figure in self.sprites():
            group.add(figure)

class TileGroup(pg.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

    def set_active(self, bool):
        for tile in self.sprites():
            tile.active = bool

#====MENU-SECTION====
class Button(pg.sprite.Sprite):
    def __init__(self, x, y, label, pict_path):
        pg.sprite.Sprite.__init__(self)

        self.label = label
        self.image = pg.transform.scale(pg.image.load(pict_path), (200,200))
        self.rect = pg.Rect(x, y, 200, 200)
    
    def update(self, game):
        m_x, m_y = pg.mouse.get_pos()
        if self.rect.collidepoint(m_x, m_y):
            if self.label == 'Replay':
                game.reset_game()                
            else:
                game.quit_game()

class Menu(pg.sprite.Sprite):
    def __init__(self, end_menu, winner, replay_button, quit_button) -> None:
        pg.sprite.Sprite.__init__(self)
    
        self.winner = winner
        self.font = pg.font.Font('assets/SupermercadoOne-Regular.ttf', 64)
        self.label = self.font.render(f'{winner} wins', 1, pg.Color(255, 255, 255, 255)) if end_menu else self.font.render('Pause menu', 1, pg.Color(255, 255, 255, 255))

        self.replay_button = replay_button
        self.quit_button = quit_button
    
    def update(self, game):
        self.quit_button.update(game)
        self.replay_button.update(game)

    def draw(self, screen):
        screen.blit(self.label, (250,100))
        screen.blit(self.replay_button.image, self.replay_button.rect)
        screen.blit(self.quit_button.image, self.quit_button.rect)