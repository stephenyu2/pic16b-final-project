import pygame
import math
pygame.init()

backround_color = (135, 206, 235)
width = 600
height = 600
floor_height = 160
fps = 60
velocity = 4
window = pygame.display.set_mode((width,height))

cx = 46             # customizable, sightline center of x (default: 46)
cy = 23             # customizable, sightline center of y (default: 23)

class Object(pygame.sprite.Sprite):
    """
    A base class for game objects.

    Attributes:
        rect (pygame.Rect): A rectangle representing the position and size of the object
        image (pygame.Surface): A surface representing the appearance of the object
        width (int): The width of the object
        height (int): The height of the object
        name (str): The name or type of the object

    Methods:
        __init__(x, y, width, height, name="block"): Initializes an Object instance with the given parameters
        draw(window, screen_offset): Draws the object onto the specified window with an optional screen offset
    """
    def __init__(self, x,y,width,height, name = "block"):
        """
        Initializes an Object instance with the given parameters.

        Args:
            x (int): The x-coordinate of the object
            y (int): The y-coordinate of the object
            width (int): The width of the object
            height (int): The height of the object
            name (str, optional): The name or type of the object. Defaults to "block"
        """
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, screen_offset):
        """
        Draws the object onto the specified window with an optional screen offset.

        Args:
            window: The pygame surface to draw the object onto
            screen_offset (int): The offset of the screen, used to adjust the object's position
        """
        window.blit(self.image,(self.rect.x - screen_offset, self.rect.y))

        
class Player(pygame.sprite.Sprite):
    """
    A class representing the player character in the game.

    Attributes:
        rect (pygame.Rect): A rectangle representing the position and size of the player.
        v_x (float): The horizontal velocity of the player.
        v_y (float): The vertical velocity of the player.
        canjump (bool): Indicates if the player is currently able to jump.
        direction (str): The current direction the player is facing ("left" or "right").
        animation_frame (int): The frame number of the player's animation.
        fall_count (int): The count of frames since the player started falling.
        win (bool): Indicates if the player has reached the flag and won the game.
        sprites (dict): A dictionary containing sprite images for different player states.
        flag_x (int): The x-coordinate of the flag's position.
        flag_y (int): The y-coordinate of the flag's position.
        died (bool): Indicates if the player has died.
        time (int): The elapsed time in the game.
        sightlines (list): A list containing sightlines used for collision detection.
        distances (list): A list containing distances to obstacles detected by sightlines.
        types (list): A list containing types of obstacles detected by sightlines.
        name_mapping (dict): A dictionary mapping obstacle names to their types.

    Methods:
        jump(): Makes the player jump.
        adjust_position(v_y, v_x): Adjusts the player's position based on velocity.
        next_frame(fps): Updates the player's animation frame and position for the next frame.
        check_collision(objects, keys): Checks for collisions with objects and updates player state.
        draw(window, screen_offset): Draws the player and collision sightlines on the window.
    """
    
    def __init__(self, x , y, width, height, sprites):
        """
        Initializes a Player instance.

        Args:
        x (int): The x-coordinate of the player's position.
        y (int): The y-coordinate of the player's position.
        width (int): The width of the player's bounding box.
        height (int): The height of the player's bounding box.
        sprites (dict): A dictionary containing sprite images for different player states.
        """
        self.rect = pygame.Rect(x,y,width,height)
        self.v_x = 0
        self.v_y = 0
        self.canjump = True
        self.direction = "right"
        self.animation_frame= 0
        self.fall_count = 0
        self.win = False
        self.sprites = sprites
        self.sightlines = []
        self.distances = []
        self.types = []
        self.name_mapping = {"block": 0, "spike": 1, "flag": 2}

    def jump(self):
        """
        Makes the player jump.
        """
        self.v_y = -6.6
        self.animation_frame = 0

    def adjust_position(self,v_y,v_x):
        """
        Adjusts the player's position based on velocity.

        Args:
        v_y (float): The vertical velocity.
        v_x (float): The horizontal velocity.
        """
        self.rect.x += v_x
        self.rect.y += v_y

    def next_frame(self,fps):
        """
        Updates the player's animation frame and position for the next frame.

        Args:
        fps (int): The frames per second of the game.
        """
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
        """
        Checks for collisions with objects and updates player state.

        Args:
        objects (list): A list of game objects to check for collisions.

        The method updates the player's velocity, direction, and animation frame based on collision 
        detection with objects in the game world. It also updates the player's sightlines for 
        obstacle detection and adjusts player position based on collisions.
        """
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

        self.distances = [100,100,100,100,100,100,100,100]
        self.types = [0,0,0,0,0,0,0,0]
        self.sightlines = [[(self.rect.x+cx,self.rect.y+cy),(self.rect.x+cx+math.sin(.25*i*math.pi)*100,self.rect.y+cy+math.cos(.25*i*math.pi)*100),3] for i in range(8)]
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
                    d = math.sqrt((start[0] - self.rect.x-cx)**2+(start[1] - self.rect.y-cy)**2)
                else: d = 100
                if d < self.distances[i]:
                    self.distances[i] = d
                    self.types[i] = self.name_mapping[object.name]
    

    def draw(self, window, screen_offset):
        window.blit(self.sprite, (self.rect.x - screen_offset,self.rect.y))
        for i in range(8):
            if self.distances[i] < 100 and self.types[i] == 0:
                x = 0
                y = 0
                z = 255
            elif self.distances[i] < 100: 
                x = 255
                y = 0
                z = 0
            else:
                x = 0
                y = 255
                z = 0
            pygame.draw.line(window,(x,y,z),tuple(map(lambda i, j: i + j, self.sightlines[i][0], (-screen_offset,0))),tuple(map(lambda i, j: i + j, self.sightlines[i][1], (-screen_offset,0))),self.sightlines[i][2])

class SquareBlock(Object):
    """
    A class representing a square block object in a game.

    Inherits from:
        Object: A base class for game objects

    Attributes:
        Inherits all attributes from the Object class

    Methods:
        __init__(x, y, width): Initializes a SquareBlock instance with the given parameters
    """
    def __init__(self,x,y,width):
        """
        Initializes a SquareBlock instance with the given parameters.

        Args:
            x (int): The x-coordinate of the block
            y (int): The y-coordinate of the block
            width (int): The width and height of the square block
        """
        super().__init__(x,y,width,width)
        image = pygame.image.load("Terrain.png").convert_alpha()
        rect = pygame.Rect(208,144,width,width)
        surface = pygame.Surface((width,width),pygame.SRCALPHA,32)
        surface.blit(image,(0,0),rect)
        block = pygame.transform.scale_by(surface,2)
        self.image.blit(block, (0,0))

class Spikes(Object): 
    """
    A class representing a spikes object in a game.

    Inherits from:
        Object: A base class for game objects

    Attributes:
        Inherits all attributes from the Object class

    Methods:
        __init__(x, y, width, height): Initializes a Spikes instance with the given parameters
    """
    
    def __init__(self,x,y,width,height):
        """
        Initializes a Spikes instance with the given parameters.

        Args:
            x (int): The x-coordinate of the spikes' position
            y (int): The y-coordinate of the spikes' position
            width (int): The width of the spikes
            height (int): The height of the spikes
        """
        
        super().__init__(x,y,width,height, "spike")
        image = pygame.image.load("spike-sprite.png").convert_alpha()
        rect = pygame.Rect(56,72,width*2,height*2)
        surface = pygame.Surface((width*2,height*2),pygame.SRCALPHA,32)
        surface.blit(image,(0,0), rect)
        block = pygame.transform.scale_by(surface, .5) 
        self.image.blit(block, (0,0))

class Flag(Object):
    """
    A class representing a flag object in a game.

    Inherits from:
        Object: A base class for game objects

    Attributes:
        x (int): The x-coordinate of the flag
        y (int): The y-coordinate of the flag
        width (int): The width of the flag
        height (int): The height of the flag

    Methods:
        __init__(x, y, width, height): Initializes a Flag object with the given parameters
    """
    def __init__(self,x,y,width, height):
        """
        Initializes a Flag object with the given parameters

        Args:
            x (int): The x-coordinate of the flag's position
            y (int): The y-coordinate of the flag's position
            width (int): The width of the flag
            height (int): The height of the flag
        """
        super().__init__(x,y,width,height,"flag")
        image = pygame.image.load("flagpole4.png").convert_alpha()
        rect = pygame.Rect(420,0,width*12,height*28)
        surface = pygame.Surface((width*12,height*28),pygame.SRCALPHA,32)
        surface.blit(image,(0,0),rect)
        flag = pygame.transform.scale(surface,(128,386))
        self.image.blit(flag, (0,0))


def Game(window, level = 1):
    """
    Runs the game simulation with the provided models and level.

    Args:
        window: The Pygame window surface.
        models (list): A list of models used to control the players.
        level (int, optional): The level of the game to be played. Defaults to 1.

    Returns:
        list: A list containing the game results for each player.

    This function initializes the game environment, including player characters, obstacles, 
    and floor elements based on the specified level. It then runs the game simulation, 
    updating player actions and positions based on model predictions and collisions 
    with game elements. The function continues until either all players reach the end 
    of the level, time runs out, or a player dies. The function returns a list containing 
    the game results for each player, including whether they won, their final position, 
    the time taken, and whether they died.

    """
    
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
                     Spikes(256,height-floor_height+32, 32, 32), 
                     Flag(256+(64*4),height-floor_height-64-64,64,128)]
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10) if i != 4]
    elif level == 4: 
        spikes = [Spikes(256 + (32 * i), height-floor_height-32, 32, 32) for i in range(12)]
        obstacles = [SquareBlock(256 + 64,height-floor_height-64-64, 64), 
                     SquareBlock(256 - 64,height-floor_height-64, 64), 
                     SquareBlock(256 + (64 * 4),height-floor_height-(64 * 3), 64), 
                     Flag(256 + (64 * 8),height-64-floor_height-64,64,128)]
        obstacles = obstacles + spikes
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(15)]
    elif level == 5: 
        spikes = [Spikes(256 + (64 * i), height-floor_height-32, 64, 64) for i in range(6)]
        obstacles = [SquareBlock(256 + 64,height-floor_height-64-64, 64), 
                     SquareBlock(256 - 64,height-floor_height-64, 64), 
                     SquareBlock(256 + (64 * 4),height-floor_height-(64 * 3), 64), 
                     SquareBlock(256 + (64 * 5),height-floor_height-(64 * 4), 64), 
                     SquareBlock(256 + (64 * 3),height-floor_height-(64 * 5), 64), 
                     SquareBlock(256 + (64 * 2),height-floor_height-(64 * 5), 64), 
                     Flag(256 + (64 * 2),height-floor_height-(64 * 7),64,128)]
        obstacles = obstacles + spikes
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10)]

    
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
            
Game(window, level = 2)
