#!/usr/bin/env python

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
    x_list=[]
    y_list=[]
    start_point=-300
    end_point=1400
    point_step=100
    velocity=7
    update_y=False

    def __init__(self, points=[], loop=False, *args, **kwargs):
        super(BezierLine, self).__init__(*args, **kwargs)
        self.points = self.initialise_points()
        self.loop = loop

        with self.canvas:
            Color(1.0, 0.0, 0.0)

            self.bezier = Bezier(
                    points=self.points,
                    segments=180,
                    loop=self.loop,
                    )

    def initialise_points(self):
        self.x_list=range(self.start_point,self.end_point,self.point_step)
        self.y_list=self.generate_random_list()
        return self.merge_lists(self.x_list, self.y_list)

    def generate_random_list(self):
        y=[]
        for i in range(self.start_point,self.end_point,self.point_step):
            y.extend([random.randint(0,200)])
        return y

    def merge_lists(self, x, y):
        b_list=[]
        for i in range(len(x)):
            b_list.extend([x[i]])
            b_list.extend([y[i]])
        return b_list

    def flow_x(self,x):
        self.update_y=False
        x_list=[]
        x_length=len(x)
        x_limit=self.end_point-self.point_step
        for i in range(x_length):
            x_list.extend([x[i]-self.velocity])
        if(x[-1]<=x_limit):
            x_list.pop(0)
            x_list.extend([self.end_point])
            self.update_y=True
        return x_list

    def flow_y(self,y):
        y_list=[]
        y_length=len(y)
        
        if(self.update_y):
            for i in range(y_length-1):
                y_list.extend([y[i+1]])
            y_list.extend([random.randint(0,200)])
        else:
            return y
        return y_list

    def move(self):
        self.x_list=self.flow_x(self.x_list)
        self.y_list=self.flow_y(self.y_list)
        b_list=self.merge_lists(self.x_list,self.y_list)
        self.bezier.points=b_list
 
class HelicopterGame(Widget):
    line=ObjectProperty(None)
    back_scroll_speed = NumericProperty(0.1)

    def __init__(self, **kw):
        super(HelicopterGame, self).__init__(**kw)

        with self.canvas.before:
            texture = CoreImage('Images/background.png').texture
            texture.wrap = 'repeat'
            self.scroll_back = Rectangle(texture=texture, size=self.size, pos=self.pos)

            self.line=BezierLine()
            Clock.schedule_interval(self.update, 0)

    def scroll_background(self, *l):
        t = Clock.get_boottime()
        self.scroll_back.tex_coords = -(t * self.back_scroll_speed), 0, -(t * self.back_scroll_speed + 1), 0,  -(t * self.back_scroll_speed + 1), -1, -(t * self.back_scroll_speed), -1 

    def update(self, dt):
        self.scroll_background()
        self.line.move()

class TestApp(App):

    def build(self):
        game = HelicopterGame(size=Window.size)
        return game

if __name__ == '__main__':
    TestApp().run()