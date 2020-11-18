import pygame
from math import sin, cos, radians
from random import randint
from vector_class import Vector3D as Vec3, Vector2D as Vec2
from noise import pnoise2

class Terrain:
    def __init__(self, w, h, scale, pos=(0, 0, 0)):
        self.pos = Vec3(pos)
        self.size = Vec2(w, h)
        self.verts = []
        self.connections = []
        self.scale = scale

        self.octaves = 6
        self.persistence = 0.5
        self.lacunarity = 2.0

        self.generate_plane()

    def generate_plane(self):
        self.connections = []
        self.verts = []

        for z in range(self.size.y):
            for x in range(self.size.x):
                y = pnoise2(x + 0.1, z + 0.1, octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity, repeatx=1024, repeaty=1024, base=0) * 2
                v = Vec3(x - self.size.x/2, y, z - self.size.y/2)

                self.verts.append(v)

        index = lambda px, py : py * self.size.y + px
        for z in range(self.size.y):
            for x in range(self.size.x):
                try:
                    if x >= self.size.x-1 or z >= self.size.y-1 : raise IndexError

                    v1 = self.verts[index(x,     z)]
                    v2 = self.verts[index(x+1,   z)]
                    v3 = self.verts[index(x+1, z+1)]
                    v4 = self.verts[index(x  , z+1)]

                    self.connections.append([v1, v2, v4])
                    self.connections.append([v2, v3, v4])
                except IndexError:
                    self.connections.append([self.verts[0], self.verts[0], self.verts[0]])

    def rotate_plane(self, xt=0, yt=0):
        for v in self.verts:
            # rotate x
            v.x = (v.x * 1) + (v.y *       0) + (v.z *        0)
            v.y = (v.x * 0) + (v.y * cos(xt)) + (v.z * -sin(xt))
            v.z = (v.x * 0) + (v.y * sin(xt)) + (v.z *  cos(xt))

            # rotate y
            v.x = (v.x *  cos(yt)) + (v.y * 0) + (v.z * sin(yt))
            v.y = (v.x *        0) + (v.y * 1) + (v.z *       0)
            v.z = (v.x * -sin(yt)) + (v.y * 0) + (v.z * cos(yt))

    def draw(self, screen):
        self.connections.sort(key=lambda elem : sum([i.z for i in elem]), reverse=True)
        for i1, i2, i3 in self.connections:
            p = [((i1 * self.scale) + self.pos).get()[:2], ((i2 * self.scale) + self.pos).get()[:2], ((i3 * self.scale) + self.pos).get()[:2]]
            pygame.draw.polygon(screen, [0, 150, 0], p, 0)
            pygame.draw.polygon(screen, [0, 0, 0], p, 1)
