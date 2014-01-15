#-----------------------------------------------------------------------------
# Use for buttons, that need to be controlled by the author (can scale to invisible if required)
from kivy.factory import Factory
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.scatter import Scatter
from utility_classes.dwell_functionality import DwellOnScatter

#-----------------------------------------------------------------------------

class DwellScatterImageButton(DwellOnScatter, Scatter):

    # Define a default function callback (or can be an expression), in case you forget to set it in the kv file
    function_callback = "self.default()"

    # Define a statement that can be called and executed
    statement_callback = None

    # source for the rectangle within the kv file (since this is not inheriting from image, roll our own way to draw)
    source = StringProperty("")

    # Define a tint over the button (currently no tint)
    color = ListProperty([1, 1, 1, 1])

    # whether to treat a double tap as a dwell
    double_tap_as_dwell = BooleanProperty(True)

    def default(self):
        print self, "has not set the function_callback"

    def double_tap(self):
        if self.double_tap_as_dwell:
            self.dwell()

    def dwell(self):
        if self.statement_callback is not None:
            exec self.statement_callback
        else:
            if len(self.function_callback) > 0:
                eval(self.function_callback)

Factory.register("DwellScatterImageButton", DwellScatterImageButton)

#-----------------------------------------------------------------------------
