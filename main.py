#!/usr/bin/env python
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Bezier, Line

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

                 
class TestApp(App):

    def build(self):
        from math import cos, sin, radians
        x = 0; y = 300
        d=30
        points = [x, y]
        for i in range(0, 10, 1):
            print i
            #print y
            #make a sin wave
            #y goes 0, -1, 0, -1
            x=x+100
            y=y+50
            points.extend([x, y])
        points1 = [0,200,100,300,200,200,300,100,400,200,500,300,600,200]
        return BezierLine(points=points1, loop=False)

if __name__ == '__main__':
    TestApp().run()