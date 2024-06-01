import pygame
pygame.init()

backround_color = (135, 206, 235)
width = 600
height = 600
floor_height = 160
fps = 60
velocity = 4
window = pygame.display.set_mode((width,height))

class Object(pygame.sprite.Sprite):
    def __init__(self, x,y,width,height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, screen_offset):
        window.blit(self.image,(self.rect.x - screen_offset, self.rect.y))

class SquareBlock(Object):
    def __init__(self,x,y,width):
        super().__init__(x,y,width,width)
        image = pygame.image.load("Terrain.png").convert_alpha()
        rect = pygame.Rect(208,144,width,width)
        surface = pygame.Surface((width,width),pygame.SRCALPHA,32)
        surface.blit(image,(0,0),rect)
        block = pygame.transform.scale_by(surface,2)
        self.image.blit(block, (0,0))
        

class Flag(Object):
    def __init__(self,x,y,width, height):
        super().__init__(x,y,width,height,"flag")
        image = pygame.image.load("flagpole.png").convert_alpha()
        rect = pygame.Rect(420,0,width*12,height*28)
        surface = pygame.Surface((width*12,height*28),pygame.SRCALPHA,32)
        surface.blit(image,(0,0),rect)
        flag = pygame.transform.scale(surface,(128,386))
        self.image.blit(flag, (0,0))

class Player(pygame.sprite.Sprite):

    def __init__(self, x , y, width, height, sprites):
        self.rect = pygame.Rect(x,y,width,height)
        self.v_x = 0
        self.v_y = 0
        self.canjump = True
        self.direction = "right"
        self.animation_frame= 0
        self.fall_count = 0
        self.win = False
        self.sprites = sprites

    def jump(self):
        self.v_y = -7
        self.animation_frame = 0

    def adjust_position(self,v_y,v_x):
        self.rect.x += v_x
        self.rect.y += v_y

    def next_frame(self,fps):
        self.v_y += max(.3,(self.fall_count/fps))
        self.adjust_position(self.v_y,self.v_x)
        self.fall_count += 1
        state = "idle"
        if abs(self.v_y)>.7 or not self.canjump:
            state = "jump"
        elif self.v_x !=0:
            state = "walk"
        if self.win:
            state = "idle"
        directional_state = state + self.direction
        state_frames = self.sprites[directional_state]
        frame_number = int((self.animation_frame / 5))%len(state_frames)
        self.sprite = state_frames[frame_number]
        self.animation_frame += 1
        self.rect = self.sprite.get_rect(topleft = (self.rect.x,self.rect.y))
    
    def check_collision(self,objects):
        keys = pygame.key.get_pressed()
        self.v_x = 0

        self.adjust_position(0,-4)
        wall_left = False
        for object in objects:
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-1), object.rect):
                wall_left = True
                if object.name == "flag":
                        self.win = True
                break
        self.adjust_position(0,8)

        wall_right = False
        for object in objects:
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-1), object.rect):
                wall_right = True
                if object.name == "flag":
                        self.win = True
                break
        self.adjust_position(0,-4)

        if keys[pygame.K_a] and not wall_left:
            self.v_x = -velocity
            if self.direction != "left":
                self.direction = "left"
                self.animation_frame = 0
        if keys[pygame.K_d] and not wall_right:
            self.v_x = velocity
            if self.direction != "right":
                self.direction = "right"
                self.animation_frame = 0

        for object in objects:
            if pygame.Rect.colliderect(self.rect,object.rect):
                if self.v_y > 0:
                    self.rect.bottom = object.rect.top
                    self.v_y = 0
                    self.fall_count = 0
                    self.canjump = True
                if self.v_y < 0:
                    self.rect.top = object.rect.bottom
                    self.v_y = 0
    

    def draw(self, window, screen_offset):
        window.blit(self.sprite, (self.rect.x - screen_offset,self.rect.y))

def Game(window, level = 1):
    pygame.display.set_caption("1 million Kirby's fail at walking")
    clock = pygame.time.Clock()
    kirbypng = pygame.image.load("kirby.png").convert_alpha()
    animation_dict = {}
    sprite_names = ["walk", "jump", "idle"]

    animation_dict["walk"] = []
    for i in range(10):
        surface = pygame.Surface((23,23), pygame.SRCALPHA, 32)
        rect = pygame.Rect(8+ i*23, 51, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        animation_dict["walk"].append(pygame.transform.scale_by(surface,2))

    animation_dict["jump"] = []
    for i in range(9):
        surface = pygame.Surface((23,23), pygame.SRCALPHA, 32)
        rect = pygame.Rect(7+ int(i*24.3), 130, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        animation_dict["jump"].append(pygame.transform.scale_by(surface,2))

    animation_dict["idle"] = []
    for i in [10,10,39,39,66,66,96,96,124]:
        surface = pygame.Surface((23,23), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i, 215, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        animation_dict["idle"].append(pygame.transform.scale_by(surface,2))

    for name in sprite_names:
        animation_dict[name+"right"] = animation_dict[name]
        animation_dict[name+"left"] = [pygame.transform.flip(sprite,True,False) for sprite in animation_dict[name]]

    player = Player(64,256,64,64,animation_dict)
    if level == 1: 
        obstacles = [SquareBlock(384,height-floor_height-64, 64), 
                     Flag(512,height-64-floor_height-64,64,128)]
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10)]
    elif level == 2: 
        obstacles = [SquareBlock(256,height-floor_height-64, 64), 
                     SquareBlock(256+64,height-floor_height-64-64, 64), 
                     SquareBlock(256+64+64,height-floor_height-64-64, 64), 
                     Flag(256+64+64,height-64-floor_height-64-64-64,64,128)]
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10)]
    elif level == 3: 
        obstacles = [SquareBlock(256+64,height-floor_height-64, 64), 
                     SquareBlock(256,height-floor_height+64, 64), 
                     Flag(256+(64*4),height-floor_height-64-64,64,128)]
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10) if i != 4]

    
    screen_offset = 0

    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.canjump:
                    player.jump()
                    player.canjump = False

        

        player.next_frame(fps)
        player.check_collision(floor+obstacles)

        window.fill(backround_color)
        player.draw(window, screen_offset)
        for object in obstacles+floor:
            object.draw(window, screen_offset)
        pygame.display.update()

        if (player.rect.right - screen_offset) > width - 150 and player.v_x > 0:
            screen_offset += player.v_x
        if (player.rect.left - screen_offset) < 150 and player.v_x < 0:
            screen_offset += player.v_x
        
    

    pygame.quit()
    quit()           
    

            
Game(window, level = 3)