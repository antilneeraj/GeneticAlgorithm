import pygame
import sys
from config.settings import WINDOW, WIN_WIDTH, WIN_HEIGHT, GROUND, PIPE_LIST, GROUND_Y, FPS
from components.graphics_components import Pipe
from managers.pop_manager import PopulationManager

pygame.init()
clock = pygame.time.Clock()
pop_manager = PopulationManager(100)

def spawn_pipe():
    PIPE_LIST.append(Pipe(WIN_WIDTH, GROUND_Y))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def main():
    pipe_spawn_timer = 10

    while True:
        handle_events()
        WINDOW.fill((0, 0, 0))
        GROUND.draw(WINDOW)
        if pipe_spawn_timer <= 0:
            spawn_pipe()
            pipe_spawn_timer = 200
        pipe_spawn_timer -= 1

        for p in PIPE_LIST[:]:
            p.draw(WINDOW, GROUND_Y)
            p.update()
            if p.off_screen_flag:
                PIPE_LIST.remove(p)

        if not pop_manager.extinct():
            pop_manager.update_live_agents()
        else:
            PIPE_LIST.clear()
            pop_manager.natural_selection()

        clock.tick(FPS)
        pygame.display.flip()

if __name__ == '__main__':
    main()
