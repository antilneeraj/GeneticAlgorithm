import pygame
import sys
from config.settings import WINDOW, WIN_WIDTH, WIN_HEIGHT, GROUND, PIPE_LIST, GROUND_Y, FPS, PIPE_COVERED
from components.graphics_components import Pipe
from managers.pop_manager import PopulationManager
import config.settings as settings

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

def draw_stats():
    font = pygame.font.SysFont('Arial', 18)
    # Display the last generation's average fitness if available,
    # otherwise compute the average lifespan of currently living agents.
    if pop_manager.last_generation_avg_fitness > 0:
        avg_fitness = pop_manager.last_generation_avg_fitness
    elif pop_manager.agents:
        avg_fitness = sum(agent.lifespan for agent in pop_manager.agents) / len(pop_manager.agents)
    else:
        avg_fitness = 0
    stats_text = (
        f"Gen: {pop_manager.generation}  "
        f"Agents: {len(pop_manager.agents)}  "
        f"Last Gen Avg Fitness: {avg_fitness:.2f}  "
        f"Breeding: {pop_manager.breeding_count}  "
        f"Poles: {settings.PIPE_COVERED}"
    )
    text_surface = font.render(stats_text, True, (255, 255, 255))
    WINDOW.blit(text_surface, (10, settings.GROUND_Y + 30))


def draw_agents():
    for agent in pop_manager.agents:
        if agent.alive:
            # Draw as a circle with a border for better visibility
            pygame.draw.circle(WINDOW, agent.color, (agent.x, int(agent.y)), agent.radius)
            pygame.draw.circle(WINDOW, (0, 0, 0), (agent.x, int(agent.y)), agent.radius, 2)

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

        draw_agents()
        draw_stats()

        clock.tick(FPS)
        pygame.display.flip()

if __name__ == '__main__':
    main()
