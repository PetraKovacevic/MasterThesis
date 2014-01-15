import kivy
kivy.require('1.6.0')

# Grab the directory where the current script is located in (different to where it is being called from)
import inspect
import os
current_path_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#-----------------------------------------------------------------------------
# Config
# Read a local configuration file (instead of using the global one that is located
# in %userprofile%/.kivy
from kivy.config import Config
config_application_file_path = current_path_directory + os.sep + "config" + os.sep + "config_application.ini"
Config.read(config_application_file_path)


# Modules
# Configure all activated modules
# Config.set for modules seems to be broken, so you must specify this in the config file
# If using a custom config file (e.g. Config.read(filename)), then, you must
# run the 2 lines below:
from kivy.modules import Modules
Modules.configure()


from kivy.lang import Builder


# Custom Project Widgets

# Note: Should be a subfolder within the main project
project_widgets_directory_name = "project_widgets"

project_widgets_directory_full_path = current_path_directory + os.sep + project_widgets_directory_name

# Search through the ajc_widgets directory and grab all the kv files
for kv_file in [file for file in os.listdir(project_widgets_directory_full_path) if file[-3:] == ".kv"]:
    kv_file_full_path = project_widgets_directory_full_path + os.sep + kv_file
    Builder.load_file(kv_file_full_path, rulesonly=True)

# Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty

from Selection1Widget import Selection1Widget
from nameTagWidget import NameTagWidget
from messageWidget import MessageWidget
from messageMoreTimeWidget import MessageMoreTimeWidget
from messageViewingTurnWidget import MessageViewingTurnWidget
from utility_classes.dwell_functionality import *
from clockWidget import ClockWidget
from project_widgets.vertical_scroller import VerticalScroller
from project_widgets.picture import *
from project_widgets.note import Note
from project_widgets.poster_keyboard import PosterKeyboard
from rotateButton import RotateButton

from functools import partial
from random import randint



print "The current path is :" + current_path_directory + "-------------------------------------------"
# Load the .kv files
Builder.load_file(current_path_directory + '\selection1Widget.kv')
Builder.load_file(current_path_directory + '\\nameTagWidget.kv')
Builder.load_file(current_path_directory + '\messageWidget.kv')
Builder.load_file(current_path_directory + '\messageMoreTimeWidget.kv')
Builder.load_file(current_path_directory + '\messageViewingTurnWidget.kv')
Builder.load_file(current_path_directory + '\clockWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'rotateButton.kv')

## Hard coded information about user name tag locations (center + angle) and user colours
numberOfUsers = 4

userLocation = [[[683, 47.5, 0], [683, 720.5, 180]],
				[[47.5, 384, -90], [683, 47.5, 0], [1318.5, 384, 90]],
				[[47.5, 384, -90], [683, 47.5, 0], [1318.5, 384, 90], [683, 720.5, 180]],
				[[47.5, 384, -90], [683, 47.5, 0], [1318.5, 384, 90], [924.5, 720.5, 180], [441.5, 720.5, 180]],
				[[47.5, 384, -90], [441.5, 47.5, 0], [924.5, 47.5, 0], [1318.5, 384, 90], [924.5, 720.5, 180], [441.5, 720.5, 180]]]

imageScrollerLocation = [[[683, 175, 0], [683, 593, 180]],
						[[175, 384, -90], [683, 175, 0], [1191, 384, 90]],
						[[175, 384, -90], [683, 175, 0], [1191, 384, 90], [683, 593, 180]],
						[[175, 384, -90], [683, 175, 0], [1191, 384, 90], [924.5, 593, 180], [441.5, 593, 180]],
						[[175, 384, -90], [441.5, 175, 0], [924.5, 175, 0], [1191, 384, 90], [924.5, 593, 180], [441.5, 593, 180]]]
				
# red, green, blue, purple, magenta, cyan, yellow
userColours = [[1, 0, 0, 0.6], [0, 1, 0, 0.6], [0, 0, 1, 0.6],
			[0.4, 0, 0.4, 0.6], [1, 1, 0, 0.6], [0, 1, 1, 0.6], [1, 0, 1, 0.6]]
		
class shareOneAtATime(Widget):

	countdown_start = 30
	
	message = MessageWidget()
	
	messageMoreTime = MessageMoreTimeWidget()
	
	clock = ClockWidget()
	
	track_user = NumericProperty()
	
	def __init__(self, options, stage_duration, **kwargs):
		super(shareOneAtATime, self).__init__(**kwargs)
		
		self.countdown_start = stage_duration*60
		self.options = options
		
		self.initialize()
		
	def initialize(self):
		
		# add message that tells user to share
		self.track_user = 1
		self.message.user = str(self.track_user)
		self.message.center = (683, 384)
		self.add_widget(self.message)
		
		self.messageMoreTime.center = (683, 384)
	
	def start(self):
	
		# Add the image scroller for the current user
		self.parent.add_image_scroller(self.track_user)
		
		# add clock widget and start the countdown
		self.clock.call_function = self.time_run_out
		self.add_widget(self.clock)
		#self.clock.countdown(self.countdown_start)
		self.clock.start(self.countdown_start)		
	
	# function to call when the time runs out
	def time_run_out(self):
		if self.track_user <= numberOfUsers:
			self.add_widget(self.messageMoreTime)
			
			if self.options['disable']:
				self.parent.set_disable(False)
	
	# This function os called only from messageWidget when the user presses a button to stop
	def stop_clock(self):
		self.clock.stop_clock()
	
	# Message More Time
	# When the user presses the YES button this method is called
	# The current user does not change; Clock starts again for the user
	def yes_pressed(self):
		self.parent.set_disable(True)
		self.remove_widget(self.messageMoreTime)
		#self.clock.countdown(self.countdown_start)
		self.clock.start(self.countdown_start)	
	
	# Message More Time
	# When the user presses the NO button this method is called
	# Images for the previous user are shown; The current user changes; Clock starts for new user
	def no_pressed(self):
		if self.track_user < numberOfUsers:
		
			if self.options['disable']:
				self.parent.set_disable(True)
				
			self.remove_widget(self.messageMoreTime)
			self.track_user = self.track_user + 1
			self.message.user = str(self.track_user)
			self.parent.add_image_scroller(self.track_user)
			#self.clock.countdown(self.countdown_start)
			self.clock.start(self.countdown_start)	
		else:
			self.parent.call_stage2()
		
class shareAllAtOnce(Widget):

	countdown_start = 30
	
	message = MessageWidget()
	
	messageMoreTime = MessageMoreTimeWidget()
	
	clock = ClockWidget()
	
	track_user = NumericProperty()
	
	def __init__(self, options, stage_duration, **kwargs):
		super(shareAllAtOnce, self).__init__(**kwargs)
		
		self.countdown_start = stage_duration*60
		self.options = options
		
		self.initialize()
	
	def initialize(self):
		
		#add message that tells user to share
		#to do: add a different message: everybody must share
		self.track_user = 1
		self.message.user = str(self.track_user)
		self.message.center = (683, 384)
		self.add_widget(self.message)
		
		self.messageMoreTime.center = (683, 384)
		
	def start(self):
	
		# Add the image scroller for the current user
		for user_num in range(numberOfUsers):
			self.parent.add_image_scroller(user_num)
		
		# Add clock widget and start the countdown
		self.clock.call_function = self.time_run_out
		self.add_widget(self.clock)
		#self.clock.countdown(5)
		self.clock.start(self.countdown_start)
	
	# function to call when the time runs out
	def time_run_out(self):
		self.add_widget(self.messageMoreTime)
		
		if self.options['disable']:
				self.parent.set_disable(False)
				
	# This function os called only from messageWidget when the user presses a button to stop
	def stop_clock(self):
		self.clock.stop_clock()
			
	# Message More Time
	# When the user presses the YES button this method is called
	# Clock starts again
	def yes_pressed(self):
		self.remove_widget(self.messageMoreTime)
		#self.clock.countdown(5)
		self.clock.start(self.countdown_start)
	
	# Message More Time
	# When the user presses the NO button this method is called
	# Images for the previous user are shown; The current user changes; Clock starts for new user
	def no_pressed(self):
	
		if self.options['disable']:
				self.parent.set_disable(True)
				
		self.remove_widget(self.messageMoreTime)
		self.parent.call_stage2()
		
class viewingInformation(Widget):

	# This is part 1 of the discussion stage
	# Users explain what kind of information they have gathered by taking turns
	# Only the images/notes of the user who's turn it is can be moved around the table
	# This is used to keep everybody focused only on the user who is explaining
				
	messageTurn = MessageViewingTurnWidget()
	
	messageMoreTime = MessageMoreTimeWidget()
	
	clock = ClockWidget()
				
	track_user = NumericProperty()
	
	countdown_start = NumericProperty(5)
	
	def __init__(self, **kwargs):
		super(viewingInformation, self).__init__(**kwargs)
		
		self.initialize()
	
	def initialize(self):
		
		# Add message that tells user to share
		self.track_user = 1
		self.messageTurn.user = str(self.track_user)
		self.messageTurn.center = (683, 384)
		self.add_widget(self.messageTurn)
		
		self.messageMoreTime.center = (683, 384)
		
	def start(self):
		
		# Add clock widget and start the countdown
		if (self.clock.parent == None):
			self.clock.call_function = self.time_run_out
			self.add_widget(self.clock)
		#self.clock.countdown(5)
		self.clock.start(self.countdown_start)			
			
	# Function to call when the time runs out
	def time_run_out(self):
		if self.track_user <= numberOfUsers:
			self.add_widget(self.messageMoreTime)
	
	# Message More Time
	# When the user presses the YES button this method is called
	# The current user does not change; Clock starts again for the user
	def yes_pressed(self):
		self.remove_widget(self.messageMoreTime)
		#self.clock.countdown(5)
		self.clock.start(self.countdown_start)
	
	# Message More Time
	# When the user presses the NO button this method is called
	# The current user changes; Clock starts for new user
	def no_pressed(self):
		self.remove_widget(self.messageMoreTime)
		
		if self.track_user < numberOfUsers:
			self.track_user = self.track_user + 1
			self.messageTurn.user = str(self.track_user)
			self.add_widget(self.messageTurn)
		else:
			self.parent.call_stage3()
			
	def ok_pressed(self):
		self.remove_widget(self.messageTurn)
		self.start()
		
class groupingInformation(Widget):
	pass
	
class posterCreation(Widget):
	pass

class MainWidget(Widget):
	
	selection1 = Selection1Widget()
	stage2 = viewingInformation()
	disable_touch = BooleanProperty(False)
	stage3 = posterCreation()
	
	# For testing images scroller
	fullpath = []
	description = []
	image_num = 0
	
	track_user = 0
	
	scroller = VerticalScroller(scrollview_height = 150, rotation = 180,
                                scrollview_width = 600, border_width = 30,
                                background_colour = [0,0,0,0.5],
                                description = "User Pictures")

	def __init__(self, **kwargs):
		# make sure we aren't overriding any important functionality
		super(MainWidget, self).__init__(**kwargs)
		
		self.initialize()
		
	def initialize(self):
	
		# Get the location information
		user_loc = userLocation[numberOfUsers - 2]
		
		# Add a nametag widget for each user
		for user_num in range(numberOfUsers):
			widget = NameTagWidget(user = str(user_num + 1), color = userColours[user_num])
			widget.center_x = user_loc[user_num][0]
			widget.center_y = user_loc[user_num][1]
			widget.angle = user_loc[user_num][2]
			self.add_widget(widget)
			
		#self.call_selection1()
		#self.selection1.center = (683, 383)
		
		#self.call_stage1()
		
		#self.call_stage2()
		
		#self.add_widget(self.stage1)
		#self.stage1.start()
		
		self.call_stage3()
		
		# Getting the paths for the images
		# Fake adding images to the scroller view
		for top, dirs, files in os.walk(current_path_directory+os.sep+"user_images"):
			for f in Utilities.natural_sort(files):
				#fullpath = os.path.join(top, f)
				self.fullpath.append(os.path.join(top, f))
				#description = f.split(".")[0]
				self.description.append(f.split(".")[0])
		
		# Button for faking adding the images to the scroller view
		button = Button(text='Add Image', font_size=14, pos = (0, 0))
		button.bind(on_press=self.callback)
		self.add_widget(button)
		
	def callback(self, instance):
		widgetId = "user" + str(self.track_user)
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		if self.image_num < len(self.fullpath):
			picture = Picture(source = self.fullpath[self.image_num],
								description = self.description[self.image_num],
								description_background_colour = [0,.5,.5,1])
			
			if self.stage1_options['colour']:
				picture.border_colour = userColours[self.track_user - 1]
			
			scroller.add_item(picture)
			self.image_num = self.image_num + 1
			
	def add_image_scroller(self, user_num):
		self.track_user = user_num
		self.image_num = 0
		
		user_scroller_loc =	imageScrollerLocation[numberOfUsers - 2]

		widget = VerticalScroller(scrollview_height = 100,
									scrollview_width = 350, border_width = 30,
									description = "User Pictures", id = "user" + str(user_num))
		
		# Colour coded or not
		'''if self.stage1_options['colour']:
			widget.background_colour = userColours[user_num - 1]
		else:
			widget.background_colour = [0,0,0,0.5]'''
			
		widget.background_colour = [0,0,0,0.5]

		widget.center_x = user_scroller_loc[user_num - 1][0]
		widget.center_y = user_scroller_loc[user_num - 1][1]
		widget.rotation = user_scroller_loc[user_num - 1][2]
		self.add_widget(widget)
		
	def call_selection1(self):
		self.selection1.pos = (0, 0)
		self.selection1.size = (1366, 768)
		self.add_widget(self.selection1)
		
	def call_stage1(self, options, stage_duration):
		self.stage1_options = options
		self.remove_widget(self.selection1)
		
		# Disable tabletop interaction??
		if self.stage1_options['disable']:
			self.set_disable(True)
		
		# What stage was selected??
		if self.stage1_options['sharing']:
			self.stage1 = shareOneAtATime(options, stage_duration)
		else:
			self.stage1 = shareAllAtOnce(options, stage_duration)
			
		self.add_widget(self.stage1)
		self.stage1.start()
		
	def call_stage2(self):
		self.remove_widget(self.stage1)
		#
		self.add_widget(self.stage2)
		#self.stage2.start()
		
	def call_stage3(self):
		# 1.Add the note icon and keyboard icon next to the nametag
		# 2.Add functionality --> When you press the note icon, a note appears in the persons colour
		#					  --> When you press the keyboard icon, a keyboard appears on the table
		user_loc = userLocation[numberOfUsers - 2]
		
		for user_num in range(numberOfUsers):
		
			button_note = RotateButton(user = user_num + 1)
			button_note.bind(on_press = self.callback_note)
			
			button_keyboard = RotateButton (user = user_num + 1)
			button_keyboard.bind(on_press = self.callback_keyboard)
			
			button_note.angle = user_loc[user_num][2]
			button_note.size = (80, 80)
			
			button_keyboard.angle = user_loc[user_num][2]
			button_keyboard.size = (80, 80)
			
			if user_loc[user_num][2] == 0:
				button_note.center_x = user_loc[user_num][0] + 130
				button_note.center_y = user_loc[user_num][1]
				
				button_keyboard.center_x = user_loc[user_num][0] - 130
				button_keyboard.center_y = user_loc[user_num][1]
			elif user_loc[user_num][2] == 180:
				button_note.center_x = user_loc[user_num][0] - 130
				button_note.center_y = user_loc[user_num][1]
				
				button_keyboard.center_x = user_loc[user_num][0] + 130
				button_keyboard.center_y = user_loc[user_num][1]
			elif user_loc[user_num][2] == -90:
				button_note.center_x = user_loc[user_num][0]
				button_note.center_y = user_loc[user_num][1] - 130
				
				button_keyboard.center_x = user_loc[user_num][0]
				button_keyboard.center_y = user_loc[user_num][1] + 130
			elif user_loc[user_num][2] == 90:
				button_note.center_x = user_loc[user_num][0]
				button_note.center_y = user_loc[user_num][1] + 130
				
				button_keyboard.center_x = user_loc[user_num][0]
				button_keyboard.center_y = user_loc[user_num][1] - 130
				
			button_note.background_normal = current_path_directory+os.sep+"images"+os.sep+"note.png"
			button_note.background_down = current_path_directory+os.sep+"images"+os.sep+"note.png"
			
			button_keyboard.background_normal = current_path_directory+os.sep+"images"+os.sep+"keyboard.png"
			button_keyboard.background_down = current_path_directory+os.sep+"images"+os.sep+"keyboard.png"

			self.add_widget(button_note)
			self.add_widget(button_keyboard)
			
	def callback_note(self, instance):
		note = Note()
		note.text = "Write something"
		note.pos = (800, 500)
		note.colour = userColours[instance.user - 1]
		note.border_colour = userColours[instance.user - 1]
		note.keyboard_can_link_to = True
		self.add_widget(note)
		
	def callback_keyboard(self, instance):
		print "Keyboard " + str(instance.user)
		mykeyboard = PosterKeyboard(size_hint_x = None, size_hint_y=None)
		mykeyboard.pos = (100, 280)
		mykeyboard.set_colour((0.8,0.8,0.8)) # grey
		self.add_widget(mykeyboard)
		
	def on_touch_down(self, touch):
		if self.disable_touch:
			return True
		else:
			handled = super(MainWidget, self).on_touch_down(touch)
			
	def set_disable(self, disable):
		self.disable_touch = disable
		

class MainApp(App):
	def build(self):
		#return shareOneAtATime()
		return MainWidget()
		
if __name__ == '__main__':
    MainApp().run()