import pygame as pg
import math as m
import random as rndm
import colorsys as cs
import sys

# Variables fijas
vec = pg.Vector2
fi = (1 + m.sqrt(5)) / 2
g = vec([0, 9.8])
cr_air_x = 1
cr_air_y = 0.7
cr_flr_x = 0.7

# Variables de control
i = 0.0
ppc = 10 # Píxeles por color

# Pantalla
WIDTH = 960
HEIGHT = 540
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
CLOCK = pg.time.Clock()

# Variables del player
size_y = HEIGHT / 3
size_x = size_y / 4
v_max = 500 / 9
pos_x_0 = rndm.uniform(size_x, WIDTH - size_x)
pos_y_0 = rndm.uniform(HEIGHT - size_y / 1.5, HEIGHT - size_y / 2 + 5)
simple = True
color_simple = (rndm.randint(100, 255), rndm.randint(100, 255), rndm.randint(100, 255))

# Píxeles por metro
pxm = size_y / 1.8

# Mapear
def mapping(x, a, b, c, d):
    return (x - a) * (d - c) / (b - a) + c

# Calcular color complejo
def color_complex(x, y):
    h = mapping(x, 0, WIDTH, 0, 1)
    s = mapping(y, 0, HEIGHT, 0, 1)
    v = 1
    r, g, b = cs.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

# Player
class player:
    def __init__(self, pos_x, pos_y):
        self.frz = vec([0.0, 0.0])
        self.acel = vec([0.0, 0.0])
        self.vel = vec([0.0, 0.0])
        self.pos = vec(float(pos_x), float(pos_y))
        
        self.P = vec(0.0, 0.0)
        self.F_n = vec(0.0, 0.0)
        self.F_r_flr = vec(0.0, 0.0)
        self.F_r_air = vec(0.0, 0.0)

        self.mass = 75
        self.shape = pg.Rect(0, 0, size_x, size_y)
        self.shape.center = (int(self.pos[0]), int(self.pos[1]))
        self.on_ground = False

    def frz_aplic(self, f_x, f_y): # N(ewton)
        self.P.y = self.mass * g.y
        if abs(self.vel.x) >= 1 / 20:
            self.F_r_air.x = -1 * (1.225 * (self.vel.x ** 2) * size_x * size_y * cr_air_x / (2 * pxm ** 2)) * (self.vel.x / abs(self.vel.x))
        else:
            self.F_r_air.x = 0
            self.vel.x = 0
        if not self.vel.y == 0:
            self.F_r_air.y = -1 * (1.225 * (self.vel.y ** 2) * (size_x ** 2) * cr_air_y / (2 * pxm ** 2)) * (self.vel.y / abs(self.vel.y))
        else:
            self.F_r_air.y = 0
        if self.on_ground:
            self.F_n.y = - self.P.y
            if (not self.vel.x == 0) and self.F_n.y < f_y:
                self.F_r_flr.x = - m.copysign(abs((self.F_n.y - f_y) * cr_flr_x), self.vel.x)
            else:
                self.F_r_flr.x = 0
        else:
            self.F_n.y = 0.0
            self.F_r_flr.x = 0.0
        # Principio de Superposición
        self.frz = vec([f_x, f_y]) + self.P + self.F_n + self.F_r_air + self.F_r_flr

    def acel_def(self): # m/s^2
        # 2ª Ley de Candy2
        self.acel = self.frz / self.mass

    def vel_def(self, dt): # m/s
        self.vel += self.acel * dt
        self.vel.x = m.copysign(min(v_max, abs(self.vel.x)), self.vel.x)
        self.vel.y = m.copysign(min(v_max, abs(self.vel.y)), self.vel.y)

    def pos_def(self, dt): # px
        self.pos += self.vel * dt * pxm
        self.shape.center = (int(self.pos.x), int(self.pos.y))
        if self.shape.right > WIDTH:
            self.shape.right = WIDTH
            self.vel.x = 0
        if self.shape.left < 0:
            self.shape.left = 0
            self.vel.x = 0
        if self.shape.bottom > HEIGHT:
            self.shape.bottom = HEIGHT
            self.vel.y = 0
        if self.shape.top < 0:
            self.shape.top = 0
            self.vel.y = 0
        if not self.shape.center == (int(self.pos.x), int(self.pos.y)):
            self.pos = self.shape.center

    def draw_simple(self):
        pg.draw.rect(WINDOW, color_simple, self.shape)

    def draw_clomplex(self):
        for x in range(self.shape.left, self.shape.right, ppc):
            for y in range(self.shape.top, self.shape.bottom, ppc):
                pg.draw.rect(WINDOW, color_complex(x, y), (x, y, ppc, ppc))

    def mover(self, f_x, f_y, dt):
        self.on_ground = (self.shape.bottom >= HEIGHT - 1)
        self.frz_aplic(f_x, f_y)
        self.acel_def()
        self.vel_def(dt)
        self.pos_def(dt)
        if simple:
            self.draw_simple()
        else:
            self.draw_clomplex()

    def dar_info_frz(self, f_x, f_y):
        print("f_x = ", f_x)
        print("f_y = ", f_y)
        print("P = ", self.P)
        print("F_n = ", self.F_n)
        print("F_r_flr = ", self.F_r_flr)
        print("F_r_air_x = ", self.F_r_air.x)
        print("F_r_air_y = ", self.F_r_air.y)

    def dar_info_vel(self):
        print("vel.x = ", self.vel.x)
        print("vel.y = ", self.vel.y)

p1 = player(pos_x_0, pos_y_0)

running = True

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                simple = not simple
    
    det = CLOCK.tick(60) / 1000
    f_x = 0
    f_y = 0

    key_pres = pg.key.get_pressed()

    if key_pres[pg.K_w]:
       f_y -= (1 + 99 * p1.on_ground) * 147
    if key_pres[pg.K_s]:
       f_y += (1 + 2 * p1.on_ground) * 245
    if key_pres[pg.K_a]:
        f_x -= (1 + 2 * p1.on_ground) * 490
    if key_pres[pg.K_d]:
        f_x += (1 + 2 * p1.on_ground) * 490
    if key_pres[pg.K_ESCAPE]:
        running = False


    WINDOW.fill(0)
    p1.mover(f_x, f_y, det)

    pg.display.flip()

pg.quit()
sys.exit()