#---------------------------------------------------------------------------------------

# Imports
import json
from math import radians
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.graphics.context_instructions import Color
from kivy.graphics.transformation import Matrix
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.scatter import Scatter
from kivy.uix.togglebutton import ToggleButton
from kivy.vector import Vector

from utility_classes.dwell_functionality import *

#---------------------------------------------------------------------------------------

class CommonAttachToPosterBackground(object):

    #-------------------------------------------------------

    def try_to_attach_to_background_object(self, x, y):
        siblings = self.parent.children
        for sibling in siblings:
            if getattr(sibling, "typename", None)=="PosterBackground":
                if sibling.collide_point(x,y):
                    parent = self.parent
                    parent.remove_widget(self)

                    # adjust for poster background co-ordinates (going from world to poster background)
                    x1, y1 = sibling.to_local(self.center[0], self.center[1])
                    self.center = (x1, y1)

                    # adjust for poster background scale (going from world to poster background)
                    self.scale *= 1.0/float(sibling.scale)

                    # adjust for poster background rotation (going from world to poster background)
                    self.apply_transform(Matrix().rotate(-radians(sibling.rotation), 0, 0, 1), anchor=Vector(self.center))

                    # add self to the poster background
                    sibling.add_widget(self)

                    break
            if getattr(sibling, "typename", None) == "VerticalScroller":
                if sibling.can_drop_items_in:
                    if sibling.collide_point(x,y):
                        sibling.add_item(self,delay=0.5, with_animation=True)

                        break
    #-------------------------------------------------------

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False

        handled = super(CommonAttachToPosterBackground, self).on_touch_up(touch)

        if handled:
            # already attached to a poster background
            if getattr(self.parent, "typename", None)=="PosterBackground":
                # take the touch point in poster background co-ordinates and change them to world co-ordinates
                # then project a test, to see if those co-ordinates still touch the poster background
                # (note: this is why do_collide_after_children is important)
                x1, y1 = self.to_window(touch.x, touch.y)

                if self.parent.collide_point(x1, y1) is True:
                    # means poster background is still under me, so nothing special to do

                    # hack to clear out the touches on the current object, to prevent weird jump issue
                    self._touches = []

                    pass
                else:
                    # means I have moved out of the poster background, perform a deattach operation from poster background, and attach to world (or another poster background).
                    # need to reverse the steps that were taken when originally attached to the poster background
                    # and also account for any transformations since.
                    parent = self.parent
                    root = parent.parent

                    # figure out the center of the object in "world co-ordinates"
                    c_x1, c_y1 = self.to_window(self.center[0], self.center[1])

                    # figure out the scale of the object in "world co-ordinates"
                    c_scale = self.scale*self.parent.scale

                    # adjust for the rotation introduced in the "poster background co-ordinates", when going from "poster background co-ordinates" to "world co-ordinates"
                    self.apply_transform(Matrix().rotate(radians(self.parent.rotation), 0, 0, 1), anchor=Vector(self.center))

                    self.parent.remove_widget(self)

                    # set the properties, don't add any delay or animation, so it looks invisible to the naked eye, the deattaching/attaching
                    self.center = c_x1, c_y1
                    self.scale = c_scale

                    # add back to the top level world
                    root.add_widget(self)

                    # add in a check to see if when we took off our finger, it was actually on another poster background and not the world
                    # poster background to poster background transforms are confusing, easier to do b->w->b
                    self.try_to_attach_to_background_object(x1, y1)

                    # hack to clear out the touches on the current object, to prevent weird jump issue
                    self._touches = []
            # not attached, lets find (if any) the closest poster background under us, and then attach to it
            else:
                self.try_to_attach_to_background_object(touch.x, touch.y)

                # hack to clear out the touches on the current object, to prevent weird jump issue
                self._touches = []

        return handled

    #-------------------------------------------------------

#---------------------------------------------------------------------------------------

class Picture(CommonAttachToPosterBackground, DwellOnScatter, Scatter):
    typename = StringProperty("Picture")

    source = StringProperty(None)

    label = ObjectProperty(None)

    description = StringProperty(None)
    description_background_colour = ListProperty([1,0,0,0.5]) # default to red
    draw_description = BooleanProperty(True)

    border_colour = ListProperty([1,1,1,1]) # default to white

    #-------------------------------------------------------

    # We have to account for the momentum function, entering different
    # co-ordinate systems (argh).
    #
    # Test around for this, and kill momentum if moving into a widget
    # where the momentum, shouldn't be on

    def inertial_translation(self, time):
        if getattr(self.parent, "typename", None)=="VerticalScroller":
            Clock.unschedule(self.inertial_translation)
        elif getattr(self.parent, "typename", None)=="PosterBackground":
            Clock.unschedule(self.inertial_translation)
        else:
            super(Picture, self).inertial_translation(time)

    #-------------------------------------------------------

    def double_tap(self):
        self.dwell()

    #-------------------------------------------------------

    # Dwell has several use cases:
    # 1. When dwelling on a picture that was within a vertical scroller,
    #    copy the picture from the scrollview to the world
    #    We have to remember to adjust for scale, and direction (rotation)
    # 2. More functionality coming soon
    # todo: make sure the item created is within bounds
    def dwell(self):
        if self.parent is not None and getattr(self.parent, "typename", None)=="VerticalScroller":
            # todo: do I need the following next line?
            if getattr(self, "typename", None)=="Picture":
                if self.parent.parent.parent.make_duplicate_on_dwell is False:
                    parent = self.parent.parent.parent


                    # todo: properly convert between the co-ordinate systems

                    parent.items.remove_widget(self)


                    root = App.get_running_app().root
                    root.add_widget(self)

                    self.do_translation = True
                    self.do_translation_x = True
                    self.do_translation_y = True
                    self.do_scale = True
                    self.do_rotation = True
                    self.auto_bring_to_front = True
                    self.accept_touch_even_if_all_transforms_are_false = True




                    # Todo: should really figure out why, when de-attaching this
                    # the touches linger on the object
                    # this hack seems to work for now
                    self._touches = []


                else:
                    # Figure out if we have colour code on/off
                    group = ToggleButton.get_widgets('colour')

                    # In what format to send the options to the main program????
                    colour_code_on = False
                    for x in group:
                        if x.text == 'Yes' and x.state == 'down':
                            colour_code_on = True
							

                    if colour_code_on:
                        p = Picture(source = self.source,
                                    description = self.description,
                                    draw_description = self.draw_description,
                                    border_colour = self.border_colour)

                        # Not sure why being ignored when in the constructor, but
                        # if set from the outside, appears to force it on :)
                        p.description_background_colour = self.description_background_colour

                    else:
                        anonymous_color = json.loads(Config.get('options', 'anonymous_color'))

                        p = Picture(source = self.source,
                                    description = self.description,
                                    draw_description = self.draw_description,
                                    border_colour = anonymous_color)

                        # Not sure why being ignored when in the constructor, but
                        # if set from the outside, appears to force it on :)
                        p.description_background_colour = anonymous_color

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
        super(Picture, self).__init__(**kwargs)

        if self.draw_description is True:
            # need to bind to texture size to update on changes as the label size here is 0,0 (as the label hasn't yet been bound)
            self.label.bind(texture_size=self.draw_description_background)

    #-------------------------------------------------------

Factory.register("Picture", Picture)

#---------------------------------------------------------------------------------------
