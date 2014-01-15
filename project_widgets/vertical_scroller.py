#---------------------------------------------------------------------------------------

# Imports
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.uix.scatter import Scatter
from kivy.vector import Vector
from utility_classes.dwell_functionality import *
from kivy import Logger

#---------------------------------------------------------------------------------------

class VerticalScroller(DwellOnScatter, Scatter):
    typename = StringProperty("VerticalScroller")

    can_drop_items_in = BooleanProperty(True)

    # Whether or not, we just move the item from the container to the outside, or
    # whether we clone the item instead
    make_duplicate_on_dwell = BooleanProperty(True)



    border_width = NumericProperty(50)
    scrollview_height = NumericProperty(50) #200
    scrollview_width = NumericProperty(50) #550

    scroller = ObjectProperty(None)
    items = ObjectProperty(None)

    background_colour = ListProperty([1,1,1,1])
    background_image = StringProperty(None)

    description = StringProperty(None)

    draw_description = BooleanProperty(True)
    allowed_to_touch = BooleanProperty(True)
    #label = ObjectProperty(None)

    # ------------------------------------------------------------------

    def __init__(self, **kwargs):
        super(VerticalScroller, self).__init__(**kwargs)

        # To allow vertical scrolling to occur
        self.items.bind(minimum_width = self.items.setter('width'))

        # change the default from 2dp to 15dp
        self.scroller.bar_width = '15dp'
        self.scroller.bar_margin = -10

        # turn off horizontal scrolling (nothing would scroll anyways, due to the grid layout
        # but the bar would be visible, this makes the horizontal bar disappear
        self.scroller.do_scroll_y = False

        self.scroller.bar_color = (0,0.2,1,.7) # blue

    # ------------------------------------------------------------------
	
    def on_touch_down(self, touch):
        if self.allowed_to_touch is False:
            # False means ignore the touch token
            return False

        super(VerticalScroller, self).on_touch_down(touch)

    # ------------------------------------------------------------------

    # internal - do not call directly
    def add_note_to_scroller(self, instance, widget):
        if self.parent is not None:
            self.parent.remove_widget(widget)

        item = widget

        # adjust the size of the image to allow for the borderimage background to be shown
        # fudge the borderimage into the equation (hard because it is drawn outside of the image,
        # and thus does not come into the calculations for the scrollview, which means
        # we need to manually fix up the left/right/top/bottom cases, for this to show
        # properly on the screen
        # 36 happens to the be border image size numbers we are using in the .kv file
        item.label.size = 100, self.scrollview_height-36
        item.size = item.label.size[0]+36, item.label.size[1]+18
        item.size_hint_x = None

        # the scroller, effects size, and not the scale of the container, so we must adjust for this,
        # else the object will be in the container with its current transforms, which would look weird
        item.scale = 1
        item.rotation = 0

        try:
            self.items.add_widget(widget)
        except:
            Logger.debug("Vertical Scroller: (note) timing issue, means user touched this object, so now it has a parent, when it shouldn't, so don't add to the scroller afterall")

    # ------------------------------------------------------------------

    # internal - do not call directly
    def add_picture_to_scroller(self, instance, widget):
		
        if self.parent is not None:
            self.parent.remove_widget(widget)

        item = widget

        # adjust the size of the image to allow for the borderimage background to be shown
        # fudge the borderimage into the equation (hard because it is drawn outside of the image,
        # and thus does not come into the calculations for the scrollview, which means
        # we need to manually fix up the left/right/top/bottom cases, for this to show
        # properly on the screen
        # 36 happens to the be border image size numbers we are using in the .kv file
        item.image.size = item.image.image_ratio*(self.scrollview_height-36), self.scrollview_height-36
        item.size = item.image.size[0]+36, item.image.size[1]+18
        item.size_hint_x = None

        # the scroller, effects size, and not the scale of the container, so we must adjust for this,
        # else the object will be in the container with its current transforms, which would look weird
        item.scale = 1
        item.rotation = 0

        try:
            self.items.add_widget(widget)
        except:
            Logger.debug("Vertical Scroller: (picture) timing issue, means user touched this object, so now it has a parent, when it shouldn't, so don't add to the scroller afterall")

    # ------------------------------------------------------------------

    def add_item(self, item, delay=0, with_animation=False):
        if getattr(item, "typename", None) == "Picture" or \
           getattr(item, "typename", None) == "PosterBackground" or \
           getattr(item, "typename", None) == "Note":

            # disable the appropriate transformations, so it plays nice in the scrollview
            item.do_translation = False
            item.do_translation_x = False
            item.do_translation_y = False
            item.do_rotation = False
            item.do_scale = False
            item.do_collide_after_children = True
            item.accept_touch_even_if_all_transforms_are_false = True
            item.auto_bring_to_front = False

            if with_animation is False or delay < 0.0001:
                if getattr(item, "typename", None) == "Note":
                    self.add_note_to_scroller(None, item)
                else:
                    self.add_picture_to_scroller(None, item)
            else:

                # get the center of x and top of y
                t_x, t_y = self.to_window(self.center[0], self.top)

                # get the center of vertical scroller x and y
                c_x, c_y = self.to_window(self.center[0], self.center[1])

                # determine the position 90% of x, and in the middle of y (of the vertical scroller)
                top          = Vector(t_x, t_y)
                center       = Vector(c_x, c_y)
                up_vector    = top-center
                up_vector    = up_vector.rotate(self.rotation)
                right_vector = up_vector.rotate(-90) # rotation is anti-clockwise (rotate right)
                right_vector = right_vector.normalize()
                position  = center + right_vector*(self.size[0]*0.45)*self.scale

                anim = Animation(scale = 0.0001,
                                 rotation = item.rotation-180,
                                 pos = (position.x, position.y),
                                 duration = delay,
                                 t='in_out_circ')
                if getattr(item, "typename", None) == "Note":
                    anim.bind(on_complete=self.add_note_to_scroller)
                else:
                    anim.bind(on_complete=self.add_picture_to_scroller)
                anim.start(item)


    # ------------------------------------------------------------------

Factory.register("VerticalScroller", VerticalScroller)

#---------------------------------------------------------------------------------------

