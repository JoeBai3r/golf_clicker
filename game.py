import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1500, 600
window = pygame.display.set_mode((WIDTH,HEIGHT))

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def create_hole(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (1300, 415)
    shape = pymunk.Poly.create_box(body, (30, 30), radius=0)
    shape.color = (0, 0, 0, 100)
    shape.mass = 100
    shape.collision_type = 3
    space.add(body, shape)
    return shape

def create_green(space, width, height):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (750, 500)
    shape = pymunk.Poly.create_box(body, (1500, 200), radius=0)
    shape.color = (124,252,0,100)
    shape.mass = 100
    shape.elasticity = 0
    shape.friction = 0
    shape.collision_type = 2
    space.add(body, shape)
    return shape

def create_boundaries(space, width, height):
    rects = [
            [(width/2, height - 10), (width, 20)],
            [(width/2, 10), (width, 20)],
            [(10, height/2), (20, height)],
            [(width - 10, height/2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_ball(space, mass, radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 255, 255, 100)
    shape.collision_type = 1
    shape.surface_velocity = (0,0)
    space.add(body, shape)
    return shape

def draw(space, window, draw_options, line):
    window.fill((0,255,255))

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)
    pygame.display.update()

def green_collide(arbiter, space, data):
    global ball
    

def green_begin(arbiter, space, data):
    return True

def goal_begin(arbiter, space, data):
    print('goal reached')
    return True

def goal_collide(arbiter, space, data):
    global run
    run = False

run = True

ball = None


def run(window, width, height):
    global run
    global ball
    
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)
  
    green = create_green(space, width, height)
    hole = create_hole(space)
    create_boundaries(space, width, height)
    ball = create_ball(space, 30, 10, (100, 100))


    handler_goal = space.add_collision_handler(1, 3)
    handler_green = space.add_collision_handler(1, 2)

    draw_options = pymunk.pygame_util.DrawOptions(window)
    
    pressed_pos = None

    while run:

        
        for event in pygame.event.get():
            
            line = None
            
            if pressed_pos:
                line = [ball.body.position, pygame.mouse.get_pos()]
            
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if not pressed_pos:
                    pressed_pos = pygame.mouse.get_pos()
                
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 100
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0,0))
                    pressed_pos = None
          
        
        handler_goal.begin = goal_begin
        handler_goal.post_solve = goal_collide

        handler_green.begin = green_begin
        handler_green.post_solve = green_collide

        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)

    
    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
