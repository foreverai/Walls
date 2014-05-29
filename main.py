#!/usr/bin/env python

#scren size is 800. have between 0 and 800 with 100 intervals for x. randomise y instaed of adding on.
#make a function which just updates the line with the new points each time

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Bezier, Line
import random

class BezierLine(FloatLayout):

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
 
class HelicopterGame(Widget):
    x_list=[]
    y_list=[]

    def __init__(self, **kw):
        super(HelicopterGame, self).__init__(**kw)

        self.x_list=range(0,900,100)
        self.y_list=self.generate_random_list()

        Clock.schedule_interval(self.update, 1)

    def generate_random_list(self):
        y=[]
        for i in range(0,9,1):
            y.extend([random.randint(200,400)])
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
        y_list.extend([random.randint(200,400)])
        return y_list

    def update(self, dt):
        #self.y_list=self.generate_random_list()
        self.y_list=self.flow_y(self.y_list)
        b_list=self.merge_lists(self.x_list,self.y_list)
        print b_list
        #print x_list, y_list

        #self.drawLine()

        #print self.points_all
        #self.
        self.add_widget(BezierLine(points=b_list))
        #return BezierLine(points=b_list)

class TestApp(App):

    def build(self):
        game = HelicopterGame(size=Window.size)
        return game

if __name__ == '__main__':
    TestApp().run()