import pygame
import math
import numpy as np
pygame.init()

backround_color = (135, 206, 235)
fps = 1000
velocity = 4
floor_height = 160
width = 600
height = 600

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
        
class Spikes(Object): 

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"spike")
        image = pygame.image.load("spikes.png").convert_alpha()
        rect = pygame.Rect(58,222,width,height)
        surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
        surface.blit(image,(0,0), rect)
        block = pygame.transform.scale(surface, (64, 32)) 
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

    def __init__(self, x , y, width, height, sprites,flag_x,flag_y):
        self.rect = pygame.Rect(x,y,width,height)
        self.v_x = 0
        self.v_y = 0
        self.canjump = False
        self.direction = "right"
        self.animation_frame= 0
        self.fall_count = 0
        self.win = False
        self.sprites = sprites
        self.flag_x = flag_x
        self.flag_y = flag_y
        self.died = False
        self.time = 0
        self.sightlines = []
        self.distances = []

    def jump(self):
        self.v_y = -6.6
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
    

    
    def check_collision(self,objects,keys):
        self.v_x = 0

        self.adjust_position(0,-4)
        wall_left = False
        for object in objects:
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-1), object.rect):
                wall_left = True
                if object.name == "spike":
                        self.died = True
                elif object.name == "flag":
                        self.win = True
                break
        self.adjust_position(0,8)

        wall_right = False
        for object in objects:
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-2), object.rect):
                wall_right = True
                if object.name == "spike":
                        self.died = True
                elif object.name == "flag":
                        self.win = True
                break
        self.adjust_position(0,-4)

        if keys[0,0]>keys[0,1] and not wall_left:
            self.v_x = -velocity
            if self.direction != "left":
                self.direction = "left"
                self.animation_frame = 0
        if keys[0,1]>keys[0,0] and not wall_right:
            self.v_x = velocity
            if self.direction != "right":
                self.direction = "right"
                self.animation_frame = 0
        self.distances = [100,100,100,100,100,100,100,100]
        self.sightlines = [[(self.rect.x+23,self.rect.y+23),(self.rect.x+23+math.sin(.25*i*math.pi)*100,self.rect.y+23+math.cos(.25*i*math.pi)*100),3] for i in range(8)]
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
            for i in range(8):
                x = object.rect.clipline(self.sightlines[i][0][0],self.sightlines[i][0][1],self.sightlines[i][1][0],self.sightlines[i][1][1])
                if x != ():
                    start = x[0]
                    d = math.sqrt((start[0] - self.rect.x-23)**2+(start[1] - self.rect.y-23)**2)
                else: d = 100
                if d < self.distances[i]:
                    self.distances[i] = d
    

    def draw(self, window, screen_offset):
        window.blit(self.sprite, (self.rect.x - screen_offset,self.rect.y))
        for i in range(8):
            if self.distances[i] < 100:
                x = 255
                y = 0
            else: 
                x = 0
                y = 255
            pygame.draw.line(window,(x,y,0),tuple(map(lambda i, j: i + j, self.sightlines[i][0], (-screen_offset,0))),tuple(map(lambda i, j: i + j, self.sightlines[i][1], (-screen_offset,0))),self.sightlines[i][2])

def Game(window,models,level = 1):
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

    players = [Player(64,256,64,64,animation_dict,512,height-64-128) for i in range(len(models))]

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
                     Spikes(256,height-floor_height+32, 150, 50), 
                     Flag(256+(64*4),height-floor_height-64-64,64,128)]
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10) if i != 4]
    elif level == 4: 
        spikes = [Spikes(256 + (64 * i), height-floor_height-32, 150, 50) for i in range(6)]
        obstacles = [SquareBlock(256 + 64,height-floor_height-64-64, 64), 
                     SquareBlock(256 - 64,height-floor_height-64, 64), 
                     SquareBlock(256 + (64 * 4),height-floor_height-(64 * 3), 64), 
                     Flag(256 + (64 * 8),height-64-floor_height-64,64,128)]
        obstacles = obstacles + spikes
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(15)]
    elif level == 5: 
        spikes = [Spikes(256 + (64 * i), height-floor_height-32, 150, 50) for i in range(6)]
        obstacles = [SquareBlock(256 + 64,height-floor_height-64-64, 64), 
                     SquareBlock(256 - 64,height-floor_height-64, 64), 
                     SquareBlock(256 + (64 * 4),height-floor_height-(64 * 3), 64), 
                     SquareBlock(256 + (64 * 5),height-floor_height-(64 * 4), 64), 
                     SquareBlock(256 + (64 * 3),height-floor_height-(64 * 5), 64), 
                     SquareBlock(256 + (64 * 2),height-floor_height-(64 * 5), 64), 
                     Flag(256 + (64 * 2),height-floor_height-(64 * 7),64,128)]
        obstacles = obstacles + spikes
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10)]
    
    player_array = np.array([models, players])
    screen_offset = 0
    time_limit = 150
    time = 0

    run = True
    while run:
        time +=1
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        window.fill(backround_color)
        
        for i in range(len(player_array[0,:])):
        
            keys = player_array[0,i].predict([[player_array[1,i].rect.x,player_array[1,i].rect.y,player_array[1,i].v_x,player_array[1,i].v_y,int(player_array[1,i].canjump),player_array[1,i].flag_x,player_array[1,i].flag_y]],verbose = 0)
        
            if keys[0,2]>.5 and player_array[1,i].canjump:
                player_array[1,i].jump()
                player_array[1,i].canjump = False

            player_array[1,i].next_frame(fps)
            player_array[1,i].check_collision(floor+obstacles,keys)

            if not player_array[1,i].died:
                player_array[1,i].draw(window, screen_offset)
            player_array[1,i].time += 1
            if player_array[1,i].win:
                player_array[1,i].time -= 1
        
       



        for object in obstacles+floor:
            object.draw(window, screen_offset)
        pygame.display.update()

        if player_array[0].size:
            camera_tracked = player_array[1,np.argmax([player.rect.right for player in player_array[1,:]])]

            if (camera_tracked.rect.right - screen_offset) > width - 150 and camera_tracked.v_x > 0:
                screen_offset += camera_tracked.v_x
            if (camera_tracked.rect.left - screen_offset) < 150 and camera_tracked.v_x < 0:
                screen_offset += camera_tracked.v_x
        
        for i in range(len(player_array[1,:])):

            if player_array[1,i].rect.y > height:
                player_array[1,i].died = True

        if time > time_limit:
            run = False

    data_array = list(player_array[1,:])
    return [[player.win,player.rect.x,time,player.died] for player in data_array]
    pygame.quit()
    quit()           
    

        