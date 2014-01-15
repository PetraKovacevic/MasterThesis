#-----------------------------------------------------------------------------
# July 5, 2013
# This entire class (and its subclass VKeyboard) is completely dynamic
# through python (and not the kv file), as such the collide functions are overloaded
# and means you need to be careful if changing this class, to make sure you
# account for transformations, as well as widgets (as on the refresh method)
# clear is called on the canvas, and that will remove all widgets
# this is required, so the keyboard can be dynamic
#-----------------------------------------------------------------------------

from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.vkeyboard import VKeyboard
from kivy.vector import Vector
from kivy.uix.scatter import Scatter
from project_widgets.dwell_scatter_image_button import DwellScatterImageButton
from utility_classes.dwell_functionality import DwellOnScatter

#-----------------------------------------------------------------------------

class PosterKeyboard(DwellOnScatter, VKeyboard, Scatter):
    # needed so we can unbind from the from_keyboard property later on
    linked_to_object = ObjectProperty(None, allownone = True)

    link_colour = ListProperty([1,1,1,0.2])

    link_width = NumericProperty(6)

    draw_arrow_head_on_link = BooleanProperty(False)

    #-------------------------------------------------------------------------

    # this is complex, because the item being binded to, is blind of
    # the object observing it, so need an indirect way of achieving
    # observation to work. this is required because when a note (for example),
    # moves from the world space to poster space, the on_center observer
    # will stop firing, which was used to update the link position,
    # because now it technically never moves, what moves is the parent
    # transformation of the poster that the item is currently within
    # so we have to tell our keyboard observer, to now observe the parent
    # of the object linked to
    # Note: (1) if this method is called, and value is none, then it works
    #           as an unbind method
    #       (2) it can also be supplied with a value (i.e. linked object parent)
    #           such that it is manually bound (important for the use case where
    #           the linked object (i.e. note/title) starts off already with a parent
    def monitor_parent_for_redraw_link(self, instance=None, value=None):
        prev = None
        try:
            prev = self.linked_to_object_parent
        except:
            pass

        if getattr(value, "typename", None)=="PosterBackground":
            value.bind(center=self.redraw_link)
            # needed to force the l_x, l_y in the re-draw method to update (because of the change in co-ordinate systems)
            self.redraw_link()
            self.linked_to_object_parent = value
        else:
            if prev is not None:
                self.linked_to_object_parent.unbind(center=self.redraw_link)
                self.linked_to_object_parent = None

    #-------------------------------------------------------------------------

    def refresh(self, force=False):
        super(PosterKeyboard, self).refresh(force)

        # add the remove link button (center dictates its location)
        if self.linked_to_object is not None:
            self.remove_widget(self.remove_link_button)
            self.remove_link_button.center = (self.width/2, self.height+5)
            self.add_widget(self.remove_link_button)

        # add the close keyboard button (center dictates its location)
        self.remove_widget(self.close_button)
        self.close_button.center = (self.width-20, self.height-20)
        self.add_widget(self.close_button)

    #-------------------------------------------------------------------------

    # using a base (rgb) colour, let this be a wrapper method for:
    # - background color
    # - key normal color
    # - link colour
    # - key down colour
    def set_colour(self, base_colour):
        r,g,b = base_colour
        self.background_color=[r,g,b,0.6]
        self.key_normal_color = [r+0.2,g+0.2,b+0.2,1]
        self.link_colour = [r,g,b,0.2]
        self.key_down_color=[r,g,b,1]

        # bs-kivy library code, bloody listener was doing nothing.. so subtle
        # taking a stab in the dark, this appears to force the color to refresh
        self.refresh_keys()



    #-------------------------------------------------------------------------

    def disconnect_linked_object_from_keyboard(self):
        if self.linked_to_object is not None:
            self.unbind(on_key_down=self.linked_to_object.from_keyboard)
            self.linked_to_object.unbind(center=self.redraw_link)
            self.monitor_parent_for_redraw_link()
            self.linked_to_object = None
            self.remove_widget(self.remove_link_button)
            self.redraw_link()

    #-------------------------------------------------------------------------

    def close_keyboard(self):
        # disconnect any attached item
        self.disconnect_linked_object_from_keyboard()

        # remove from the widget tree (if applicable)
        if self.parent is not None:
            self.parent.remove_widget(self)

    #-------------------------------------------------------------------------

    def __init__(self, **kwargs):
        super(PosterKeyboard, self).__init__(**kwargs)

        # initialise the remove link button (but do not attach to the canvas)
        self.remove_link_button = DwellScatterImageButton(size=(30, 30),
                                                          source="images/assets/deattach_new.png",
                                                          ignore_double_tap=False,
                                                          color=[1,1,1,1])
        self.remove_link_button.function_callback = "self.parent.disconnect_linked_object_from_keyboard()"

        # initialise the close button (but do not attach to the canvas)
        self.close_button = DwellScatterImageButton(size=(25, 25),
                                                    source="images/assets/button_delete.png",
                                                    ignore_double_tap=False,
                                                    color=[1,1,1,0.75])
        self.close_button.function_callback = "self.parent.close_keyboard()"

    #-------------------------------------------------------------------------

    # provide fake expectant variables, so as to allow the signature to work
    # with the observers for on_center for other objects being
    # bound to call this method
    def redraw_link(self, instance=None, value=None):
        root = App.get_running_app().root

        if root is not None:
            root.canvas.after.remove_group(str(self.uid))

            if self.linked_to_object is not None:

                # find out the vectors for the keyboard (in objects (its) co-ordinates)
                a = Vector(*self.center)
                b = Vector(a[0], a[1]+10)
                v = b-a
                vup = v.rotate(self.rotation)
                #vl = vup.rotate(90)  # rotation is anti-clockwise
                #vr = vup.rotate(-90) # rotation is anti-clockwise
                vup = vup.normalize()
                #vl = vl.normalize()
                #vr = vr.normalize()

                center = a

                up_half = vup*self.size[1]/2*self.scale
                #left_half = vl*self.size[0]/2*self.scale
                #right_half = -left_half

                # positions representing the object, have to use vectors, as otherwise pos, etc. gives back the bounding box instead
                top_center   = center + up_half
                #top_left     = center + left_half  + up_half
                #top_right    = center + right_half + up_half
                #bottom_left  = center + left_half  - up_half
                #bottom_right = center + right_half - up_half

                # figure out the vectors for the linked object (in object co-ordinates)
                la = Vector(*self.linked_to_object.center)
                lb = Vector(la[0], la[1]+10)
                lv = lb-la
                lvup = lv.rotate(self.linked_to_object.rotation)
                lvl = lvup.rotate(90)  # rotation is anti-clockwise
                #lvr = lvup.rotate(-90) # rotation is anti-clockwise
                lvup = lvup.normalize()
                lvl = lvl.normalize()
                #lvr = lvr.normalize()

                lcenter = la

                lup_half = lvup*self.linked_to_object.size[1]/2*self.linked_to_object.scale
                lleft_half = lvl*self.linked_to_object.size[0]/2*self.linked_to_object.scale
                lright_half = -lleft_half

                # positions representing the object, have to use vectors, as otherwise pos, etc. gives back the bounding box instead
                #ltop_center    = lcenter + lup_half
                #lbottom_center = lcenter - lup_half
                #lleft_center   = lcenter + lleft_half
                #lright_center  = lcenter + lright_half
                ltop_left      = lcenter + lleft_half  + lup_half
                ltop_right     = lcenter + lright_half + lup_half
                lbottom_left   = lcenter + lleft_half  - lup_half
                lbottom_right  = lcenter + lright_half - lup_half

                wk_top_center    = self.to_window(*top_center)
                wl_center        = self.linked_to_object.to_window(*lcenter)

                # this is where you can do the code for the intersection testing
                wl_top_left     = self.linked_to_object.to_window(*ltop_left)
                wl_top_right    = self.linked_to_object.to_window(*ltop_right)
                wl_bottom_left  = self.linked_to_object.to_window(*lbottom_left)
                wl_bottom_right = self.linked_to_object.to_window(*lbottom_right)

                # quit when we find the first intersection, else quit when at the end
                shouldDraw = False
                while True:
                    # bottom line
                    intersects, collinear, position = Vector.line_segment_intersection(wk_top_center, wl_center, wl_bottom_left, wl_bottom_right)
                    if intersects and collinear=="not-collinear":
                        x2, y2 = position
                        shouldDraw = True
                        break

                    # top line
                    intersects, collinear, position = Vector.line_segment_intersection(wk_top_center, wl_center, wl_top_left, wl_top_right)
                    if intersects and collinear=="not-collinear":
                        x2, y2 = position
                        shouldDraw = True
                        break

                    # right side
                    intersects, collinear, position = Vector.line_segment_intersection(wk_top_center, wl_center, wl_bottom_right, wl_top_right)
                    if intersects and collinear=="not-collinear":
                        x2, y2 = position
                        shouldDraw = True
                        break

                    # left side
                    intersects, collinear, position = Vector.line_segment_intersection(wk_top_center, wl_center, wl_bottom_left, wl_top_left)
                    if intersects and collinear=="not-collinear":
                        x2, y2 = position
                        shouldDraw = True
                        break

                    # default get out of the loop
                    break

                # only draw, if we have a point to draw to
                if shouldDraw is True:
                    x1, y1 = wk_top_center

                    if self.draw_arrow_head_on_link is False:
                        with root.canvas.after:
                            Color(*self.link_colour)

                            # main line
                            Line(points=(x1, y1, x2, y2),
                                 width=self.link_width,
                                 group=str(self.uid))

                            Color(1,1,1,.1)

                            # main line
                            Line(points=(x1, y1, x2, y2),
                                 width=self.link_width/3.0,
                                 group=str(self.uid))

                    else:
                        _a = Vector(x1, y1)
                        _b = Vector(x2, y2)
                        _v = _b-_a

                        _vl = _v.rotate(140)
                        _vl = _vl.normalize()

                        _vr = _v.rotate(-140)
                        _vr = _vr.normalize()

                        end_point_left  = _b+_vl*20
                        end_point_right = _b+_vr*20

                        with root.canvas.after:
                            Color(*self.link_colour)

                            # main line
                            Line(points=(x1, y1, x2, y2),
                                 width=self.link_width,
                                 group=str(self.uid))

                            # left end point
                            Line(points=(end_point_left.x, end_point_left.y, x2, y2),
                                 width=self.link_width,
                                 group=str(self.uid))

                            # right end point
                            Line(points=(end_point_right.x, end_point_right.y, x2, y2),
                                 width=self.link_width,
                                 group=str(self.uid))

                            Color(1,1,1,.1)

                            # main line
                            Line(points=(x1, y1, x2, y2),
                                 width=self.link_width/3.0,
                                 group=str(self.uid))

                            # left end point
                            Line(points=(end_point_left.x, end_point_left.y, x2, y2),
                                 width=self.link_width/3.0,
                                 group=str(self.uid))

                            # right end point
                            Line(points=(end_point_right.x, end_point_right.y, x2, y2),
                                 width=self.link_width/3.0,
                                 group=str(self.uid))


                # refresh the scene, which adds the line disconnect button
                self.refresh()

    #-------------------------------------------------------------------------

    def on_center(self, instance, value):
        self.redraw_link()

    #-------------------------------------------------------------------------

    def on_touch_down(self, touch):
        #touch.push()
        #touch.apply_transform_2d(self.to_local)
        #if self.close_button.collide_point(touch.x, touch.y):
        #    self.close_button.on_touch_down(touch)
        #    touch.pop()
        #    return True
        #touch.pop()

        if self.remove_link_button.parent is not None:
            # then check it first for intersection, otherwise do normal
            # since they keyboard seems to use a different collide method
            touch.push()
            touch.apply_transform_2d(self.to_local)

            if self.remove_link_button.collide_point(touch.x, touch.y):
                self.remove_link_button.on_touch_down(touch)
                touch.pop()
                return True
            touch.pop()

        handled = super(PosterKeyboard, self).on_touch_down(touch)

        return handled

    #-------------------------------------------------------------------------

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return False

        handled = super(PosterKeyboard, self).on_touch_move(touch)

        if handled:
            siblings = self.parent.children
            for sibling in siblings:

                keyboard_can_link_to = getattr(sibling, "keyboard_can_link_to", False)

                if keyboard_can_link_to:
                    if sibling.collide_point(*touch.pos):
                        # found a note/title to link to
                        if self.linked_to_object is None:
                            self.linked_to_object = sibling
                            self.bind(on_key_down=sibling.from_keyboard)

                            # bind the linked object center property to call
                            # the keyboard redraw_link method, which refreshes the
                            # connection of the link between the keyboard
                            # and note/title
                            sibling.bind(center=self.redraw_link)
                            sibling.bind(parent=self.monitor_parent_for_redraw_link)
                        elif self.linked_to_object == sibling:
                            # found self, nothing to do, already bound
                            break
                        else:
                            # unbind from existing
                            self.unbind(on_key_down=self.linked_to_object.from_keyboard)

                            # unbind the drawing method
                            self.linked_to_object.unbind(center=self.redraw_link)
                            self.monitor_parent_for_redraw_link()

                            # bind to new
                            self.linked_to_object = sibling
                            self.bind(on_key_down=sibling.from_keyboard)
                            sibling.bind(center=self.redraw_link)
                            sibling.bind(parent=self.monitor_parent_for_redraw_link)
                        break

                # Might be the case that the note we are trying to link to, happens to be inside of a poster background
                # Account for this case
                elif getattr(sibling, "typename", None)=="PosterBackground":
                    for poster_child in sibling.children:

                        keyboard_can_link_to = getattr(poster_child, "keyboard_can_link_to", False)

                        if keyboard_can_link_to:
                            print "test"
                            # change the touch from the world to poster background co-ordinate system
                            x,y = sibling.to_local(touch.pos[0], touch.pos[1])
                            if poster_child.collide_point(x,y):
                                if self.linked_to_object is None:
                                    self.linked_to_object = poster_child
                                    self.bind(on_key_down=poster_child.from_keyboard)
                                    poster_child.bind(center=self.redraw_link)
                                    poster_child.bind(parent=self.monitor_parent_for_redraw_link)
                                    self.monitor_parent_for_redraw_link(value=poster_child.parent)
                                elif self.linked_to_object == poster_child:
                                    # found self, nothing to do, already bound
                                    return handled
                                else:
                                    # unbind from existing
                                    self.unbind(on_key_down=self.linked_to_object.from_keyboard)
                                    self.linked_to_object.unbind(center=self.redraw_link)
                                    self.monitor_parent_for_redraw_link()

                                    # bind to new
                                    self.linked_to_object = poster_child
                                    self.bind(on_key_down=poster_child.from_keyboard)
                                    poster_child.bind(center=self.redraw_link)
                                    poster_child.bind(parent=self.monitor_parent_for_redraw_link)
                                    self.monitor_parent_for_redraw_link(value=poster_child.parent)
                                return handled

        return handled

    #-------------------------------------------------------------------------

#-----------------------------------------------------------------------------
