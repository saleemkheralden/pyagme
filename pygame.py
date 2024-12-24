import pygame
import random, math

from pygame import Vector2 as Vec

pygame.init()

WIDTH = 1080 // 2
HEIGHT = 780 // 2
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
vel = .04
x = y = 50

running = True

EARTH_MASS = 5.972e24
SUN_MASS = 1.989e30

LEN_NORM = 151.2e9
VEL_NORM = 107e6

G = 6.6743e-11

AU = 151.2e9
SCALE = 250 / AU
DAY = 3600 * 24

print(G)
# print(-math.sqrt(G * 1.989e30 / (MASS_NORM * 1) ))
# print(107e6 / (3600 * VEL_NORM))

class planet:
    def __init__(self, pos, mass=1, vel=pygame.Vector2(0, 0), r=1, color='blue'):
        self.pos = pos
        self.f = pygame.Vector2(0, 0)
        self.mass = mass
        self.vel = vel
        self.path = [self.pos.copy()]
        self.r = r
        self.color = color
    
    def add_force(self, o: 'planet'):
        distance = self.pos.distance_to(o.pos) / AU
        F = G * self.mass * o.mass / (distance ** 2)
        print(F)

        direction = (o.pos - self.pos).normalize()
        self.f += F * direction
    
    def move(self, dt):
        acceleration = self.f / self.mass
        
        self.vel += acceleration * dt
        
        self.pos += self.vel * dt
        
        self.path.append(self.pos.copy())
        
        # Reset the force for the next frame
        # self.f = pygame.Vector2(0, 0)
        
    def display(self):
        # pygame.draw.circle(screen, self.color, self.pos, self.r)
        head = self.vel if self.vel.magnitude() != 0 else pygame.Vector2(0, 1)
        poly_shape = (
            self.pos + head.normalize() * 1.2,
            self.pos + self.pos.rotate(130),
            self.pos - head.normalize() * 0.8,
            self.pos + self.pos.rotate(-130),
        )
        pygame.draw.polygon(screen, self.color, poly_shape)
        pygame.draw.line(screen, (250, 250, 250), self.pos, self.pos + 1 * self.vel, width=2)


class bird:
    def __init__(self, id: int, pos: Vec, vel: Vec, head: Vec, color: str='red'):
        self.id = id
        self.pos = pos
        self.vel = vel
        self.head = head if vel.magnitude() == 0 else vel
        self.poly = (
            pos + unit_vec,
            pos + unit_vec + unit_vec.rotate(150).normalize() * 15,
            pos - 8 * unit_vec,
            pos + unit_vec + unit_vec.rotate(-150).normalize() * 15,
            )
        self.pivot = self.calc_pivot()
        self.color = color
        self.o_birds = []
        
    def calc_pivot(self):
        ret = Vec(0, 0)
        for e in self.poly:
            ret = ret + e
        return ret / len(self.poly)    
    
    def add_o_bird(self, o):
        self.o_birds.append(o)
        
    def update(self):
        self.poly = tuple((
            (e - self.pivot)
            .rotate((self.poly[0] - self.pivot).angle_to(pygame.mouse.get_pos() - self.pivot)) 
            + self.pivot
            
            for e in self.poly
        ))
        
        # for e in self.o_birds:
            # vel += (self.p)
        
        self.poly = tuple((
            e + (1 + vel) * (self.poly[0] - self.pivot).normalize()
            for i, e in enumerate(self.poly)
        ))
        
        self.pivot = self.calc_pivot()
        
    def draw(self):
        pygame.draw.polygon(screen, self.color, self.poly)
        
    def __eq__(self, other):
        return self.id == other.id
        


planets = [
    planet(pygame.Vector2(HEIGHT / 2, WIDTH / 2), mass=1.989e30, r=10, color=(250, 200, 50)),
    # planet(pygame.Vector2(HEIGHT / 2 + AU, WIDTH / 2),
    #        mass=EARTH_MASS,
    #        vel=pygame.Vector2(0, -29.783e3),
    #        r=5,
    #        color=(20, 100, 250)),
    # planet(pygame.Vector2(50, 50), vel=pygame.Vector2(-3, 2).normalize() * vel),
]
    
# for e in planets:
#     for o in planets:
#         if e is o:
#             continue
#         e.add_force(o)

pos = pygame.Vector2(100, 100)
unit_vec = pygame.Vector2(1, 0)

width = 5
height = 15

birds = [
    bird(0, pos.copy(), Vec(0, 0), unit_vec),
    bird(1, pos.copy() * 3, Vec(0, 0), unit_vec, (20, 200, 20)),
    ]

for e in birds:
    for u in birds:
        if e == u:
            continue
        e.add_o_bird(u)


# poly_shape = (
#     pos + unit_vec,
#     pos + unit_vec + unit_vec.rotate(150).normalize() * 15,
#     pos - 8 * unit_vec,
#     pos + unit_vec + unit_vec.rotate(-150).normalize() * 15,
# )

# def calc_pivot(poly):
#     ret = pygame.Vector2(0, 0)
#     for e in poly:
#         ret = ret + e
#     return ret / len(poly)

# pivot = calc_pivot(poly_shape)
# print(pivot)
# pivot = pos


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get dt in seconds
    dt = clock.tick(100)
    
    screen.fill((0, 0, 0))

    
    # for e in planets:
    #     e.move(dt)
    #     e.display()
    #     pygame.draw.lines(screen, (0, 250, 0), closed=False, points=e.path)
    
    # pos = pos.rotate((random.random() - 0.5) * 60)
    # pos = pos + pos.normalize().rotate(1)
    
    # birds[0].update()
    for e in birds:
        e.update()
        e.draw()

    pygame.display.flip()
    
pygame.quit()


# pos_v = pygame.Vector2(x, y)
# vel_v = pygame.Vector2(vel, vel)
# path = [pos_v]
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     # x += (-1 if random.random() <= 0.5 else 1) * random.random()
#     # y += (-1 if random.random() <= 0.5 else 1) * random.random()
#     # pos_v = pos_v.rotate(random.random())
#     # pos_v = pos_v.elementwise() + random.random()
    
#     # prev_pos_v = pos_v.copy()
    
#     vel_v = vel_v.rotate((random.random() - 0.5) * 60)
#     pos_v = pos_v + vel_v * 10
#     path.append(pos_v)
    
#     if not (10 <= pos_v.x <= WIDTH - 10):
#         vel_v.x = -vel_v.x
#     if not (10 <= pos_v.y <= HEIGHT - 10):
#         vel_v.y = -vel_v.y
    
    
    
#     screen.fill((0, 0, 0))
#     pygame.draw.circle(screen, (250, 0, 0), pos_v, 5)
#     pygame.draw.line(screen, (250, 250, 250), pos_v, pos_v + 5 * vel_v, width=2)
#     pygame.draw.lines(screen, (0, 250, 0), False, path)
#     # pygame.draw.rect(screen, (250, 0, 0), (pos_v.x, pos_v.y, 20, 50))
    
#     pygame.display.flip()
    
    
#     clock.tick(100)

# pygame.quit()


