##############################################################################

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty

##############################################################################
from utility_classes.utilities import Utilities


class DwellBase(object):
    # objects to track the current touch for the dwell operation
    dwell_started_counter = NumericProperty(0)
    dwell_started_by_touch = ObjectProperty(None, allownone=True)

    # bypass variable, if you want to toggle double tap on/off on a widget
    ignore_double_tap = BooleanProperty(True)

    # bypass variable, if you want to toggle dwell on/off on a widget
    ignore_dwell = BooleanProperty(False)

    # ------------------------------------------------------------------------

    def __init__(self, **kwargs):
        self.dwell_color = [eval(n) for n in Config.get('dwell', 'dwell_color').split(',')]
        self.dwell_width = Config.getfloat('dwell', 'dwell_width')
        self.dwell_time  = Config.getfloat('dwell', 'dwell_time')
        self.dwell_jitter_distance_ignore = Config.getfloat('dwell', 'dwell_jitter_distance_ignore')
        self.dwell_initial_wait_period  = Config.getfloat('dwell', 'dwell_initial_wait_period')

        # Add-on hack at the last moment, need the touch info from the dwell
        self.dwell_touch = None
        self.double_tap_touch = None

        super(DwellBase, self).__init__(**kwargs)

    # ------------------------------------------------------------------------

    # Called after a finger is continuous held for 2 seconds on a widget with the Dwell mixin
    def dwell(self):
        print "got to dwell in the DWELL class [default function]"

    # ------------------------------------------------------------------------

    def double_tap(self):
        print "got to double_tap in the DWELL class [default function]"

    # ------------------------------------------------------------------------

    # Create a clock callback to get to the dwell operation
    def process_dwell(self, dt):
        self.dwell_started_counter += 0.05

        root = App.get_running_app().root
        root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])

        with root.canvas:
            Color(*self.dwell_color)
            x, y = self.dwell_started_by_touch.pos
            sx = sy = self.dwell_width
            percent_complete = (self.dwell_started_counter+0.05)/self.dwell_time

            Ellipse(source='images/dot.png',
                size=(sx, sy),
                angle_start=0,
                angle_end=percent_complete*360.0,
                pos=(x-sx/2.0, y-sy/2.0),
                group=str(self.dwell_started_by_touch.uid),
                segments=percent_complete*50)

        if abs(self.dwell_started_counter-self.dwell_time) < 0.00001: # compare double within error epsilon
            self.dwell_started_counter = 0 # set the counter to 0
            if self.dwell_started_by_touch is not None:
                root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])

            # DATABASE MARK - needed for the database
            self.dwell_touch = self.dwell_started_by_touch

            self.dwell_started_by_touch = None
            self.dwell() # execute the dwell
        else:
            Clock.schedule_once(self.process_dwell, 0.05) #, else keep iterating until time hit

    # ------------------------------------------------------------------------

##############################################################################

class DwellOnLeafWidget(DwellBase):

    # ------------------------------------------------------------------------
    # re-write the way touch down is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)

            if self.ignore_double_tap is False:
                if touch.is_double_tap:
                    self.double_tap_touch = touch

                    self.double_tap()

            if self.ignore_dwell is not True:
                self.dwell_started_counter = 0 # start a counter
                self.dwell_started_by_touch = touch
                touch.ud['dwell'] = str(touch.uid)
                Clock.schedule_once(self.process_dwell,self.dwell_initial_wait_period) # start a recursive callback
                return True

        return False

    # ------------------------------------------------------------------------
    # re-write the way touch move is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return False

        # does this even do anything?, i think it just dispatches?
        #super(DwellOnWidget, self).on_touch_move(touch)

        if self.ignore_dwell is not True:
            #if self.collide_point(*touch.pos): # check dwell on myself, not the kids (todo: refine?)
            if self.dwell_started_by_touch != touch:
                self.dwell_started_counter = 0
                if self.dwell_started_by_touch is not None:
                    root = App.get_running_app().root
                    root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
                self.dwell_started_by_touch = None
                Clock.unschedule(self.process_dwell)
            else:
                # rather than base the calculation on the last touch frame, which means the user might be so slow, that a dwell follows them
                # base it on the original touch position, with the dwell_jitter_distance essentially mimicing a radius
                # around which a point can be within for the dwell to not be cancelled out
                diff = [abs(i-j) for i, j in zip(self.dwell_started_by_touch.opos,self.dwell_started_by_touch.pos)]
                #if abs(self.dwell_started_by_touch.dx) >= self.dwell_jitter_distance_ignore or abs(self.dwell_started_by_touch.dy) >= self.dwell_jitter_distance_ignore:
                if diff[0] >= self.dwell_jitter_distance_ignore or diff[1] >= self.dwell_jitter_distance_ignore:
                    self.dwell_started_counter = 0
                    if self.dwell_started_by_touch is not None:
                        root = App.get_running_app().root
                        root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
                    self.dwell_started_by_touch = None
                    Clock.unschedule(self.process_dwell)
                else:
                    pass
                    # ignore small movements of the finger

            return True

        return False


    # ------------------------------------------------------------------------
    # re-write the way touch up is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False

        #super(DwellOnWidget, self).on_touch_up(touch)

        if self.ignore_dwell is not True:

            #if self.collide_point(touch.x, touch.y):
            self.dwell_started_counter = 0
            if self.dwell_started_by_touch is not None:
                root = App.get_running_app().root
                root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
            self.dwell_started_by_touch = None
            Clock.unschedule(self.process_dwell)

            touch.ungrab(self)
            return True

        return False

    # ------------------------------------------------------------------------

##############################################################################

class DwellOnScatter(DwellBase):
    ignore_momentum = BooleanProperty(True) # by default ignore momentum

    # ------------------------------------------------------------------------

    def __init__(self, **kwargs):
        super(DwellOnScatter, self).__init__(**kwargs)

        self.global_ignore_momentum = Config.getboolean('dwell', 'global_ignore_momentum')

        # Do not do momentum if change in dx, dy due to rotational change
        # Only apply momentum for translations
        self.original_rotation = 0

    # ------------------------------------------------------------------------
    # re-write the way touch down is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_down(self, touch):
        self.original_rotation = self.rotation
		
        # does a grab in the super
        handled = super(DwellOnScatter, self).on_touch_down(touch)

        if handled:
            touch_from_child = touch.ud.get('touch_passed_upwards', False)

            # To check double tap
            #if self.collide_point(touch.x, touch.y): # use this to check it hit was to myself and not my kids, Todo: might need to refine this
            #    print "is this touch a double tap?------------------------->", touch.is_double_tap

            # double tap code
            if self.ignore_double_tap is False:
                # ajc - march 17, 2013
                # check for the presence of a field that tells us, that the touch was handled, due to passing the touch
                # from the child to the parent (as set in scatter.py)
                if touch.is_double_tap and (self.collide_point(touch.x, touch.y) or touch_from_child) : # use this to check it hit was to myself and not my kids, Todo: might need to refine this
                    # DATABASE MARK - line needed for database
                    self.double_tap_touch = touch

                    self.double_tap()
                    #print "is this touch a double tap?------------------------->", touch.is_double_tap


            if self.ignore_dwell is not True:
                if self.collide_point(touch.x, touch.y) or touch_from_child: # use this to check it hit was to myself and not my kids, Todo: might need to refine this
                    if len(self._touches) == 1:
                        self.dwell_started_counter = 0 # start a counter
                        self.dwell_started_by_touch = touch
                        touch.ud['dwell'] = str(touch.uid)
                        Clock.schedule_once(self.process_dwell,self.dwell_initial_wait_period) # start a recursive callback
                    else:
                        self.dwell_started_counter = 0 # reset the counter
                        if self.dwell_started_by_touch is not None:
                            root = App.get_running_app().root
                            root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
                        self.dwell_started_by_touch = None
                        Clock.unschedule(self.process_dwell) # remove the callback

                        #print "touches = ", len(self._touches) # debug

            #Clock.unschedule(self.inertial_translation)

        return handled

    # ------------------------------------------------------------------------
    # re-write the way touch move is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return False
        
        handled = super(DwellOnScatter, self).on_touch_move(touch)
		
        
        if handled:
            if self.ignore_dwell is not True:
                #if self.collide_point(touch.x, touch.y): # check dwell on myself, not the kids (todo: refine?)
                if self.dwell_started_by_touch != touch:
                    self.dwell_started_counter = 0
                    if self.dwell_started_by_touch is not None:
                        root = App.get_running_app().root
                        root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
                    self.dwell_started_by_touch = None
                    Clock.unschedule(self.process_dwell)
                else:
                    # rather than base the calculation on the last touch frame, which means the user might be so slow, that a dwell follows them
                    # base it on the original touch position, with the dwell_jitter_distance essentially mimicing a radius
                    # around which a point can be within for the dwell to not be cancelled out
                    diff = [abs(i-j) for i, j in zip(self.dwell_started_by_touch.opos,self.dwell_started_by_touch.pos)]
                    #if abs(self.dwell_started_by_touch.dx) >= self.dwell_jitter_distance_ignore or abs(self.dwell_started_by_touch.dy) >= self.dwell_jitter_distance_ignore:
                    if diff[0] >= self.dwell_jitter_distance_ignore or diff[1] >= self.dwell_jitter_distance_ignore:
                        self.dwell_started_counter = 0
                        if self.dwell_started_by_touch is not None:
                            root = App.get_running_app().root
                            root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
                        self.dwell_started_by_touch = None
                        Clock.unschedule(self.process_dwell)
                    else:
                        pass # ignore little movements

        return handled

    # ------------------------------------------------------------------------

    # Implementation for momentum based on:
    # https://groups.google.com/forum/?fromgroups=#!topic/kivy-users/YGaa-dmVLZE

    # Momentum implementation
    def inertial_translation(self, time):
        #print abs(self.dx), 0.003 * self.width, abs(self.dy), 0.003 * self.height
        if abs(self.dx) > 0.003 * self.width and abs(self.dy) > 0.003 * self.height:
            self.pos = [self.x + self.dx, self.y + self.dy]
            self.center = Utilities.clamp(*self.center) # Todo: this needs to be removed to a gloabl class!

            # If the item gets near the edge, kill the schedule function on it, as it will just waste cycles
            if self.center[0]-15 < 0 or\
               self.center[0]+15 > Utilities.window_width or \
               self.center[1] -15 < 0 or \
               self.center[1] + 15 > Utilities.window_height:
                #self.dx *= 0.1
                #self.dy *= 0.1
                Clock.unschedule(self.inertial_translation)
                return

            # friction (1= glides forever)/ rate of decay
            try:
                if self.linked_children:
                    self.dx *= 0.8
                    self.dy *= 0.8
                else:
                    self.dx *= 0.9
                    self.dy *= 0.9
            except Exception, e:
                self.dx *= 0.93
                self.dy *= 0.93

        else:
            Clock.unschedule(self.inertial_translation)

    # ------------------------------------------------------------------------
    # re-write the way touch up is handled,
    # do all the standard stuff, and em-bue with
    # necessary code for a dwell operation to occur
    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return False

        handled = super(DwellOnScatter, self).on_touch_up(touch)

        if self.ignore_dwell is not True:
            #if self.collide_point(touch.x, touch.y):
            self.dwell_started_counter = 0
            if self.dwell_started_by_touch is not None:
                root = App.get_running_app().root
                root.canvas.remove_group(self.dwell_started_by_touch.ud['dwell'])
            self.dwell_started_by_touch = None
            Clock.unschedule(self.process_dwell)

        if self.global_ignore_momentum is False:
            # Set up momentum
            if not self.ignore_momentum:
                if  self.do_translation_x is True and \
                    self.do_translation_y is True and \
                    abs(self.rotation-self.original_rotation) < 0.01:
                    # check's that we haven't rotated, else the vectors for momentum will be off

                    # tries to do a cheap check, if we haven't moved much, stop momentum from firing
                    if touch.time_end-touch.time_update < 0.15:
                        self.dx = touch.dx
                        self.dy = touch.dy
                        Clock.schedule_interval(self.inertial_translation, 0.02)

        return handled

    # ------------------------------------------------------------------------

##############################################################################