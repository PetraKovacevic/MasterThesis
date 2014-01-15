#---------------------------------------------------------------------------------------

# Imports
import datetime
from math import radians
import os
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.graphics.transformation import Matrix
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.scatter import Scatter
from kivy.core.gl import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE
from kivy.vector import Vector
import pygame
from functools import partial

from utility_classes.dwell_functionality import *

#---------------------------------------------------------------------------------------

class PosterBackground(DwellOnScatter, Scatter):
    typename = StringProperty("PosterBackground")

    source = StringProperty(None)

    label = ObjectProperty(None)

    image = ObjectProperty(None, allownone = True)

    description = StringProperty(None)
    description_background_colour = ListProperty([1,0,0,0.5]) # default to red
    draw_description = BooleanProperty(False)

    # Playing with a hack to save the poster, disable for now
    save_poster = BooleanProperty(False)

    #-----------------------------------------------------

    # Experimental save operation - fbo not working, using this hack instead
    def dwell(self):
        if self.save_poster is True:
            time_string = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            self.widget_shot(self, filename="{0}-poster.png".format(time_string))

    #-----------------------------------------------------

    # Experimental save operation - fbo not working, using this hack instead
    def save(self,x,y,w,h,prev_scale, prev_rotation, prev_center, widget, filename, *largs):
        data = glReadPixels(x-18, y-18, w+36, h+36, GL_RGBA, GL_UNSIGNED_BYTE)
        surf = pygame.image.fromstring(data, (int(w+36),int(h+36)), 'RGBA', True)
        pygame.image.save(surf, "user_posters"+os.sep+filename)

        widget.center = prev_center
        widget.scale = prev_scale
        widget.rotation = prev_rotation

    #-----------------------------------------------------

    def countdown(self, value, *largs):
        root = App.get_running_app().root
        root.message = str(value)
        if value > 0:
            Clock.schedule_once(partial(self.countdown, value-0.1),0.1)
        else:
            root.message = None

    #-----------------------------------------------------

    # Experimental save operation - fbo not working, using this hack instead
    def widget_shot(self, widget, filename='output.png'):
        prev_scale = widget.scale
        prev_rotation = widget.rotation
        prev_center = widget.center

        widget.center = 1920/2.0, 1080/2.0
        widget.scale = 3
        widget.rotation = 90

        x,y = widget.bbox[0]
        w,h = widget.bbox[1]

        delay = 2
        Clock.schedule_once(partial(self.save, x,y,w,h, prev_scale, prev_rotation, prev_center, widget, filename),delay)
        Clock.schedule_once(partial(self.countdown, delay),-1)


    #-------------------------------------------------------

    def draw_description_background(self, instance, value):
        # make sure on the refresh, we remove the previous (if any) graphic instruction
        self.label.canvas.before.remove_group("description_background")

        with self.label.canvas.before:
            Color(*self.description_background_colour)
            Rectangle(pos = (self.label.center[0]-self.label.texture_size[0]/2, self.label.center[1]-self.label.texture_size[1]/2),
                      size = self.label.texture_size,
                      group = "description_background")

    #-------------------------------------------------------

    def __init__(self, **kwargs):
        super(PosterBackground, self).__init__(**kwargs)

        if self.draw_description is True:
            # need to bind to texture size to update on changes as the label size here is 0,0 (as the label hasn't yet been bound)
            self.label.bind(texture_size=self.draw_description_background)

    #-----------------------------------------------------

    def double_tap(self):
        self.dwell()

    #-----------------------------------------------------

    # Dwell has several use cases:
    # 1. When dwelling on a picture that was within a vertical scroller,
    #    copy the picture from the scrollview to the world
    #    We have to remember to adjust for scale, and direction (rotation)
    # 2. More functionality coming soon
    # todo: make sure the item created is within bounds
    def dwell(self):
        if self.parent is not None and getattr(self.parent, "typename", None)=="VerticalScroller":
            # todo: do I need the following next line?
            if getattr(self, "typename", None)=="PosterBackground":
                p = PosterBackground(source = self.source,
                                     description = self.description,
                                     draw_description = self.draw_description)

                # get the center of x and top of y
                t_x, t_y = self.to_window(self.center[0], self.top)

                # get the center of x and bottom of y
                b_x, b_y = self.to_window(self.center[0], 0)

                # get the center of x and y
                c_x, c_y = self.to_window(self.center[0], self.center[1])

                top = Vector(t_x, t_y)
                bottom = Vector(b_x, b_y)
                up_vector = top-bottom

                try:
                    rotation = self.parent.parent.parent.rotation
                except:
                    rotation = 0

                up_vector = up_vector.normalize()

                # place a constant 150 pixels up from the center
                # todo: should incoporate the size of the vertical scroller box
                center_position = top+up_vector*150

                # make sure the new position isn't outside of the screen
                final_center_position = Utilities.clamp(*center_position)

                root = App.get_running_app().root
                p.center = (c_x, c_y)

                p.apply_transform(Matrix().rotate(radians(rotation), 0, 0, 1), anchor=Vector(p.center))

                p.scale = 0.0001

                root.add_widget(p)

                anim = Animation(center = final_center_position, duration = 0.5, t="in_out_cubic") &\
                       Animation(scale = 1, duration = 0.5, t="in_out_cubic")
                anim.start(p)


    #-----------------------------------------------------

Factory.register("PosterBackground", PosterBackground)

#---------------------------------------------------------------------------------------
