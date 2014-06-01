#!/usr/bin/env python

#scren size is 800. have between 0 and 800 with 100 intervals for x. randomise y instaed of adding on.
#make a function which just updates the line with the new points each time

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Bezier, Line
import random
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.uix.label import Label

class BezierLine(Widget):
    def __init__(self, points=[], loop=False, *args, **kwargs):
        super(BezierLine, self).__init__(*args, **kwargs)
        self.points = points
        self.loop = loop
        
        with self.canvas:
            #Color(1.0, 0.0, 0.0)

            self.bezier = Bezier(
                    points=self.points,
                    segments=180,
                    loop=self.loop,
                    )

    def move(self, points):
        self.bezier.points=points

 
class HelicopterGame(Widget):
    x_list=[]
    y_list=[]
    line=ObjectProperty(None)
    back_scroll_speed = NumericProperty(0.1)

    def __init__(self, **kw):
        super(HelicopterGame, self).__init__(**kw)

        with self.canvas.before:
            texture = CoreImage('Images/background.png').texture
            texture.wrap = 'repeat'
            self.scroll_back = Rectangle(texture=texture, size=self.size, pos=self.pos)
            
            self.x_list=range(-100,1000,100)
            self.y_list=self.generate_random_list()

            b_list=self.merge_lists(self.x_list, self.y_list)
            self.line=BezierLine(points=b_list)
        
            Clock.schedule_interval(self.update, 0)

    def scroll_background(self, *l):
        t = Clock.get_boottime()
        self.scroll_back.tex_coords = -(t * self.back_scroll_speed), 0, -(t * self.back_scroll_speed + 1), 0,  -(t * self.back_scroll_speed + 1), -1, -(t * self.back_scroll_speed), -1 

    def generate_random_list(self):
        y=[]
        for i in range(-1,10,1):
            y.extend([random.randint(0,200)])
        return y

    def merge_lists(self, x, y):
        b_list=[]
        for i in range(len(x)):
            b_list.extend([x[i]])
            b_list.extend([y[i]])
        return b_list

    def flow_y(self,y):
        y_list=[]
        for i in range(len(y)-1):
            y_list.extend([y[i+1]])
        y_list.extend([random.randint(0,200)])
        return y_list

    def update(self, dt):
        self.scroll_background()

        self.y_list=self.flow_y(self.y_list)
        b_list=self.merge_lists(self.x_list,self.y_list)

        self.line.move(b_list)

class TestApp(App):

    def build(self):
        game = HelicopterGame(size=Window.size)
        return game

if __name__ == '__main__':
    TestApp().run()