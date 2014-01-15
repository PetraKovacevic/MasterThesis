#---------------------------------------------------------------------------------------

# Kivy imports
from math import radians
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.core.window import Keyboard
from kivy.uix.label import Label

# Add extra Kivy imports here
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty

#---------------------------------------------------------------------------------------

# Need a label to have the ability to be scaled, use for static displays (non-interactive)
from kivy.vector import Vector
from project_widgets.picture import CommonAttachToPosterBackground

from utility_classes.dwell_functionality import DwellOnScatter

#---------------------------------------------------------------------------------------

# Todo: bind size to texture_size and update that way for width/height
from utility_classes.utilities import Utilities


class Note(CommonAttachToPosterBackground, DwellOnScatter, Scatter):
    typename = StringProperty("Note")

    default_note_width  = NumericProperty(50)
    default_note_height = NumericProperty(50)

    # ------------------------------------------------------------------------

    # Define the color of the font (currently black)
    text_colour = ListProperty([1, 1, 1, 1])

    # Define a tint over the Label (current no tint)
    colour = ListProperty([1, 1, 0, 0.5])

    text = StringProperty("")
    font_size = NumericProperty('20sp')

    keyboard_can_link_to = BooleanProperty(False)

    border_colour = ListProperty([1,0,0,1]) # default to red

    # We have to account for the momentum function, entering different
    # co-ordinate systems (argh).
    #
    # Test around for this, and kill momentum if moving into a widget
    # where the momentum, shouldn't be on

    # ------------------------------------------------------------------------

    def inertial_translation(self, time):
        if getattr(self.parent, "typename", None)=="VerticalScroller":
            Clock.unschedule(self.inertial_translation)
        elif getattr(self.parent, "typename", None)=="PosterBackground":
            Clock.unschedule(self.inertial_translation)
        else:
            super(Note, self).inertial_translation(time)

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
            if getattr(self, "typename", None)=="Note":
                n = Note(text = self.text,
                         colour = self.colour,
                         border_colour = self.border_colour,
                         keyboard_can_link_to = self.keyboard_can_link_to)

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
                n.center = (c_x, c_y)

                n.apply_transform(Matrix().rotate(radians(rotation), 0, 0, 1), anchor=Vector(n.center))

                n.scale = 0.0001

                root.add_widget(n)

                anim = Animation(center = final_center_position, duration = 0.5, t="in_out_cubic") &\
                       Animation(scale = 1, duration = 0.5, t="in_out_cubic")
                anim.start(n)

    # ------------------------------------------------------------------------

    def from_keyboard(self, instance, keycode, text, modifiers):
		#self.text += str(text)
		#print "keycode: " + keycode
		#print "text: " + keycode
		#print "Keycode to string: " + chr(Keyboard().string_to_keycode(keycode)) + chr(13)
		#print "This is for backspace: " + str(Keyboard().string_to_keycode(keycode))
		#print "This is for backspace: " + keycode
		#char = Keyboard().string_to_keycode(keycode)
		
		if self.text == "Write something":
			self.text = ""
		
		if keycode in ['capslock', 'shift']:
			self.text += ""
		elif keycode == 'enter':
			self.text += "\n"
		elif keycode == 'tab':
			self.text += " "
		elif keycode == 'backspace':
			if len(self.text)>0:
				self.text = self.text[:-1]
		else:
			self.text += str(text)

    # ------------------------------------------------------------------------

    def figureOutHeight(self, _width=100, content=""):
        temp_label = Label(width=_width, markup=True, text=content)
        d = temp_label._font_properties
        dkw = dict(zip(d, [getattr(temp_label, x) for x in d]))
        from kivy.core.text.markup import MarkupLabel
        la = MarkupLabel(**dkw)

        w, h = la.render(real=False) # makes the _lines variables

        # Grab the heights dimensions of the input (guard against empty string)
        input_heights = []
        for entry in la._lines:
            heights = [item[1] for item in entry[4]]
            input_heights.extend(heights)
        input_height = max(input_heights) if len(input_heights) > 0 else 0

        return input_height*len(la._lines)

    # ------------------------------------------------------------------------

    # Hard-coded to work with font = 20sp (play around with the multiplier on the box_height if you change the text from 20sp)
    def update_label_size(self, instance, value):
        box_width = self.default_note_width if self.label.texture_size[0] < self.default_note_width else self.label.texture_size[0]+50
        approx_height = self.figureOutHeight(_width = box_width, content = self.label.text)
        box_height = self.default_note_height if approx_height < self.default_note_height else approx_height*1.5

        # Re-size the note container
        self.label.size = box_width, box_height

    # ------------------------------------------------------------------------

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)

        # Create a listener on the texture_size of the label
        self.label.bind(texture_size=self.update_label_size)

    #------------------------------------------------------------------------

Factory.register("Note", Note)

#---------------------------------------------------------------------------------------
