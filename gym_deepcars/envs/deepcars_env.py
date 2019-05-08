# DeepCars environment registered for the OpenAI gym

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import random, os
import numpy as np
import pygame
from pygame.locals import *

import skimage as skimage
from skimage import transform, color, exposure

# To show output image
import time
from scipy.misc import toimage
# =======================================================================================================================
# -------------------------------------------Global Parameter values----------------------------------------------------
# =======================================================================================================================

DefaultTextColor = (255, 97, 3)
BackgroundColor = (255, 255, 255)
FPS = 100

IMAGE_SCALE_WIDTH = 160
IMAGE_SCALE_HEIGHT = 210

Horiz_Move_Rate = 4
AddNewCarRate = 1
CarsMinSpeed = 2  # Min. relative speed for the other cars wrt to the PlayerSpeed
CarsMaxSpeed = 2  # Max. relative speed for the other cars wrt to the PlayerSpeed
PlayerSpeed = 8  # Player's speed wrt to side walls (ground speed)

CarWidth = 50
CarHeight = 100
SpaceWidth = 5  # Width of space between objects, e.g. btw car and line/wall
LineWidth = 5  # Width of the lines in between the lanes
WallWidth = 50  # Width of the walls on the left and right sides
NoOfLanes = 5

MaxCarsInLane = 10  # Maximum number of cars vertically in one lane (for window size setting)

ActionList = ['Left', 'Stay', 'Right']

# Define window's dimensions wrt objects dimensions
WindowWidth = (CarWidth + 2 * SpaceWidth) * NoOfLanes + LineWidth * (NoOfLanes - 1) + 2 * WallWidth
WindowHeight = CarHeight * MaxCarsInLane + 2 * SpaceWidth + (MaxCarsInLane - 1) * LineWidth

# Calculate the x coordinate of top-right pixel of cars for staying in all lanes
LaneXCoorVec = []
for i in range(NoOfLanes):
    tempX = WallWidth + SpaceWidth + i * (CarWidth + SpaceWidth + LineWidth + SpaceWidth)
    LaneXCoorVec.append(tempX)

# No of pixels in between the vertical grids
NoOfHorGridPixels = LaneXCoorVec[1] - LaneXCoorVec[0]

# Calculate the y coordinate of top-right pixel of cars for staying in all grid rectangles
LaneYCoorVec = []
for i in range(MaxCarsInLane):
    tempY = SpaceWidth + i * (CarHeight + SpaceWidth + LineWidth + SpaceWidth)
    LaneYCoorVec.append(tempY)

# No of pixels in between the vertical grids
NoOfVerGridPixels = LaneYCoorVec[1] - LaneYCoorVec[0]


# =======================================================================================================================
# -------------------------------------------Grid World Class-----------------------------------------------------------
# =======================================================================================================================

class DeepCarsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.MainClock = 0
        self.WindowSurface = 0
        self.font = 0
        self.PlayerImage = 0
        self.CarsImageVec = 0
        self.LineImage = 0
        self.HorizLineImage = 0
        self.LeftWall = 0
        self.RightWall = 0
        self.LineRecSamples = []
        self.HorizLineRecSamples = []

        self.observation_space = spaces.Box(low=0, high=255, shape=(IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT, 3),
                                            dtype=np.uint8)
        self.action_space = spaces.Discrete(len(ActionList))

        self.CarAddCounter = AddNewCarRate
        self.PassedCarsCount = 1  # No. of cars that the agent has passed (start from 1 to avoid deving to 0 in SuccessRate)
        self.HitCarsCount = 0  # No. of cars that are hit by player
        self.OtherCarsVec = []
        self.PlayerLane = round((NoOfLanes - 1) / 2)
        self.PlayerRect = 0
        print('Game images are going to be loaded from: {}/image/'.format(os.getcwd()))

    def Self_Param_Initialization(self):
        self.MainClock = 0
        self.WindowSurface = 0
        self.font = 0
        self.PlayerImage = 0
        self.CarsImageVec = 0
        self.LineImage = 0
        self.HorizLineImage = 0
        self.LeftWall = 0
        self.RightWall = 0
        self.LineRecSamples = []
        self.HorizLineRecSamples = []

        self.observation_space = spaces.Box(low=0, high=255, shape=(IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT, 3),
                                            dtype=np.uint8)
        self.action_space = spaces.Discrete(len(ActionList))

        self.CarAddCounter = AddNewCarRate
        self.PassedCarsCount = 1  # No. of cars that the agent has passed (start from 1 to avoid deving to 0 in SuccessRate)
        self.HitCarsCount = 0  # No. of cars that are hit by player
        self.OtherCarsVec = []
        self.PlayerLane = round((NoOfLanes - 1) / 2)
        self.PlayerRect = 0

    def close(self):
        pygame.quit()
        print("The game is terminated")
        # sys.exit()

    def reset(self):  # Get initial state
        self.Self_Param_Initialization()        # Initialize self parameters
        self.PygameInitialize()
        # a = self.action_space.sample()  # Take a random action
        ImageData, Reward, done, __ = self.step(1)
        # obs = self.observation_space.sample()   # Sample an observation with the correct dimensions and format
        # obs[:] = 0                              # Set the observations to zero as the initial observation in game
        return ImageData

    def DrawText(self, text, font, TextColor, surface, x, y):
        textobj = font.render(text, 1, TextColor)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def PlayerHasHitBaddie(self, PlayerRect, baddies):
        for b in baddies:
            if PlayerRect.colliderect(b['rec']):
                return True
        return False

    def PygameInitialize(self):
        # set up pygame, the window, and the mouse cursor
        # You ca do the following dummies in main also
        # os.environ['SDL_AUDIODRIVER'] = "dummy"           # Create a AUDIO DRIVER to not produce the pygame sound
        # os.environ["SDL_VIDEODRIVER"] = "dummy"           # Create a dummy window to not show the pygame window
        pygame.init()
        self.MainClock = pygame.time.Clock()
        self.WindowSurface = pygame.display.set_mode((WindowWidth, WindowHeight))
        pygame.display.set_caption('Deep Cars Grid World (ITUarc)')
        pygame.mouse.set_visible(False)
        self.font = pygame.font.SysFont(None, 30)

        # images:
        # I know that this is not the best approach to get env images :)
        # Requirement: image folder should be in os path (same directory as main script)
        # print('Game images are going to be loaded from: {}/image/'.format(os.getcwd()))

        self.PlayerImage = pygame.image.load('image/MyCar')
        self.PlayerImage = pygame.transform.scale(self.PlayerImage, (CarWidth, CarHeight))

        Car1Image = pygame.image.load('image/Car1')
        Car1Image = pygame.transform.scale(Car1Image, (CarWidth, CarHeight))
        Car2Image = pygame.image.load('image/Car2')
        Car2Image = pygame.transform.scale(Car2Image, (CarWidth, CarHeight))
        Car3Image = pygame.image.load('image/Car3')
        Car3Image = pygame.transform.scale(Car3Image, (CarWidth, CarHeight))
        Car4Image = pygame.image.load('image/Car4')
        Car4Image = pygame.transform.scale(Car4Image, (CarWidth, CarHeight))
        Car5Image = pygame.image.load('image/Car5')
        Car5Image = pygame.transform.scale(Car5Image, (CarWidth, CarHeight))
        Car6Image = pygame.image.load('image/Car6')
        Car6Image = pygame.transform.scale(Car6Image, (CarWidth, CarHeight))

        self.CarsImageVec = [Car1Image,Car2Image,Car3Image,Car4Image,Car5Image, Car6Image]

        LeftWallImage = pygame.image.load('image/left')
        RightWallImage = pygame.image.load('image/right')

        self.LineImage = pygame.image.load('image/black')
        self.LineImage = pygame.transform.scale(self.LineImage, (LineWidth, WindowHeight))

        # Define walls
        self.LeftWall = {'rec': pygame.Rect(0, -2 * WindowHeight, WallWidth, 3 * WindowHeight),
                         'surface': pygame.transform.scale(LeftWallImage, (WallWidth, 3 * WindowHeight))
                         }
        self.RightWall = {'rec': pygame.Rect(WindowWidth - WallWidth, -2 * WindowHeight, WallWidth, 3 * WindowHeight),
                          'surface': pygame.transform.scale(RightWallImage, (WallWidth, 3 * WindowHeight))
                          }

        # Define line rectangles
        for i in range(NoOfLanes - 1):
            LineXCoord = WallWidth + i * LineWidth + (i + 1) * (SpaceWidth + CarWidth + SpaceWidth)
            NewLineRec = pygame.Rect(LineXCoord, 0, LineWidth, WindowHeight)
            self.LineRecSamples.append(NewLineRec)

        for i in range(MaxCarsInLane - 1):
            LineYCoord = LaneYCoorVec[i + 1]
            NewLineRec = pygame.Rect(0, LineYCoord, WindowWidth, LineWidth)
            self.HorizLineRecSamples.append(NewLineRec)

        self.PlayerRect = self.PlayerImage.get_rect()
        self.PlayerRect.topleft = (LaneXCoorVec[self.PlayerLane], LaneYCoorVec[MaxCarsInLane - 2])

        # print('The game has initiated')

    # Prepare the game screen as the observation vector suitable for Keras
    def keras_preprocess(self, ImageData):
        ImageData = np.flipud(ImageData)
        ImageData = ImageData[WallWidth:WindowWidth - WallWidth, CarHeight + 4 * SpaceWidth:]
        ImageData = skimage.color.rgb2gray(ImageData)
        ImageData = skimage.transform.resize(ImageData, (IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT))
        ImageData = skimage.exposure.rescale_intensity(ImageData, out_range=(0, 255))
        # In Keras, need to reshape
        ImageData = ImageData.reshape(1, ImageData.shape[0], ImageData.shape[1], 1)  # 1*60*60*1
        return ImageData

    def baselines_preprocess(self, ImageData):
        ImageData = np.flipud(ImageData)
        ImageData = ImageData[WallWidth:WindowWidth - WallWidth, CarHeight + 4 * SpaceWidth:]   # Crop useful space
        ImageData = skimage.transform.resize(ImageData, (IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT, 3))
        ImageData = skimage.exposure.rescale_intensity(ImageData, out_range=(0, 255))
        return ImageData

    def step(self, ActionIndex=1, TrainingFlag=True):

        Action = ActionList[ActionIndex]  # Pick the action from action list

        # ==============================================Define new cars======================================================
        if self.CarAddCounter >= AddNewCarRate:
            self.CarAddCounter = 0
            NewCarLaneNo = random.randint(0, NoOfLanes - 1)
            NewCar = {'rec': pygame.Rect(LaneXCoorVec[NewCarLaneNo], 0 - CarHeight - SpaceWidth - LineWidth, CarWidth,
                                         CarHeight),
                      'speed': NoOfVerGridPixels,
                      'XCoord': NewCarLaneNo,  # x coordinate in grid world
                      'YCoord': MaxCarsInLane - 1,  # y coordinate in grid world
                      'surface': self.CarsImageVec[random.randint(0, len(self.CarsImageVec)-1)] # Randomize cars visuals
                      }
            self.OtherCarsVec.append(NewCar)
        self.CarAddCounter += 1

        # =================================================Movements=========================================================
        # Side walls
        self.LeftWall['rec'].move_ip(0, NoOfVerGridPixels)
        self.RightWall['rec'].move_ip(0, NoOfVerGridPixels)

        # Move the player left
        if Action is 'Left' and self.PlayerLane is not 0:
            self.PlayerRect.move_ip(-1 * NoOfHorGridPixels, 0)
            self.PlayerLane -= 1
            # print('Player car lane number has changed to ', step.PlayerLane + 1)

        # Move the player right
        if Action is 'Right' and self.PlayerLane is not NoOfLanes - 1:
            self.PlayerRect.move_ip(+1 * NoOfHorGridPixels, 0)
            self.PlayerLane += 1
            # print('Player car lane number has changed to ', step.PlayerLane + 1)

        # Move other cars backward
        for Car in self.OtherCarsVec:
            Car['rec'].move_ip(0, +1 * Car['speed'])
            Car['YCoord'] -= 1

        # ================================Remove the other cars that pass the game window====================================
        for Car in self.OtherCarsVec:
            # if Car['rec'].top > WindowHeight + SpaceWidth or Car['rec'].top + CarHeight < - SpaceWidth:
            if Car['YCoord'] < 0:
                self.OtherCarsVec.remove(Car)
                self.PassedCarsCount += 1

        # ==================================================================================================================
        # ------------------------------------------------Game state----------------------------------------------------
        # ==================================================================================================================
        self.render()
        ImageData = pygame.surfarray.array3d(pygame.display.get_surface())

        # ImageData = self.keras_preprocess(ImageData)
        ImageData = self.baselines_preprocess(ImageData)

        # # Show the output image
        # toimage(ImageData).show()
        # time.sleep(1)

        # ==================================================================================================================
        # --------------------------------------------Reward function---------------------------------------------------
        # ==================================================================================================================
        done = False
        if self.PlayerHasHitBaddie(self.PlayerRect, self.OtherCarsVec):
            Reward = -1000
            done = True
            print('Passed cars: {}'.format(self.PassedCarsCount))
            self.PassedCarsCount -= 1
            self.HitCarsCount += 1
        else:
            Reward = 1

        # ==================================================================================================================
        # -----------------------------------------------ESC for Terminate--------------------------------------------------
        # ==================================================================================================================
        # done = False
        # for event in pygame.event.get():
        #     if event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:  # escape quits
        #             done = True
        #             self.close()

        # return np.array(ImageData), Reward, done, {} #self.HitCarsCount, self.PassedCarsCount
        # Accuracy = round(self.PassedCarsCount / (self.PassedCarsCount + self.HitCarsCount) * 100, 2)
        # time.sleep(1)
        return ImageData, Reward, done, {}  # self.HitCarsCount, self.PassedCarsCount

    def render(self, mode='human', close=False):
        # =======================================Draw the game world on the window===========================================
        self.WindowSurface.fill(BackgroundColor)

        for i in range(0, len(self.LineRecSamples)):
            self.WindowSurface.blit(self.LineImage, self.LineRecSamples[i])

        for Car in self.OtherCarsVec:
            self.WindowSurface.blit(Car['surface'], Car['rec'])

        self.WindowSurface.blit(self.PlayerImage, self.PlayerRect)

        self.DrawText('Cars passed: %s' % (self.PassedCarsCount), self.font, DefaultTextColor, self.WindowSurface,
                      WallWidth + SpaceWidth,
                      SpaceWidth)
        self.DrawText('Cars hit: %s' % (self.HitCarsCount), self.font, DefaultTextColor, self.WindowSurface,
                      WallWidth + SpaceWidth,
                      10 * SpaceWidth)

        self.WindowSurface.blit(self.LeftWall['surface'], self.LeftWall['rec'])
        self.WindowSurface.blit(self.RightWall['surface'], self.RightWall['rec'])

        # ============Move walls' Y coordinate to -2*WindowHeight when their top left pixel reached to y = 0================
        if self.LeftWall['rec'].topleft[1] >= - WindowHeight / 2:
            self.LeftWall['rec'].topleft = [0, -2 * WindowHeight]
            self.RightWall['rec'].topleft = [WindowWidth - WallWidth, -2 * WindowHeight]

        # ==============================================Environment update==================================================
        SuccessRate = round(100 * self.PassedCarsCount / (self.PassedCarsCount + self.HitCarsCount), 2)

        self.DrawText('Accuracy: %% %s' % (SuccessRate), self.font, DefaultTextColor, self.WindowSurface,
                      WallWidth + SpaceWidth,
                      20 * SpaceWidth)

        pygame.display.update()
        self.MainClock.tick(FPS)