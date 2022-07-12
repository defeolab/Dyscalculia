from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.properties import  ObjectProperty, NumericProperty
from kivy.clock import Clock
import generating_sim as gs
import random

class TrialCanvas(Widget) :
    left_fence = ObjectProperty(None)
    right_fence = ObjectProperty(None)
    dif = 0.50# NumericProperty(round(random.uniform(0.15, 1), 2))
    num_left = NumericProperty(0)
    num_right = NumericProperty(0)
    chicken_size = NumericProperty(0)

    def display_trial(self, *args) :
        left, right, chicken_size = gs.generate_positions(self.left_fence.size[0]/2, self.left_fence.center, self.right_fence.center, self.dif)
        self.left_fence.draw_chickens(left, chicken_size)
        self.right_fence.draw_chickens(right, chicken_size)
        
        
        self.num_right += len(right)
        self.num_left += len(left)
        self.chicken_size += chicken_size
        
class Fence(Widget) :
    def draw_chickens(self, posis, chicken_size) :
        with self.canvas:
            Color(1, 0, 0)
            for position in posis :
                Ellipse(pos=tuple(position), size=(chicken_size, chicken_size))
            Color(1, 1, 1)
    
class GameApp(App) :
    def build(self) :
        trial = TrialCanvas() 
        Clock.schedule_once(trial.display_trial, 0.5)
        return trial


if __name__ == "__main__":
    GameApp().run()