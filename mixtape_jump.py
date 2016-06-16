"""
***************************************************************************
filename:       mixtape_jump.py
description:    A side scrolling game where the player (mixtape) must navigate through rappers and achieve a high score!
Author:         Wei.K, Miyata.Y, Han.J
Created On:     06/13/2016
***************************************************************************
"""

import kivy
kivy.require('1.7.2')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Canvas
from random import *

class WidgetDrawer(Widget):
"""
Class that initializes all the widgets used in this game.
"""
#This widget is used to draw all of the objects on the screen
#objects of this class must be initiated with an image string

    def __init__(self, imageStr, **kwargs):
    """
    Initializes widget movement, size, positioning
    :param imageStr: str - What allows you to put the location of your imported images
    :param kwargs: None
    :return: None
    """
        super(WidgetDrawer, self).__init__(**kwargs)

        with self.canvas:
        #this line creates a rectangle with the image drawn on top
            self.size = (Window.width*.005*25,Window.height*.005*25)
            self.rect_bg= Rectangle(source=imageStr,pos=self.pos,size = self.size)

            #this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y

            #center the widget
            self.pos = (self.x,self.y)

            #center the rectangle on the widget
            self.rect_bg.pos = self.pos

    def update_graphics_pos(self, instance, value):
        """
        If the position of the widget is moved then the rectangle which has the image is also moved
        :param instance:
        :param value: int - What updates the rectangles position after the position of the widget has changed
        :return: None
        """
        #if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value

    #use this function to change widget size
    def setSize(self,width, height):
        """
        Set the size of the widgets
        :param width: int - The width of the widget
        :param height: int - The height of the widget
        :return: None
        """
        self.size = (width, height)

    def setPos(self,xpos,ypos):
        """
        Setting initial x and y positions of the widget
        :param xpos: int - X position of widget
        :param ypos: int - Y position of widget
        :return: None
        """
        self.x = xpos
        self.y = ypos
#Start of John"s code
class mixtape(WidgetDrawer):
    """
    A mixtape object
    """
    def __init__(self, imageStr) :
        """
        This function initializes the mixtapes gravity and impulse attributes
        :param imageStr: calls on an image file
        :return:none
        """
        WidgetDrawer.__init__(self, imageStr)
        self.impulse = 3
        self.grav = -0.1

        self.velocity_x = 0
        self.velocity_y = 0

        self.setSize(50, 30)

    def setSize (self, width, height):
        """
        sets the size of the mixtape
        :param width: width
        :param height: height
        :return: none
        """
        WidgetDrawer.setSize(self, width, height)

    def move(self):
        """
        A function that updates the coordinates of the object with the velocity movements
        :return:none
        """
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y

        if self.y > Window.height*0.95:
            self.impulse = -3

    def determineVelocity(self):
        """
        A function that changes the velocity in certain circumstances when the mixtape goes up or down the screen.
        :return: none
        """
        self.grav = self.grav*1.05

        if self.grav < -4:
            self.grav = -4

        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95*self.impulse

    def update(self):
        """
        A function that determines the new velocity and moves the mixtape
        :return:
        """
        self.determineVelocity()
        self.move()


class MyButton(Button):
    """
    A button object
    """
    def __init__(self, **kwargs):
        """
        calls upon the button widget to be used for the restart button
        :param kwargs:
        """
        super(MyButton, self).__init__(**kwargs)
        self.font_size = Window.width*0.018
#End of John's Code

class GUI(Widget):
    rapperList =[]
    rapperScore = NumericProperty(0)
    minProb = 1780
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.score = Label(text = "0")
        self.score.y = Window.height*0.8
        self.score.x = Window.width*0.2
        self.rapperScore = 0
        l = Label(text='Mixtape Jump')
        l.x = Window.width/2 - l.width/2
        l.y = Window.height*0.8
        self.add_widget(l)
        self.mixtape = mixtape(imageStr = 'C:\Users\Koven\desktop\photoshopped\mmixtape.png')
        self.mixtape.x = Window.width/4
        self.mixtape.y = Window.height/2
        self.add_widget(self.mixtape)

        def check_score(self,obj):
            self.score.text = str(self.rapperScore)
        self.bind(rapperScore = check_score)
        self.add_widget(self.score)

    def addrapper(self):
        """
        Program to initialize the opposing objects and the multiple rapper heads which includes its randomized placement
        and the velocity which it moves at
        :return:
        """
        #add an rapper to the screen
        #initialize its image
        imageNumber = randint(1,7)
        imageStr = ('C:\Users\Koven\desktop\photoshopped\image'+str(imageNumber)+'.png')
        tmprapper = rapper(imageStr)
        tmprapper.x = Window.width*0.99
        #randomize y position
        ypos = randint(2,25)
        ypos = ypos*Window.height*.0625
        #moves only on the x-axis
        tmprapper.y = ypos
        tmprapper.velocity_y = 0
        vel = 10
        tmprapper.velocity_x = -0.1*vel
        #adds list to another rapper list which helps append score
        self.rapperList.append(tmprapper)
        self.add_widget(tmprapper)
    #handle input events
    def on_touch_down(self, touch):
        """
        Program to move the mixtape up according to when the screen is pressed
        :param touch: none (when it is pressed down (responsive to touch events))
        :return:
        """
        #moves the mixtape up
        self.mixtape.impulse = 3
        #Gravitational velocity to help move down
        self.mixtape.grav = -0.1

    def gameOver(self):
        """
        Program to initiate when the game is over from collision as well as the initialization of restart
        :return:
        """
        # this function is called when the game ends
        #add a restart button
        restartButton = MyButton(text='Press to Restart, your score was ' + str(self.rapperScore))
        def restart_button(obj):
        #this function will be called whenever the reset button is pushed
            print 'restart button pushed'
            #reset game
            for k in self.rapperList:
                self.remove_widget(k)
                self.mixtape.xpos = Window.width*0.25
                self.mixtape.ypos = Window.height*0.5
                self.minProb = 1780
            self.rapperList = []

            self.parent.remove_widget(restartButton)
            #stop the game clock in case it hasn't already been stopped
            Clock.unschedule(self.update)
            #start the game clock
            Clock.schedule_interval(self.update, 1.0/60.0)
        restartButton.size = (Window.width*.3,Window.width*.1)
        restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.5
        #bind the button using the built-in on_release event
        #whenever the button is released, the restart_button function is called
        restartButton.bind(on_release=restart_button)

        #It's important that the parent gets the button so you can click on it
        #otherwise you can't click through the main game's canvas
        self.parent.add_widget(restartButton)

    def gameOver(self):
        """
        Program to initiate when the game is over from collision as well as the initialization of restart
        :return:
        """
        # this function is called when the game ends
        #add a restart button
        restartButton = MyButton(text='Press to Restart, your score was ' + str(self.rapperScore))
        def restart_button(obj):
        #this function will be called whenever the reset button is pushed
            print 'restart button pushed'
            #reset game
            for k in self.rapperList:
                self.remove_widget(k)
                self.mixtape.xpos = Window.width*0.25
                self.mixtape.ypos = Window.height*0.5
                self.minProb = 1780
            self.rapperList = []

            self.parent.remove_widget(restartButton)
            #stop the game clock in case it hasn't already been stopped
            Clock.unschedule(self.update)
            #start the game clock
            Clock.schedule_interval(self.update, 1.0/60.0)
        restartButton.size = (Window.width*.3,Window.width*.1)
        restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.5
        #bind the button using the built-in on_release event
        #whenever the button is released, the restart_button function is called
        restartButton.bind(on_release=restart_button)

        #It's important that the parent gets the button so you can click on it
        #otherwise you can't click through the main game's canvas
        self.parent.add_widget(restartButton)

    def update(self,dt):
        """
        Program to update when the add to score as well as when to spawn a rapper, end the game
        :param dt: none (clock object (time elapsed))
        :return:
        """
        #This update function is the main update function for the game
        #events are setup here as well
        #update game objects
        #update mixtape
        self.mixtape.update()
        #update rappers
        #randomly add an rapper
        tmpCount = randint(1,1800)
        print self.minProb
        #overtime difficulty increase
        if tmpCount > self.minProb:
            self.addrapper()
            self.minProb = self.minProb - 0.10
        #peak difficulty
        if self.minProb <= 1750:
            self.minProb = self.minProb + 0.1
        if self.mixtape.y < Window.height * 0.001:
            self.mixtape.impulse = 10
        for k in self.rapperList:
            #check for collision with mixtape
            if k.collide_widget(self.mixtape):
                print 'death'
                #game over routine
                self.gameOver()
                Clock.unschedule(self.update)
                self.rapperScore = 0
            #when rappers past the left screen
            if k.x < -100:
                self.remove_widget(k)
                self.rapperScore += 1
                tmpRapperList = self.rapperList
                tmpRapperList[:] = [x for x in tmpRapperList if (x.x > - 100)]
                self.RapperList = tmpRapperList
            k.update()


class ClientApp(App):
    """
    An Client App Object
    """
    def build(self):
        """
        Program to initialize the buttons and start the game and game clock
        :return: none (return the GUI Class)
        """
        #widget initializations and insertion
        #used to initialize buttons
        parent = Widget()
        app = GUI()
        #Start the game clock (runs update function once every (1/60) seconds)
        Clock.schedule_interval(app.update, 1.0/60.0)
        parent.add_widget(app)
        return parent

if __name__ == '__main__' :
    ClientApp().run()












