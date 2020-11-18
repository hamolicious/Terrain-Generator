import pygame
from time import time
from vector_class import Vector2D as Vec2
from terrain import Terrain

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

terrain = Terrain(10, 10, 45, pos=(size[0]/2, size[0]/2, size[1]/2))
terrain.rotate_plane(xt=50)
terrain.rotate_plane(yt=45/2)

sense = 0.1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    frame_start_time = time()
    screen.fill([51, 51, 51])

    mmovrel = Vec2(pygame.mouse.get_rel())
    mpress = pygame.mouse.get_pressed()

    if mpress[0]:
        terrain.rotate_plane(yt=-(mmovrel.x * sense) * delta_time)
    if mpress[2]:
        terrain.rotate_plane(xt=(mmovrel.y * sense) * delta_time)
    if mpress[1]:
        terrain.scale -= mmovrel.y

    terrain.draw(screen)

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - frame_start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
