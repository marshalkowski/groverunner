import time
import random
import grovepi
import math
from grovepi import *
from grove_rgb_lcd import *

dial_pin = 0

playerPosition = 1;
screenTiles = ("P" + " " * 15) * 2
obstacles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
obstacleTimer = 0
maxObstacleTimer = 4
oldDialSetting = -10
frameRate = 0.2
score = 0
density = 1;

def render_screen():
    render_player()
    render_obstacles()
    setText(screenTiles)
    
def render_player():
    global screenTiles
    if playerPosition == 1:
        screenTiles = '\'' + screenTiles[1:]
    elif playerPosition == 2:
        screenTiles = ',' + screenTiles[1:]
    else:
        screenTiles = ' ' + screenTiles[1:]
    
    if playerPosition == 4:
        screenTiles = screenTiles[:16] + '\'' + screenTiles[17:]
    elif playerPosition == 8:
        screenTiles = screenTiles[:16] + ',' + screenTiles[17:]
    else:
        screenTiles = screenTiles[:16] + ' ' + screenTiles[17:]
        
def render_obstacles():
    global screenTiles
    #generate last column
    newTop = ' '
    newBottom = ' '
    if (obstacles[14] & 1) and (obstacles[14] & 2):
        newTop = '8'
    elif obstacles[14] & 1:
        newTop = chr(223)
    elif obstacles[14] & 2:
        newTop = 'o'
    
    if (obstacles[14] & 4) and (obstacles[14] & 8):
        newBottom = '8'
    elif obstacles[14] & 4:
        newBottom = chr(223)
    elif obstacles[14] & 8:
        newBottom = 'o'
        
    #keep first column, shift column 2-15 down 1, add new column
    screenTiles = screenTiles[0:1] + screenTiles[2:16] + newTop + screenTiles[16:17] + screenTiles[18:] + newBottom

def get_player_input():
    global oldDialSetting
    global playerPosition
    newDialSetting = grovepi.analogRead(dial_pin)
    if abs(oldDialSetting - newDialSetting) > 5:
        oldDialSetting = newDialSetting
        playerPosition = 2 ** (oldDialSetting // 256)
    
def update_obstacles():
    global obstacles
    obstacles = obstacles[1:] + generate_obstacle()

def generate_obstacle():
    global obstacleTimer
    if obstacleTimer == 0:
        obstaclePosition = 0
        obstacleTimer = maxObstacleTimer
        for i in range(0, density):
            obstaclePosition = obstaclePosition | 2 ** random.randint(0,3)
        #ensure there is always at least 1 gap
        if obstaclePosition == 15:
            obstaclePosition -= 2 ** random.randint(0,3)
        print(obstaclePosition)
        return [obstaclePosition]
    else:
        obstacleTimer -= 1
        return [0]
    
def collision():
    return playerPosition & obstacles[0]

def main():

    global score
    global density
    global maxObstacleTimer
    global frameRate

    pinMode(dial_pin, "INPUT")
    setText("  GROVE Runner  ")
    setRGB(0,255,128)

    time.sleep(1)
    
    while True:
        try:
            #check for input
            get_player_input()
            
            #check for collision
            if collision():
                break;
            
            score += 1
            if score % 100 == 0:
                if density < 5:
                    density += 2
                elif maxObstacleTimer > 2:
                    maxObstacleTimer -= 1
                else
                    frameRate -= 0.1
            
            update_obstacles()
            
            render_screen()
            
            time.sleep(frameRate)
                
        except IOError:
            print("Error")
    
    setRGB(255,255,0)
    time.sleep(0.75)
    setRGB(128,0,64)
    setText("   GAME OVER    " + "   SCORE: " + str(score))

main()
        

    