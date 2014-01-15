#-----------------------------------------------------------------------------

from kivy.factory import Factory
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout

#-----------------------------------------------------------------------------

class ApplicationBackground(FloatLayout):
    # using this as a message to the user, you can ignore this
    message = StringProperty(None, allownone=True)

    # the background colour will tint the image (if any image exists)
    background_colour = ListProperty([1,1,1,0.5]) # grey by default

    background_image = StringProperty(None)

    # A canvas to draw the line connections in, underneath all the other objects in the scene
    line_connections = ObjectProperty(None)

    # todo - a function, to disconnect a keyboard from an object
    # especially if we delete said object, we need a way to
    # tell a keyboard this, etc.

Factory.register("ApplicationBackground", ApplicationBackground)

#-----------------------------------------------------------------------------
