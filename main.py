import pygame
import pymunk
import pymunk.pygame_util
import math

class Game:
    def __init__(self):
        self.map = Map()
        self.handler_goal = self.map.space.add_collision_handler(1, 3)
        self.handler_green = self.map.space.add_collision_handler(1, 2)
        self.count = 0
        self.run()

    def run(self):
        pygame.init()

        run = True

        clock = pygame.time.Clock()
        fps = 60
        dt = 1 / fps

        pressed_pos = None

        while run:
            for event in pygame.event.get():
                
                self.map.line = None

                if pressed_pos:
                    self.map.line = [self.map.ball.body.position, pygame.mouse.get_pos()]

                if event.type == pygame.QUIT:
                    run = False
                    break
                
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if not pressed_pos:
                        pressed_pos = pygame.mouse.get_pos()

                    elif pressed_pos:
                        self.map.ball.shape.body_type = pymunk.Body.DYNAMIC
                        angle = self.calculate_angle(*self.map.line)
                        force = self.calculate_force(*self.map.line) * 100
                        fx = math.cos(angle) * force
                        fy = math.sin(angle) * force
                        self.map.ball.body.apply_impulse_at_local_point((fx,fy), (0,0))
                        pressed_pos = None
                        self.count += 1
            
            self.handler_goal.begin = self.goal_collide
            self.handler_green.begin = self.green_collide

            self.map.draw()
            self.map.space.step(dt)
            clock.tick(fps)

        pygame.quit()

    def calculate_force(self, p1, p2):
        return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

    def calculate_angle(self, p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
    def goal_collide(self, arbiter, space, data):
        print('Goal reached')
        if self.count == 1:
            print('Hole in 1!')
        else:
            print(f'Your score was {self.count}')
        return True
    
    def green_collide(self, arbiter, space, data):
        self.map.ball.body.velocity = (0, 0)   
        return True
        
class Map:
    def __init__(self):
        self.width = 1500
        self.height = 600
        self.line = None
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.ball = Ball(self.space)
        self.create_green()
        self.create_hole()
        self.create_boundaries()
        

    def draw(self):
        self.window.fill((0, 255,255)) 
        
        if self.line:
            pygame.draw.line(self.window, "black", self.line[0], self.line[1], 3)

        draw_options = pymunk.pygame_util.DrawOptions(self.window)

        self.space.debug_draw(draw_options)
        pygame.display.update()
    
    def create_hole(self):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (1300, 415)
        shape = pymunk.Poly.create_box(body, (30,30), radius=0)
        shape.color = (0, 0, 0, 100)
        shape.mass = 100
        shape.collision_type = 3
        self.space.add(body, shape)

    def create_green(self):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (750, 500)
        shape = pymunk.Poly.create_box(body, (1500, 200), radius=0)
        shape.color = (124,252,0,100)
        shape.mass = 100
        shape.elasticity = 0
        shape.friction = 0
        shape.collision_type = 2
        self.space.add(body, shape)

    def create_boundaries(self):
        rects = [
                [(self.width/2, self.height - 10), (self.width, 20)],
                [(self.width/2, 10), (self.width, 20)],
                [(10, self.height/2), (20, self.height)],
                [(self.width - 10, self.height/2), (20, self.height)]
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction - 0.5
            self.space.add(body, shape)



class Ball:
    def __init__(self, space):
       self.space = space
       self.body = pymunk.Body()
       self.body.position = (100, 100)
       self.shape = pymunk.Circle(self.body, 10)
       self.shape.mass = 30
       self.shape.elasticity = 0.9
       self.shape.friction = 0.4
       self.shape.velocity = (0, 0)
       self.shape.color = (255, 255, 255, 100)
       self.shape.collision_type = 1
       self.space.add(self.body, self.shape)
       

if __name__ == "__main__":
    game = Game()
