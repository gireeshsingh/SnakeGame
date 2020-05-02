import pygame
from pygame.locals import *
from random import randint
import pygame
import time
 
pygame.init() 

class Apple:
    x = 0
    y = 0
    step = 42

    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player:
    x = [0]
    y = [0]
    step = 42
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*42
       self.x[2] = 2*42
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        #print(str(x1)+":"+ str(x2)+":"+str(y1)+":"+str(y2)+":")
        if(x1<-120 or x1>1002 or x2<-120 or x2>1002 or y1<-120 or y1>602 or y2<-120 or y2>602):
            return True
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:

    windowWidth, windowHeight = 1000, 600
    player = 0
    apple = 0
    level = 1
    speed = 50.0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)
 
    def on_init(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)
        self.level=1
        self.speed=50.0
        
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Snake Game')
        self._running = True
        self._image_surf = pygame.image.load("block.jpg").convert()
        self._apple_surf = pygame.image.load("apple.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],42):
                self.apple.x = randint(2,9) * 42
                self.apple.y = randint(2,9) * 42
                self.player.length = self.player.length + 1
                if(self.player.length>15):
                    self.level = 2
                    self.speed = 45.0
                elif(self.player.length>20):
                    self.level = 3
                    self.speed = 40.0
                elif(self.player.length>25):
                    self.level = 4
                    self.speed = 35.0
                elif(self.player.length>30):
                    self.level = 5
                    self.speed = 30.0
                elif(self.player.length>35):
                    self.level = 6
                    self.speed = 25.0
                elif(self.player.length>40):
                    self.level = 7
                    self.speed = 20.0
                elif(self.player.length>45):
                    self.level = 8
                    self.speed = 15.0
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                #read high score from file
                rf=open("highscore.txt", "r")
                hs = rf.read()
                highscore=int(hs)
                rf.close()
                print(type(highscore))
                print("highscore::",highscore)
                
                #update highscore 
                if(self.player.length>highscore):
                    highscore=self.player.length
                    f= open("highscore.txt","w+")
                    f.write(str(highscore))
                    f.close()
                    
                self.end_menu(highscore)
                print("Game over: ")
                print("Your Score: "+ str(self.player.length))
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)
 
        pass
 
    def on_render(self):
        self._display_surf.fill((240, 192, 22))
        
        speed = pygame.font.SysFont("comicsansms", 20)
        TextSurf, TextRect = self.text_objects("LEVEL: " + str(self.level), speed)
        TextRect.center = (60,10)
        self._display_surf.blit(TextSurf, TextRect)
        pygame.display.update()
        
        score = pygame.font.SysFont("comicsansms", 20)
        TextSurf, TextRect = self.text_objects("SCORE: "+str(self.player.length), score)
        TextRect.center = (900,10)
        self._display_surf.blit(TextSurf, TextRect)
        pygame.display.update()
        
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (self.speed / 1000.0);
        self.on_cleanup()
    
    def end_menu(self, highscore):
        
        while(self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            
            self._display_surf.fill((3, 244, 252))
            
            final_score = pygame.font.SysFont("comicsansms", 40)
            TextSurf, TextRect = self.text_objects("Press SPACE to restart", final_score)
            TextRect.center = ((1000/2),(400/2))
            self._display_surf.blit(TextSurf, TextRect)
            #pygame.display.update()
            
            largeText = pygame.font.SysFont("comicsansms", 40)
            TextSurf, TextRect = self.text_objects("Your final score is "+str(self.player.length),largeText)
            TextRect.center = ((1000/2),(600/2))
            self._display_surf.blit(TextSurf, TextRect)
            
            #largeText = pygame.font.SysFont("comicsansms", 40)
            TextSurf, TextRect = self.text_objects("Highscore is "+str(highscore),largeText)
            TextRect.center = ((1000/2),(800/2))
            self._display_surf.blit(TextSurf, TextRect)
            pygame.display.update()
            
            if (keys[K_ESCAPE]):
                self._running = False
            elif(keys[K_SPACE]):
                self._running = False
                self.on_cleanup()
                self.on_execute()
            
            pygame.display.flip() 
        self.on_cleanup()
    
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()
    
    def start_menu(self):
        if self.on_init() == False:
            self._running = False
        
        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            
            self._display_surf.fill((3, 244, 252))
            largeText = pygame.font.SysFont("comicsansms",40)
            TextSurf, TextRect = self.text_objects("Press any key to start", largeText)
            TextRect.center = ((1000/2),(600/2))
            self._display_surf.blit(TextSurf, TextRect)
            pygame.display.update()
            
            if (keys[K_ESCAPE]):
                self._running = False
            elif(keys[K_SPACE]):
                self._running = False
                self.on_cleanup()
                self.on_execute()
            
            pygame.display.flip()
        self.on_cleanup()

if __name__ == "__main__" :
    
    theApp = App()
    theApp.start_menu()