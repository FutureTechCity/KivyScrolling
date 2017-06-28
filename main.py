from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.core.window import Window

class AnimatingImage(Image):
    time = 0.0
    rate = 0.2
    frame = 1
    def update(self, dt):
        self.time += dt
        if (self.time > self.rate):
            self.time -= self.rate
            self.source = "atlas://invader/frame" + str(self.frame)
            self.texture.mag_filter = "nearest"
            self.frame = self.frame + 1
            if (self.frame > 2):
                self.frame = 1

class ScrollingImage(Widget):
    image = ObjectProperty(None)
    time = 0
    
    def build(self):
        with self.canvas:
            texture = CoreImage(self.image).texture
            texture.wrap = 'repeat'
            self.rectangle = Rectangle(texture=texture, size=self.size, pos=self.pos)
            
    def tex_coords(self, time):
        return [time, 1, 2.0 + time, 1, 2 + time, 0.03, time, 0.03]
            
    def update(self, dt):
        self.time += dt
        if (self.time > 1.0):
            self.time -= 1.0
        self.rectangle.tex_coords = self.tex_coords(self.time)
        
class ScrollingScreen(Widget):
    front_layer = ObjectProperty(None)
    back_layer = ObjectProperty(None)
    cactus = ObjectProperty(None)
    invader = ObjectProperty(None)
    
    def update(self, dt):
        self.front_layer.update(dt * 0.1)
        self.back_layer.update(dt * 0.05)
        self.cactus.pos[0] -= dt * 200.0
        self.invader.update(dt)
        if (self.cactus.pos[0] < -self.cactus.size[0]):
            self.cactus.pos[0] = Window.size[0]
        
    def build(self):
        self.back_layer.build()
        self.front_layer.build()

class ScrollingApp(App):
    def build(self):
        scroller = ScrollingScreen(size=Window.size)
        scroller.build()
        Clock.schedule_interval(scroller.update, 1.0 / 60.0)
        return scroller

if __name__ == '__main__':
    ScrollingApp().run()
