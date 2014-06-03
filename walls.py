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
    points_a=[]; points_b=[]
    x_list=[]; y_list=[]
    x_start=-300; x_end=1400; x_step=100
    #for later, we can slowly increase y end to make the gap between the walls thinner
    y_start=0; y_end=200; y_diff=600-y_end

    #maybe also increase velocity slowly
    velocity=5

    update_y=False

    def __init__(self, *args, **kwargs):
        super(BezierLine, self).__init__(*args, **kwargs)
        self.points_a = self.initialise_points()
        self.points_b = self.make_points_b(self.points_a)

        with self.canvas:
            Color(1.0, 0.0, 0.0)

            self.bezier_a = Bezier(
                    points=self.points_a,
                    segments=180,
                    loop=False,
                    )

            self.bezier_b = Bezier(
                    points=self.points_b,
                    segments=180,
                    loop=False,
                    )

    def make_points_b(self, l):
        x=l[::2]
        y=l[1::2]
        new_y=[i+self.y_diff for i in y]
        return self.merge_lists(x,new_y)

    def initialise_points(self):
        self.x_list=range(self.x_start,self.x_end,self.x_step)
        self.y_list=self.generate_random_list()
        return self.merge_lists(self.x_list, self.y_list)

    def generate_random_list(self):
        y=[]
        for i in range(self.x_start,self.x_end,self.x_step):
            y.extend([random.randint(self.y_start,self.y_end)])
        return y

    def merge_lists(self, x, y):
        list=[]
        for i in range(len(x)):
            list.extend([x[i]])
            list.extend([y[i]])
        return list

    def flow_x(self,x):
        self.update_y=False
        x_list=[]
        x_length=len(x)
        x_limit=self.x_end-self.x_step
        for i in range(x_length):
            x_list.extend([x[i]-self.velocity])
        if(x[-1]<=x_limit):
            x_list.pop(0)
            x_list.extend([self.x_end])
            self.update_y=True
        return x_list

    def flow_y(self,y):
        y_list=[]
        y_length=len(y)
        if(self.update_y):
            for i in range(y_length-1):
                y_list.extend([y[i+1]])
            y_list.extend([random.randint(self.y_start,self.y_end)])
            return y_list
        return y

    def move(self):
        self.x_list=self.flow_x(self.x_list)
        self.y_list=self.flow_y(self.y_list)
        a_list=self.merge_lists(self.x_list,self.y_list)
        b_list=self.make_points_b(a_list)
        self.bezier_a.points=a_list
        self.bezier_b.points=b_list
 
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