import pygame as pg
import sys
import game as g

pg.init()
game = g.Game()

background = pg.transform.scale(pg.image.load('assets/background.png'),game.screen_size)

screen = pg.display.set_mode(game.screen_size)

while True:

    # logic of input handling
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game.pause_game()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                if game.end:
                    game.end_menu.update(game)
                elif game.pause:
                    game.pause_menu.update(game)
                else:
                    if game.pressed_figures.sprites():
                        game.pressed_figures.update(game)
                        if game.jump_tiles.sprites():
                            game.jump_tiles.update(game)
                        else:
                            game.tiles.update(game)
                    else:
                        game.jump_figures.update(game)
                        game.active_figures.update(game)
                    

    # logic for screen drawing
    screen.blit(background, (0,0))
    if game.quit:
        pg.quit()
        sys.exit()
    elif game.end:
        game.end_menu.draw(screen)
        pg.display.set_caption(f'{game.end_menu.winner} wins')
    elif game.pause:
        game.pause_menu.draw(screen)
        pg.display.set_caption('Pause menu')
    else:
        game.black_figures.draw(screen)
        game.white_figures.draw(screen)
        game.pressed_figures.draw(screen)
        game.jump_figures.draw(screen)
        pg.display.set_caption(f"{game.player}'s turn")

        if game.jump_tiles.sprites():
            game.jump_tiles.draw(screen)
        else:
            game.tiles.draw(screen)
    
    pg.display.flip()
    
