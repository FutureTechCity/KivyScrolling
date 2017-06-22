# Kivy scrolling

This Kivy project demonstrates how scroll parallax layers and foreground objects.

## Drawing components

You need to create a long thin texture that represents the sky gradient. You will also need two tilable textures: one for the front parallax layer and one for the back. You can use a vector drawing program to create them such as Adobe Illustrator or Inkscape, or you can use a pixel editing program such as [Piskel](http://www.piskelapp.com/). You will also need to create a foreground image. I used Piskel for this.

## Structure

First you'll draw a full screen `Rectangle`, by stretching the single pixel bitmap sky gradiant across the whole screen. 

Then you'll make two full screen width rectangles, and you'll assume that the texture repeats twice across this width. In each case the rectangle drawn is the screen width and doesn't move, but the pixels mapped onto those rectangles are taken from a moving region of the image file. When those coordinates move beyond the original image, they are reset back to the beginning. You won't see this transition since the image file pixels repeat.

Finally, you'll add a sprite as an `Image` which you'll then move in code from one side of the screen to the other. When the sprite goes beyond the edge its position is reset to the other side.

## Create your code file

Use an editor to create a `main.py` file. You can copy the following template code into this file:

~~~
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.core.window import Window

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
    
    def update(self, dt):
        self.front_layer.update(dt * 0.1)
        self.back_layer.update(dt * 0.05)
        self.cactus.pos[0] -= dt * 200.0
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
~~~

## Create your layout file

Use an editor to create a `scrolling.kv` file. You can copy the following template layout into this file:
~~~
#:kivy 1.9.0

<ScrollingScreen>:
    front_layer: front
    back_layer: back
    cactus: cactus1

    canvas.before:
        BorderImage:
            source: 'sky-gradient.png'
            border: 0, 0, 0, 0
            size: self.width, self.height
            pos: 0, 0
            
    ScrollingImage:
        id: back
        image: 'mountains2.png'
        pos: 0, root.height / 8
        size: root.width, root.height / 8

    ScrollingImage:
        id: front
        image: 'mountains.png'
        pos: 0, root.height / 8
        size: root.width, root.height / 8

    Image:
        id: cactus1
        source: 'cactus.png'
        pos: 0, 0
        size: self.size
~~~

## Test scrolling

You can test by running the following command from the Anaconda prompt:
~~~
python main.py
~~~

## Challenges

* Create textures that repeat 3 or 4 times across the screen
* Create a third layer
* Make additional foreground objects
* Create foreground objects that move at different speeds
* Add a sun that rises
* Scroll the sky gradient
