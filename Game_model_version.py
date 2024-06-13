#importing packages
import pygame
import math
import numpy as np
import imageio.v3 as iio
import pygame.pixelcopy
pygame.init()

#setting backround color to sky blue
backround_color = (135, 206, 235)
#setting fps cap
fps = 1000
#setting the player velocity
velocity = 4

#setting the pixel height of the floor level
floor_height = 160

#setting screen width and height
width = 600
height = 600

#setting parameters for the sightlines
sl = 100            # customizable, sightline length (default: 100)
cx = 23             # customizable, sightline center of x (default: 46)
cy = 23             # customizable, sightline center of y (default: 23)

#defining the object class
class Object():
    def __init__(self, x,y,width,height, name = "block"):
        """
        Initializer for the Object class
        Args:
            self: Object to be initialized
            x: x coordinate from left of the window
            y: y coordinate from the top of the window
            width: width of the hitbox for the Object in pixels
            height: height of the hitbox for the Object in pixels
            name: string used to identify the type of object, default "block"
        """
        #initializing a rect from the given coordinate and hitbox size
        self.rect = pygame.Rect(x,y,width,height)

        #initializing pygame surface with the given size, SRCALPHA allowing for transparency
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)

        #initializing the other variables as given
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, screen_offset):
        """
        blits the Object to the screen
        Args:
            self: Object to be blitted
            window: window where self will be blitted
            screen_offset: offset in the x direction accounting for screen scrolling
        """

        #blitting self.image to window at the objects (x,y) coordinate, accounting for screen offset
        window.blit(self.image,(self.rect.x - screen_offset, self.rect.y))


#defining function to convert from numpy array with alpha channel to pygame surface
#this function will be needed in the subclasses of Object
def make_surface(array):
    """
    takes 3d numpy array and converts it into a pygame surface
    Args:
        array: 3d numpy array representing a png image with alpha channel
    Returns:
        surface: pygame surface 
    
    """
    #initializing empty surface with the same size as the image
    surface = pygame.Surface((array.shape[0],array.shape[1]), pygame.SRCALPHA)

    #Copying the rgb channels to the surface using pixelcopy()
    pygame.pixelcopy.array_to_surface(surface, array[:,:,0:3])

    #mapping the alpha channel to the surface using memory allocation
    alpha_channel = np.array(surface.get_view("a"), copy = False)
    alpha_channel[:,:] = array[:,:,3]

    return surface

#defining the class SquareBlock, inheriting from object
class SquareBlock(Object):
    def __init__(self,x,y,width):
        """
        initializer for the SquareBlock class
        Args:
            self: SquareBlock to be initialized
            x: x coordinate to be passed to Object initializer
            y: y coordinate to be passed to Object initializer
            width: width and height vlaue to be passed to Object initializer
        """
        #calling the Object initializer
        super().__init__(x,y,width,width,"block")

        #loading png containing the block sprite and allowing for transparency
        im = iio.imread("https://raw.githubusercontent.com/stephenyu2/pic16b-final-project/main/Terrain.png")
        image = make_surface(im.swapaxes(0,1))

        #Initalixing rect with the pixel coordinates of the sprite in Terrain.png and size of the block
        rect = pygame.Rect(208,144,width,width)

        #Initializing a surface object of size (width,height), allowing for transparency
        surface = pygame.Surface((width,width),pygame.SRCALPHA)

        #blitting the subimage of Terrain.png at rect onto surface
        surface.blit(image,(0,0),rect)

        #scaling up the size of the surface by 2 times
        block = pygame.transform.scale_by(surface,2)

        #blitting the scaled surface (stored locally) onto the Object class variable image, another pygame surface
        self.image.blit(block, (0,0))

#defining class Spikes, inheriting from Object
class Spikes(Object): 
    def __init__(self,x,y,width,height):
        """
        Initializer for the Spikes object
        Args:
            self: Spikes object to be initialized
            x: x coordinate to be passed to Object initializer
            y: x coordinate to be passed to Object initializer
            width: width to be passed to Object initializer
            height: height to be passed to Object initializer
        """

        #calling Object initializer with the given parameters and name = "spike"
        super().__init__(x,y,width,height,"spike")

        #loading png containing the spike sprite and allowing for transparency
        im = iio.imread("https://raw.githubusercontent.com/stephenyu2/pic16b-final-project/main/Spike-Sprite.png")
        image = make_surface(im.swapaxes(0,1))

        #Initalixing rect with the pixel coordinates of the sprite in spike-sprite.png and size of the spike sprite
        #width and height are multiplied by 2 to account for smaller size of spike
        rect = pygame.Rect(52,72,width*2,height*2)

        #Initializing a surface object of size (2*width,2*height), allowing for transparency
        surface = pygame.Surface((width*2,height*2),pygame.SRCALPHA)

        #blitting the subimage of spike-sprite.png at rect onto surface
        surface.blit(image,(0,0), rect)

        #scaling down the size of the surface by 2 times
        block = pygame.transform.scale_by(surface, .5) 

        #blitting the scaled surface (stored locally) onto the Object class variable image, another pygame surface
        self.image.blit(block, (0,0))

#defininf the Flag class, inheriting from Object
class Flag(Object):
    def __init__(self,x,y,width, height):
        """
        Initializer for the Flag object
        Args:
            self: Flag to be initialized
            x: x coordinate to be passed to Object initializer
            y: x coordinate to be passed to Object initializer
            width: width to be passed to Object initializer
            height: height to be passed to Object initializer
        """

        #calling the Object initializer with the given parameters and name = "flag"
        super().__init__(x,y,width,height,"flag")

        #loading png containing the spike sprite and allowing for transparency
        im = iio.imread("https://raw.githubusercontent.com/stephenyu2/pic16b-final-project/main/flagpole4.png")
        image = make_surface(im.swapaxes(0,1))


        #Initalixing rect with the pixel coordinates of the sprite in flagpole.png and size of the spike sprite
        #width and height are factored to account for the larger resolution of flagpole.png
        rect = pygame.Rect(420,0,width*12,height*28)

        #Initializing a surface object of size (12*width,28*height), allowing for transparency
        surface = pygame.Surface((width*12,height*28),pygame.SRCALPHA)

        #blitting the subimage of flagpole.png at rect onto surface
        surface.blit(image,(0,0),rect)

        #scaling down the size of the surface to a specific coordinate size
        flag = pygame.transform.scale(surface,(128,386))

         #blitting the scaled surface (stored locally) onto the Object class variable image, another pygame surface
        self.image.blit(flag, (0,0))

#defining the Player class
class Player():
    def __init__(self, x , y, width, height, sprites,flag_x,flag_y):
        """
        Initializer for the Player object
        Args:
            self: Player obejct to be initialized
            x: x coordinate of starting position
            y: y coordinate of starting position
            width: width of the player hitbox
            height: height of the player hitbox
            sprites: dictionary of lists of images corresponding to the different animation cycles of the player character
                     Should have keys: "jumpright", "jumpleft", "idleleft", "idleright", "walkleft", "walkright"
            flag_x: x coordinate of the flag for the chosen level
            flag_y: y coordinate of the flag for the chosen level
        """
        #Defining class variables:

        #Initializing variables given by the initializer arguments
        self.sprites = sprites 
        self.flag_x = flag_x 
        self.flag_y = flag_y

        self.rect = pygame.Rect(x,y,width,height) #rect defining the hitbox for the character
        self.v_x = 0 #initializing x velocity to 0
        self.v_y = 0 #intializing x velocity to 0
        self.canjump = False #initizing state of the character as being unable to jump
        self.direction = "right" #initialing the direction of the character as facing right
        self.animation_frame= 0 #initialing the animation frame count as frame 0
        self.fall_count = 0 #initializing the number of frames since touching the ground as 0
        self.win = False #intialing the player win condition as false
        self.died = False #initializing the state of the player as alive
        self.time = 0 #initializing the frame since spawning as 0
        self.sightlines = [] #initializing an empty list used to store pygame line objects later on
        self.distances = [sl,sl,sl,sl,sl,sl,sl,sl] #intializing a list of lengths for the sightlines, given by a global variable
        self.types = [0,0,0,0,0,0,0,0] #initializing a list of object types representing what type each sightline is detecting, encoded as integers
        self.name_mapping = {"block": 0, "spike": 1, "flag": 2} #initializing a dict which decodes the integer Object types into corresponding names


    #DEFINING CLASS FUNCTIONS:

    #defining jump function
    def jump(self):
        """
        makes the player jump by assigning y velocity to a large upward value
        Args:
            self: player to jump
        """
        #sets player velocity to a high upward value (negative is up in pygame)
        self.v_y = -6.6
        #resets animation frame, as player will be entering the jump animation
        self.animation_frame = 0

    #defining move function
    def adjust_position(self,v_y,v_x):
        """
        Moves the player by their velocity vector
        Args:
            self: player to be moved
            v_y: y increment to move
            v_x: x increment to mvoe
        """
        #adjusting position of player hitbox by given increments
        self.rect.x += v_x
        self.rect.y += v_y

    #defining a function which handles the necessary frame by frame adjustments to the player
    def next_frame(self,fps):
        """
        function which increments the state of the player by one frame and checks/updates all player variables
        which can change frame by frame.

        Args:
            self: player to be updated
            fps: fps of the game loop, (globally defined variable)
        """

        #gravity simulation, moving the player down by more the longer the player has been in the air
        self.v_y += max(.3,(self.fall_count/fps))

        #adjusting the players position by their velocity vector
        self.adjust_position(self.v_y,self.v_x)

        #incrementing the number of frames the player has been in the air
        self.fall_count += 1

        #initializing the default state to "idle"
        state = "idle"

        #checks if the player is falling quickly or has spent their jump, 
        # setting the players state to "jump" in either case
        if abs(self.v_y)>.7 or not self.canjump:
            state = "jump"

        #if the player is not jumping, sets the player state to "walk" 
        # as long as the player is moving in the x direction
        elif self.v_x !=0:
            state = "walk"

        #if the player has won the game sets state to "idle" as a visual indicator
        if self.win:
            state = "idle"

        #string concatenation which adds the direction information ("left" or "right") of the player to state 
        directional_state = state + self.direction

        #selects the correct animation (list of images) to be playing using directional_state as the key to the sprites class variable
        state_frames = self.sprites[directional_state]

        #setting the animation to move to the next frame every 5 frames and loop when done playing
        frame_number = int((self.animation_frame / 5))%len(state_frames)

        #selecting the image at the correct animation index
        self.sprite = state_frames[frame_number]

        #incrementing the animation_frame by one
        self.animation_frame += 1

        #resets the players x velocity to zero
        self.v_x = 0

        #aligning the animation image with the hitbox of the player
        self.rect = self.sprite.get_rect(topleft = (self.rect.x,self.rect.y))
    
    #defining a function to handle all required collision calculations
    def check_collision(self,objects,keys):
        """
        Checks the x and y collisions of the player as well as the collisiong calculations for the sightlines of the player
        Args:
            self: player in question
            objects: list of all objects in the level with collision
            keys: list of the three outputs of the neural network

        """
        #CHECKING LEFT X COLLISION:

        #moving the player to the left by the x velocity
        self.adjust_position(0,-4)
        #intializing a bool to track if the player hits a wall
        wall_left = False

        #looping over all objects in the level
        for object in objects:
            #checks in the hitboxes of the player and object collide (player is shifted slightly to remove ground collision issues)
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-1), object.rect):
                wall_left = True
                #if the player hits a spike they die
                if object.name == "spike":
                        self.died = True
                #if the player has not died and hits a flag then they win
                elif object.name == "flag" and self.died == False:
                        self.win = True
                #only records collision for the first object hit to save computing time, 
                #a shortcut which does not introduce any bugs with simple level geometry
                break

        #moving the player back over to the right by the x velocity (net movement)
        self.adjust_position(0,8)

        #intializing a bool to track if the player hits a wall
        wall_right = False
        #looping over all objects in the level
        for object in objects:
            #checks in the hitboxes of the player and object collide (player is shifted slightly to remove ground collision issues)
            if pygame.Rect.colliderect(self.rect.move(0,1), object.rect) and pygame.Rect.colliderect(self.rect.move(0,-2), object.rect):
                wall_right = True
                #if the player hits a spike they die
                if object.name == "spike":
                        self.died = True
                #if the player has not died and hits a flag then they win
                elif object.name == "flag":
                        self.win = True
                #only records collision for the first object hit to save computing time, 
                #a shortcut which does not introduce any bugs with simple level geometry
                break

        #returns the players position
        self.adjust_position(0,-4)

        #checks if the left inclination of the model is greater than the right inclination and there is no obstacle in the left direction
        if keys[0,0]>keys[0,1] and not wall_left:
            #sets x velocity to be leftward
            self.v_x = -velocity

            #if the character was not already facing left, the model is turned around and the walking animation is reset
            if self.direction != "left":
                self.direction = "left"
                self.animation_frame = 0

        #else checks if the right inclination of the model is greater than the left inclination and there is no obstacle in the right direction
        elif keys[0,1]>keys[0,0] and not wall_right:
            #sets x velocity to be rightward
            self.v_x = velocity

            #if the character was not already facing right, the model is turned around and the walking animation is reset
            if self.direction != "right":
                self.direction = "right"
                self.animation_frame = 0

        #resets the sight distances and block types detected
        self.distances = [sl,sl,sl,sl,sl,sl,sl,sl]
        self.types = [0,0,0,0,0,0,0,0]

        #sets the sightlines class variable to a list of lists formatted as 8 pygame lines evenly spaced around the circle
        self.sightlines = [[(self.rect.x+cx,self.rect.y+cy),(self.rect.x+cx+math.sin(.25*i*math.pi)*sl,self.rect.y+cy+math.cos(.25*i*math.pi)*sl),3] for i in range(8)]
        
        #looping over every object in the level
        for object in objects:
            #checks if the player collides vertically
            if pygame.Rect.colliderect(self.rect,object.rect):
                #if the player is moving down then the player is shifted up so as not to collide with any object
                if self.v_y > 0:
                    #shifting player to the top of collided object
                    self.rect.bottom = object.rect.top
                    #reset vertical velocity an fall timer
                    self.v_y = 0
                    self.fall_count = 0
                    #player is grounded and therefore regains the ability to jump
                    self.canjump = True
                
                #if the player is moving down then the player is shifted up so as not to collide with any object
                if self.v_y < 0:
                    #shifting player to the bottom of collided object
                    self.rect.top = object.rect.bottom
                    #resets vertical velocity
                    self.v_y = 0

            #loops over the index of each sight line
            for i in range(8):
                #if the object collides with the line, returns the coordinate along the line for which the line collides
                x = object.rect.clipline(self.sightlines[i][0][0],self.sightlines[i][0][1],self.sightlines[i][1][0],self.sightlines[i][1][1])

                #if collision occurs:
                if x != ():
                    #distance is calculated as the length of the line until the collision point
                    start = x[0]
                    d = math.sqrt((start[0] - self.rect.x-cx)**2+(start[1] - self.rect.y-cy)**2)
                #otherwise distance is caluculated as the full length of the sight line
                else: d = sl

                #if the sollision distance is less than the collision distance for any object in the level so far,
                # it is set to be the distance at the corresponding index
                if d < self.distances[i]:
                    self.distances[i] = d
                    #the name of the closest object is then encoded as an integer using the name_mapping dict,
                    # and stored as the type of object at the corresponding index
                    self.types[i] = self.name_mapping[object.name]
    
    #defining a function to draw the player and sightlines onto the screen
    def draw(self, window, screen_offset):
        """
        blits the player and their sightlines to the window
        Args:
            self: player in question
            window: window on which the sighlines and player sprite will be displayed
            screen_offset: x direction offset to account for the screen scrolling left and right
        """

        #blitting the player sprite at the players position offset by screen_offset
        window.blit(self.sprite, (self.rect.x - screen_offset,self.rect.y))

        #looping over the index of each sightline
        for i in range(8):
            #setting rgb values:
            #blue if the line intersects a block
            if self.distances[i] < sl and self.types[i] == 0:
                x = 0
                y = 0
                z = 255
            #red if the line intersects a flag or spike
            elif self.distances[i] < sl: 
                x = 255
                y = 0
                z = 0
            #green if the line intersects nothing
            else:
                x = 0
                y = 255
                z = 0
            #using the pygame draw function to blit the line with the correct color and screen offset
            pygame.draw.line(window,(x,y,z),tuple(map(lambda i, j: i + j, self.sightlines[i][0], (-screen_offset,0))),tuple(map(lambda i, j: i + j, self.sightlines[i][1], (-screen_offset,0))),self.sightlines[i][2])


#defining the function which implements the main frame loop
def Game(window,models,level = 1, modeltype = 1):
    """
    launches the game into a new window and runs a list of models as different players simultaneously. 
    Closes after every model has died or until the maximum number of frames is reached.
    Also tracks the performance of each model in

    Args:
        window: window on which the game is drawn
        models: list of neural networks each of which predict key presses each frame to control a player character
        level: accepts integers 1 - 5. Controls which level the models will play
        modeltype: accpets integers 0 - 4. Controls what inputs the models receive to inform their predictions
    Returns:
        list of lists containing data on the performance of each model.
        data includes player position, dead/alive state, win/lose state, and time spent reaching the flag
    """
    #sets the name of the window
    pygame.display.set_caption("1 million Kirby's fail at walking")  

    #initializing a Clock object to standardize framerate across devices
    clock = pygame.time.Clock() 


    #CONSTRUCTING THE ANIMATIONS USING A SPRITE SHEET:

    #loading the sprite sheet for the player character, allowing for transparency with rbga
    im = iio.imread("https://raw.githubusercontent.com/stephenyu2/pic16b-final-project/main/kirby.png")
    kirbypng = make_surface(im.swapaxes(0,1))
    
    #defining the dict which will store a list of sprites for each animation
    animation_dict = {}
    #names of the three animations implemented into the program
    sprite_names = ["walk", "jump", "idle"]

    #constructing the walk animation
    animation_dict["walk"] = []
    #looping over the number of frames in the animation
    for i in range(10):
        #constructing a surface and blitting the correct subsprite onto the surface
        surface = pygame.Surface((23,23), pygame.SRCALPHA)
        rect = pygame.Rect(8+ i*23, 51, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        #appending the surface to the list at the "walk" key
        animation_dict["walk"].append(pygame.transform.scale_by(surface,2))

    #constructing the jump animation
    animation_dict["jump"] = []
    #looping over the number of frames in the animation
    for i in range(9):
        #constructing a surface and blitting the correct subsprite onto the surface
        surface = pygame.Surface((23,23), pygame.SRCALPHA)
        rect = pygame.Rect(7+ int(i*24.3), 130, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        #appending the surface to the list at the "jump" key
        animation_dict["jump"].append(pygame.transform.scale_by(surface,2))

    #constructing the idle animation
    animation_dict["idle"] = []
    #looping over the x position of subsprites in the animation
    for i in [10,10,39,39,66,66,96,96,124]:
        #constructing a surface and blitting the correct subsprite onto the surface
        surface = pygame.Surface((23,23), pygame.SRCALPHA)
        rect = pygame.Rect(i, 215, 23,23)
        surface.blit(kirbypng, (0,0), rect)
        #appending the surface to the list at the "idle" key
        animation_dict["idle"].append(pygame.transform.scale_by(surface,2))

    #for each constructed animation adds a second flipped version, and adds directional information to the dict keys
    for name in sprite_names:
        #saving original as right facing animation
        animation_dict[name+"right"] = animation_dict[name]
        #saving flipped version as left facing animation
        animation_dict[name+"left"] = [pygame.transform.flip(sprite,True,False) for sprite in animation_dict[name]]

    #constructing Player object for each model in models
    players = [Player(64,256,64,64,animation_dict,512,height-64-128) for i in range(len(models))]

    #CONSTRUCTING LEVELS:

    #for each choice of level, initializes a list of obstacles and a line of blocks to be the floor
    #exact construction is what determines the geometry and design of each level
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
                     Spikes(256+32,height-floor_height+32, 32, 32),
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
        spikes = [Spikes(256 + (32 * i), height-floor_height-32, 32, 32) for i in range(12)]
        obstacles = [SquareBlock(256 + 64,height-floor_height-64-64, 64), 
                     SquareBlock(256 - 64,height-floor_height-64, 64), 
                     SquareBlock(256 + (64 * 4),height-floor_height-(64 * 3), 64), 
                     SquareBlock(256 + (64 * 5),height-floor_height-(64 * 4), 64), 
                     SquareBlock(256 + (64 * 3),height-floor_height-(64 * 5), 64), 
                     SquareBlock(256 + (64 * 2),height-floor_height-(64 * 5), 64), 
                     Flag(256 + (64 * 2),height-floor_height-(64 * 7),64,128)]
        obstacles = obstacles + spikes
        floor = [SquareBlock(64*i, height-floor_height,64) for i in range(10)]
    
    #assembles the models and Player objects into a 2d numpy array, with each row describing a model/Player pair
    player_array = np.array([models, players])

    #initializing the screen_offset at zero
    screen_offset = 0

    #setting the time limit at 200 frames
    time_limit = 200
    #initializing a variable to track how many frames have elapsed
    time = 0

    #FRAME LOOP BEGINS HERE
    run = True
    while run:
        #increment the time
        time +=1
        #stardardizing fps with clock.tick (not relevant for training model as computational time makes the game run significantly slower than the fps cap)
        clock.tick(fps)

        #checks if the window has been closed manually and ends the loop early
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        #draws the backround color per the global variable backround_color
        window.fill(backround_color)
        
        #initializes the stop bool which tracks if every model has died
        #note it starts as true and will be overwritten if any model is still alive
        stop = True
        #looping over the number of models to simulate
        for i in range(len(player_array[0,:])):
            #depending on the construction of the model, initializes input_data
            if modeltype == 2:
                #input_data contains character position, velocity, flag position, and sightline information
                input_data = np.array([[player_array[1, i].rect.x, player_array[1, i].rect.y,
                                    player_array[1, i].v_x, player_array[1, i].v_y,
                                    int(player_array[1, i].canjump), player_array[1, i].flag_x,
                                    player_array[1, i].flag_y] + player_array[1, i].distances
                                   + player_array[1, i].types])
            elif modeltype == 1:
                #input_data contains character position, velocity, and flag position
                input_data = np.array([[player_array[1, i].rect.x, player_array[1, i].rect.y,
                                    player_array[1, i].v_x, player_array[1, i].v_y,
                                    int(player_array[1, i].canjump), player_array[1, i].flag_x,
                                    player_array[1, i].flag_y]])
            
            elif modeltype == 3:
                #input_data contains sightline information
                input_data = np.array([player_array[1, i].distances
                                   + player_array[1, i].typesw])
            
            #stores the prediction of the model on input_data
            keys = player_array[0, i].predict(input_data, verbose=0)
        
            #if the models jump prediction meets a threshhold and the Player is in a state capable of jumping,
            #then the Player associated to the model jumps
            if keys[0,2]>.5 and player_array[1,i].canjump:
                player_array[1,i].jump()
                #after jumping the Player is set to be unable to jump again (until grounded)
                player_array[1,i].canjump = False

            #next_frame is called on the Player
            player_array[1,i].next_frame(fps)
            #check_collision is called on the Player
            player_array[1,i].check_collision(floor+obstacles,keys)

            #if the player has not died then their sprite is blitted to the window
            if not player_array[1,i].died:
                player_array[1,i].draw(window, screen_offset)
                #if this if-statement is entered then not every model has died, so stop is set to False
                stop = False
            
            #Player time variable is incremented
            player_array[1,i].time += 1

            #If the player has won then the time is deincremented, such that Player.time stores the number of frames until winning
            if player_array[1,i].win:
                player_array[1,i].time -= 1
            
        #if every model has died then the time is incremented past its limit such that the frame loop will break
        if stop == True:
            time += time_limit



        #blits all obstacles and the floor to the window
        for object in obstacles+floor:
            object.draw(window, screen_offset)

        #updates the display, drawing all blitted objects and overwriting the objects drawn on the last frame
        pygame.display.update()

        #if the player array is not empty (which it never is)
        if player_array[0].size:
            #stores the Player with the largets x coordinate
            camera_tracked = player_array[1,np.argmax([player.rect.right for player in player_array[1,:]])]

            #if the rightmost Player is too close to either side of the screen then the x velocity (a constant) is added to the screen_offset
            if (camera_tracked.rect.right - screen_offset) > width - 150 and camera_tracked.v_x > 0:
                #if camera_tracked is too close to the right, shifts the level to the left
                screen_offset += camera_tracked.v_x
            if (camera_tracked.rect.left - screen_offset) < 150 and camera_tracked.v_x < 0:
                #if camera_tracked is too close to the right, shifts the level to the left
                screen_offset += camera_tracked.v_x
        
        #loops over the Players
        for i in range(len(player_array[1,:])):
            #if the Players y coordinate is too high then then that player dies to the void
            if player_array[1,i].rect.y > height:
                player_array[1,i].died = True

        #if the time_limit has been reached then the while loop ends after this interation
        if time > time_limit:
            run = False

    #convert the numpy array to a list
    data_array = list(player_array[1,:])
    #returns a list containing the player metrics for each model
    return [[player.win,player.rect.x,time,player.died] for player in data_array]