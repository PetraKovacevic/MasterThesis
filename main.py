#-----------------------------------------------------------------------------

import kivy
kivy.require('1.6.0')

#-----------------------------------------------------------------------------
# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

# noinspection PyUnresolvedReferences
from twisted.internet import reactor

# noinspection PyUnresolvedReferences
from handlers.handler_filename_receiver import FilenameReceiverServer

# noinspection PyUnresolvedReferences
from handlers.network_factories import TCPServerFactoryWithRoot

#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------
# On the fly figure out the computer's ip address, and open up a listener
# Since a laptop/computer might have more than 1 active ip address
if Config.getboolean('input', 'tuio_allow_external'):
    import socket
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    for index, ip_address in enumerate(ip_addresses):
        # Taken care of in the config, and when there is a network connection, the gethostname, will override
        # the default 127.0.0.1 field with a real ip address, so if there is no net, this basically means
        # it will try to add this line twice under input and that will cause an attribute error
        # put a clause to guard against that happening
        if ip_address != "127.0.0.1":
            Config.set('input', 'tuio_from_external_source_%s' % index, 'tuio,%s:3333' % ip_address)



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
from kivy.core.window import Window

from project_widgets.Selection1Widget import Selection1Widget
from project_widgets.selectionTransferWidget import SelectionTransferWidget
from project_widgets.selectionDisableWidget import SelectionDisableWidget
from project_widgets.selection2DisableWidget import Selection2DisableWidget
from project_widgets.selectionColourWidget import SelectionColourWidget
from project_widgets.selectionTimeWidget import SelectionTimeWidget
from project_widgets.Selection2Widget import Selection2Widget
from project_widgets.selection3Widget import Selection3Widget
from project_widgets.nameTagWidget import NameTagWidget
from project_widgets.messageWidget import MessageWidget
from project_widgets.messageWidget2 import MessageWidget2
from project_widgets.messageMoreTimeWidget import MessageMoreTimeWidget
from project_widgets.moreTime import MoreTime
from project_widgets.messageCancelClockWidget import MessageCancelClockWidget
from project_widgets.messageClock import MessageClock
from project_widgets.messageViewingTurnWidget import MessageViewingTurnWidget
from project_widgets.messageViewingTurn import MessageViewingTurn
from utility_classes.dwell_functionality import *
from project_widgets.clockWidget import ClockWidget
from project_widgets.vertical_scroller import VerticalScroller
from project_widgets.picture import *
from project_widgets.note import Note
from project_widgets.poster_keyboard import PosterKeyboard
from project_widgets.rotateButton import RotateButton
from project_widgets.application_background import ApplicationBackground
from project_widgets.poster_background import PosterBackground
from project_widgets.stage1MessageWidget import Stage1MessageWidget
from project_widgets.chooseWidget import ChooseWidget
from project_widgets.stage3MessageWidget import Stage3MessageWidget
from project_widgets.selection3KeyboardWidget import Selection3KeyboardWidget

from functools import partial
from random import randint



print "The current path is :" + current_path_directory + "-------------------------------------------"
# Load the .kv files
'''Builder.load_file(current_path_directory + '\selection1Widget.kv')
Builder.load_file(current_path_directory + '\selection2Widget.kv')
Builder.load_file(current_path_directory + '\selection3Widget.kv')
Builder.load_file(current_path_directory + '\\nameTagWidget.kv')
Builder.load_file(current_path_directory + '\messageWidget.kv')
Builder.load_file(current_path_directory + '\messageWidget2.kv')
Builder.load_file(current_path_directory + '\messageMoreTimeWidget.kv')
Builder.load_file(current_path_directory + '\moreTime.kv')
Builder.load_file(current_path_directory + '\messageViewingTurnWidget.kv')
Builder.load_file(current_path_directory + '\messageViewingTurn.kv')
Builder.load_file(current_path_directory + '\clockWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'rotateButton.kv')
Builder.load_file(current_path_directory + os.sep + 'stage1MessageWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selectionTransferWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selectionDisableWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selection2DisableWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selectionColourWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selectionTimeWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'messageCancelClockWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'backgroundColorWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'messageClock.kv')
Builder.load_file(current_path_directory + os.sep + 'ChooseWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'stage3MessageWidget.kv')
Builder.load_file(current_path_directory + os.sep + 'selection3KeyboardWidget.kv')'''


## Hard coded information about user name tag locations (center + angle) and user colours
numberOfUsers = 0

userLocation2 = []
imageScrollerLocation2 = []

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
userColours = [[1, 0, 0, 0.6],  # red
			   [0.4, 0, 0.4, 0.6], # this is purple (not green)
			   [0, 0, 1, 0.6], # blue
			   [0, 1, 0, 0.6], # this is green (not purple)
			   [1, 1, 0, 0.6], # magenta
			   [0, 1, 1, 0.6], # cyan
			   [1, 0, 1, 0.6]] # yellow

import datetime
import time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print st
f=open(current_path_directory + os.sep + str(ts) + '.txt', 'w+')
f.write("Date: " + st + "\n")

class BackgroundColorWidget(Widget):
	pass
		
class shareOneAtATime(Widget):

	countdown_start = 30
	
	message = MessageWidget()
	
	#messageMoreTime = MessageMoreTimeWidget()
	messageMoreTime = MoreTime()
	
	# To Do: Add at least one more clock
	clock = ClockWidget(id = "clock1")
	
	track_user = NumericProperty()
	
	backgroundWidget = BackgroundColorWidget()
	
	def __init__(self, options, stage_duration, **kwargs):
		super(shareOneAtATime, self).__init__(**kwargs)
		
		# Divide the stage duration into equal parts for each user.
		self.countdown_start = int(stage_duration*60/numberOfUsers)
		self.options = options
		
		f.write("Stage 1 Transfer one at a time\n")
		f.write("Time for individual: " + str(self.countdown_start/60) + " minutes \n")
	
	def start(self):
	
		app = App.get_running_app().root
		self.height = app.height
		self.width = app.width
		
		self.track_user = 1
		f.write("User " + str(self.track_user ) + "\n")
		
		self.message.user = str(self.track_user)
		self.message.angle = userLocation2[self.track_user - 1][2]
		self.message.center = self.get_message_center()
		
		self.add_widget(self.message)
	
		# Add the image scroller for the current user
		self.parent.add_image_scroller(self.track_user)
		
		# Add button that simulates iPad -- needs to be deleted when iPads are added
		self.parent.add_button_add_images()
		
		# add clock widget and start the countdown
		self.clock.call_function = self.time_run_out
		self.clock.center = (40, self.height - 60)
		
		#self.clock2.call_function = self.time_run_out
		#self.clock2.angel = -90
		#self.clock2.center = (self.width - 40, 60)
		
		self.add_widget(self.clock)
		#self.add_widget(self.clock2)
		
		self.clock.start(self.countdown_start)	
		#self.clock2.start(self.countdown_start)	

		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)	

		self.messageMoreTime.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		#self.messageMoreTime.center = self.get_message_center()
		self.messageMoreTime.rotation = userLocation2[self.track_user - 1][2]
		
		#self.messageMoreTime.size = self.parent.size
		#self.messageMoreTime.pos = (0, 0)
	
	# function to call when the time runs out
	def time_run_out(self):
		if self.track_user <= numberOfUsers:
			# Add the black see through background
			self.parent.add_widget(self.backgroundWidget)
			
			# Add the message widget
			self.parent.add_widget(self.messageMoreTime)
			
			'''if self.options['disable']:
				self.parent.set_disable(False)'''
	
	# After the Cancel Clock message, if the user presses Yes then this method is called to stop the clock
	def stop_clock(self):
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		self.parent.remove_widget(self.backgroundWidget)
		
		time = self.clock.stop_clock()
		f.write("Stopped clock at: " + time + "\n")
		
		self.no_pressed()
		
	# Call this function when the clock is tapped to ask the user if they want to stop the clock
	def cancel_clock(self):
		
		# Add the black see through background
		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)
		self.parent.add_widget(self.backgroundWidget)
		
		# Add the message widget
		# To Do: Make the message clock widget, do you need more time widget and it's your turn widget closer to each user -- depends on the number of users
		# and locations
		cancel_message = MessageClock(id = "cancel_message")
		cancel_message.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		cancel_message.rotation = userLocation2[self.track_user - 1][2]
		self.parent.add_widget(cancel_message)
	
	# If user decides not to stop the clock then resume from where the clock stopped
	def resume_clock(self):
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		self.parent.remove_widget(self.backgroundWidget)
		
		self.clock.resume()
	
	# Message More Time
	# When the user presses the YES button this method is called
	# The current user does not change; Clock starts again for the user
	def yes_pressed(self):
		#self.parent.set_disable(True)
		
		f.write("More time: Yes\n")
		
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageMoreTime)
		self.clock.start(self.countdown_start)	
	
	# Message More Time
	# When the user presses the NO button this method is called
	# Images for the previous user are shown; The current user changes; Clock starts for new user
	def no_pressed(self):
		
		f.write("More time: No\n")
		
		if self.track_user < numberOfUsers:
		
			'''if self.options['disable']:
				self.parent.set_disable(True)'''
			
			self.parent.remove_widget(self.backgroundWidget)
			self.parent.remove_widget(self.messageMoreTime)
			
			self.track_user = self.track_user + 1
			
			f.write("User " + str(self.track_user) + "\n")
			
			self.message.user = str(self.track_user)
			self.message.angle = userLocation2[self.track_user - 1][2]
			self.message.center = self.get_message_center()
			
			self.messageMoreTime.rotation = userLocation2[self.track_user - 1][2]
			#self.messageMoreTime.center = self.get_message_center()
			self.parent.add_image_scroller(self.track_user)
			
			# Add button that simulates iPad -- needs to be deleted when iPads are added
			self.parent.add_button_add_images()
			
			#self.clock.countdown(self.countdown_start)
			self.clock.start(self.countdown_start)	
		else:
			self.parent.remove_widget(self.backgroundWidget)
			self.parent.remove_widget(self.messageMoreTime)
			self.parent.call_selection2()
	
	def get_message_center(self):
		if userLocation2[self.track_user - 1][2] == 0 or userLocation2[self.track_user - 1][2] == 180:
			center = (self.width/2, self.height/2)
		elif userLocation2[self.track_user - 1][2] == -90:
			center = (self.width/4, self.height/2)
		elif userLocation2[self.track_user - 1][2] == 90:
			center = (self.width*3/4, self.height/2)
			
		return center
		
class shareAllAtOnce(Widget):

	countdown_start = 30
	
	message = MessageWidget2()
	
	#messageMoreTime = MessageMoreTimeWidget()
	messageMoreTime = MoreTime()
	
	clock = ClockWidget()
	
	track_user = NumericProperty()
	
	backgroundWidget = BackgroundColorWidget()
	
	def __init__(self, options, stage_duration, **kwargs):
		super(shareAllAtOnce, self).__init__(**kwargs)
		
		f.write("Stage 1 Transfer all at once\n")
		
		self.countdown_start = int(stage_duration*60)
		self.options = options
		
	def start(self):
	
		app = App.get_running_app().root
		self.height = app.height
		self.width = app.width
		
		self.track_user = 1
		self.message.user = str(self.track_user)
		self.message.center = (self.width/2, self.height/2)
		self.add_widget(self.message)
	
		# Add the image scroller for the current user
		for user_num in range(numberOfUsers):
			self.parent.add_image_scroller(user_num + 1)
			
		self.parent.add_button_all_at_once()
		
		# Add clock widget and start the countdown
		self.clock.call_function = self.time_run_out
		self.clock.center = (40, self.height - 60)
		#self.clock.bind(on_touch_down=self.stop_clock)
		self.add_widget(self.clock)
		#self.clock.countdown(5)
		self.clock.start(self.countdown_start)
		
		#self.messageMoreTime.size = self.parent.size
		#self.messageMoreTime.pos = (0, 0)
		
		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)
		
		self.messageMoreTime.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.messageMoreTime.rotation = 0
	
	# function to call when the time runs out
	def time_run_out(self):
		# Add the message widget
		self.parent.add_widget(self.backgroundWidget)
		self.parent.add_widget(self.messageMoreTime)
		'''if self.options['disable']:
				self.parent.set_disable(False)'''
				
	# After the Cancel Clock message, if the user presses Yes then this method is called to stop the clock
	def stop_clock(self):
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		self.parent.remove_widget(self.backgroundWidget)
				
		time = self.clock.stop_clock()
		f.write("Stopped clock at: " + time + "\n")
		
		self.no_pressed()
		
	# Call this function when the clock is tapped to ask the user if they want to stop the clock
	def cancel_clock(self):
	
		# Add the black see through background
		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)
		self.parent.add_widget(self.backgroundWidget)
		
		# Add the message widget
		cancel_message = MessageClock(id = "cancel_message")
		cancel_message.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		cancel_message.rotation = 0
		self.parent.add_widget(cancel_message)
		
		'''cancel_message = MessageCancelClockWidget(id = "cancel_message")
		cancel_message.size = self.parent.size
		cancel_message.pos = (0, 0)
		self.parent.add_widget(cancel_message)'''
	
	# If user decides not to stop the clock then resume from where the clock stopped
	def resume_clock(self):
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		self.parent.remove_widget(self.backgroundWidget)
				
		self.clock.resume()
			
	# Message More Time
	# When the user presses the YES button this method is called
	# Clock starts again
	def yes_pressed(self):
		
		f.write("More time: Yes\n")
		
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageMoreTime)

		self.clock.start(self.countdown_start)
	
	# Message More Time
	# When the user presses the NO button this method is called
	# Images for the previous user are shown; The current user changes; Clock starts for new user
	def no_pressed(self):
		
		f.write("More time: No\n")
	
		'''if self.options['disable']:
				self.parent.set_disable(True)'''
		
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageMoreTime)
		self.parent.call_selection2()
		
class viewingInformation(Widget):

	# Users explain what kind of information they have gathered by taking turns
	# Only the images/notes of the user who's turn it is can be moved around the table --> this is an otpion
	# This is used to keep everybody focused only on the user who is explaining
				
	#messageTurn = MessageViewingTurnWidget()
	
	messageTurn = MessageViewingTurn()
	
	#messageMoreTime = MessageMoreTimeWidget()
	messageMoreTime = MoreTime()
	
	clock = ClockWidget()
				
	track_user = NumericProperty()
	
	countdown_start = NumericProperty(5)
	
	backgroundWidget = BackgroundColorWidget(id = "background")
	
	def __init__(self, stage_duration, **kwargs):
		super(viewingInformation, self).__init__(**kwargs)
		
		self.countdown_start = int(stage_duration*60/numberOfUsers)
		
		f.write("Stage 2 Discussion\n")
		f.write("Time for individual: " + str(self.countdown_start/60) + " minutes\n")
		
		self.track_user = 1
		self.messageTurn.user = str(self.track_user)
		
		f.write("User " + str(self.track_user ) + "\n")
		
	def start(self):
		
		self.parent.add_garbage_bin()
		self.parent.enable_user_scroller(self.track_user)
		
		#self.messageTurn.size = self.parent.size
		#self.messageTurn.pos = (0, 0)
		
		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)
		self.parent.add_widget(self.backgroundWidget)
		
		self.messageTurn.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.messageTurn.rotation = userLocation2[self.track_user - 1][2]
		self.parent.add_widget(self.messageTurn)

		self.messageMoreTime.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.messageMoreTime.rotation = userLocation2[self.track_user - 1][2]
		
		# Add clock widget and start the countdown
		if (self.clock.parent == None):
			self.clock.call_function = self.time_run_out
			self.clock.center = (40, self.parent.height - 60)
			#self.clock.bind(on_touch_down=self.stop_clock)
			self.add_widget(self.clock)
		
	# After the Cancel Clock message, if the user presses Yes then this method is called to stop the clock
	def stop_clock(self):
		self.parent.remove_widget(self.backgroundWidget)
		
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		time = self.clock.stop_clock()
		f.write("Stopped clock at: " + time + "\n")
		
		self.no_pressed()
		
	# Call this function when the clock is tapped to ask the user if they want to stop the clock
	def cancel_clock(self):
	
		# Add the black see through background
		self.backgroundWidget.size_hint = (None, None)
		self.backgroundWidget.size = (self.parent.width, self.parent.height)
		self.backgroundWidget.pos = (0, 0)
		self.parent.add_widget(self.backgroundWidget)
		
		# Add the message widget
		cancel_message = MessageClock(id = "cancel_message")
		cancel_message.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		cancel_message.rotation = userLocation2[self.track_user - 1][2]
		self.parent.add_widget(cancel_message)
		
		'''cancel_message = MessageCancelClockWidget(id = "cancel_message")
		cancel_message.size = self.parent.size
		cancel_message.pos = (0, 0)
		self.parent.add_widget(cancel_message)'''
	
	# If user decides not to stop the clock then resume from where the clock stopped
	def resume_clock(self):
		for child in self.parent.children[:]:
			if child.id == "cancel_message":
				self.parent.remove_widget(child)
				
		self.parent.remove_widget(self.backgroundWidget)
				
		self.clock.resume()
			
	# Function to call when the time runs out
	def time_run_out(self):
		if self.track_user <= numberOfUsers:
			# Add the black see through background
			self.parent.add_widget(self.backgroundWidget)
			
			# Add the message widget
			self.parent.add_widget(self.messageMoreTime)
	
	# Message More Time
	# When the user presses the YES button this method is called
	# The current user does not change; Clock starts again for the user
	def yes_pressed(self):
		
		f.write("More time: Yes\n")
		
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageMoreTime)
		self.clock.start(self.countdown_start)
	
	# Message More Time
	# When the user presses the NO button this method is called
	# The current user changes; Clock starts for new user
	def no_pressed(self):
		
		f.write("More time: No\n")
		
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageMoreTime)
		
		if self.track_user < numberOfUsers:
			self.track_user = self.track_user + 1
			f.write("User " + str(self.track_user ) + "\n")
			self.messageTurn.user = str(self.track_user)
			self.messageTurn.rotation = userLocation2[self.track_user - 1][2]
			
			self.messageMoreTime.rotation = userLocation2[self.track_user - 1][2]
			
			self.parent.add_widget(self.backgroundWidget)
			self.parent.add_widget(self.messageTurn)
		else:
			self.remove_widget(self.clock)
			#self.parent.call_stage3()
			self.parent.call_selection3()
			
	def ok_pressed(self):
		self.parent.remove_widget(self.backgroundWidget)
		self.parent.remove_widget(self.messageTurn)
		self.parent.enable_user_scroller(self.track_user)
		self.clock.start(self.countdown_start)
		#self.start()
		
class groupingInformation(Widget):
	pass
	
class posterCreation(Widget):
	pass

class MainWidget(FloatLayout):

	clock = ClockWidget()
	
	backgroundwidget = BackgroundColorWidget(id = "background")
	
	selection1 = Selection1Widget()
	selection2 = Selection2Widget()
	selection3 = Selection3Widget()
	#stage2 = viewingInformation()
	disable_touch = BooleanProperty(False)
	stage3 = posterCreation()
	
	stage1options = {}
	stage2options = {}
	stage3options = {}
	
	selection_tracker = 1
	stage_tracker = 1
	
	buttons = []
	
	# For testing images scroller
	fullpath = []
	description = []
	
	fullpath1 = []
	description1= []
	
	fullpath2 = []
	description2 = []
	
	fullpath3 = []
	description3 = []
	
	all_fullpath = []
	all_description = []
	
	number_of_notes = []
	
	image_num = 0
	image_num1 = 0
	image_num2 = 0
	image_num3 = 0
	
	track_user = 0
	
	scripting = False
	
	# Track the activity for when the buttons are being used
	track_activtiy = 1

	def __init__(self, **kwargs):
		# make sure we aren't overriding any important functionality
		super(MainWidget, self).__init__(**kwargs)
		
		self.setup()
		
	def initialize(self):
		
		print "Current path -- initilaize: " + current_path_directory
		if self.track_activity == 1:
			path1 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User1"+os.sep+"User Study 1"
			path2 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User2"+os.sep+"User Study 1"
			path3 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User3"+os.sep+"User Study 1"
		elif self.track_activity == 2:
			path1 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User1"+os.sep+"User Study 2"
			path2 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User2"+os.sep+"User Study 2"
			path3 = current_path_directory+os.sep+"user_images"+os.sep+"Photos for user study"+os.sep+"User3"+os.sep+"User Study 2"

			
		# Get the image paths for all the users
		for top, dirs, files in os.walk(path1):
			for f in Utilities.natural_sort(files):
				#fullpath = os.path.join(top, f)
				self.fullpath1.append(os.path.join(top, f))
				#description = f.split(".")[0]
				self.description1.append(f.split(".")[0])
				
		self.all_fullpath.append(self.fullpath1)
		self.all_description.append(self.description1)
				
		for top, dirs, files in os.walk(path2):
			for f in Utilities.natural_sort(files):
				#fullpath = os.path.join(top, f)
				self.fullpath2.append(os.path.join(top, f))
				#description = f.split(".")[0]
				self.description2.append(f.split(".")[0])
		
		self.all_fullpath.append(self.fullpath2)
		self.all_description.append(self.description2)
		
		for top, dirs, files in os.walk(path3):
			for f in Utilities.natural_sort(files):
				#fullpath = os.path.join(top, f)
				self.fullpath3.append(os.path.join(top, f))
				#description = f.split(".")[0]
				self.description3.append(f.split(".")[0])
		
		self.all_fullpath.append(self.fullpath3)
		self.all_description.append(self.description3)
		
		print self.all_fullpath
		
		# Getting the paths for the images
		# Fake adding images to the scroller view
		'''for top, dirs, files in os.walk(current_path_directory+os.sep+"user_images"):
			for f in Utilities.natural_sort(files):
				#fullpath = os.path.join(top, f)
				self.fullpath.append(os.path.join(top, f))
				#description = f.split(".")[0]
				self.description.append(f.split(".")[0])'''
		
		# Button for faking adding the images to the scroller view
		# Only add button if we don't have a phone on us.
		if Config.getboolean('options', 'need_hardcoded_script_add_image_button') is True:
			self.button = RotateButton(text='Add Image', font_size=14, pos = (0, 0), id = "button_add_image")
			self.button.bind(on_press=self.callback)
			self.button.size_hint = (None, None)
		#self.add_widget(button)
		
		#Clock.schedule_once(self.start, 1)
		
		#self.setup()
		
	def setup(self):
		print "I'm in setup"
	
		self.stage1options.clear()
		self.stage2options.clear()
		self.stage3options.clear()
		
		del userLocation2[:]
		del imageScrollerLocation2[:]
		
		del self.fullpath1[:]
		del self.description1[:]
		
		del self.fullpath2[:]
		del self.description2[:]
		
		del self.fullpath3[:]
		del self.description3[:]
		
		del self.all_fullpath[:]
		del self.all_description[:]
		
		del self.number_of_notes[:]
		
		for child in self.children[:]:
			self.remove_widget(child)
			
		self.stage_tracker = 1
		self.selection_tracker = 1
		self.track_user = 0
		self.scripting = False
		
		self.number_of_notes = []
			
		# Only for moderator to choose what version of the program to use during user study
		chooseWidget = ChooseWidget(pos = (0, 0), id = 'choose')
		chooseWidget.size_hint = (None, None)
		chooseWidget.size = (1366, 768)
		self.add_widget(chooseWidget)
		
	#def start(self, dt):
	def start(self, num, option, user):
		
		f.write("\nNumber of users: " + str(num) + "\n")
		f.write("Scripted version? " + str(option) + "\n")
		f.write("User study: " + str(user) + "\n")
		
		self.track_activity = user
		
		for i in range(num):
			self.number_of_notes.append(0)
		
		if Config.getboolean('options', 'need_hardcoded_script_add_image_button') is True:
			print "calling initialize"
			self.initialize()
		
		# Remove the choose widget
		for child in self.children[:]:
			if child.id == 'choose':
				self.remove_widget(child)
	
		global numberOfUsers
		numberOfUsers = num
	
		app = App.get_running_app().root
		self.height = app.height
		self.width = app.width
						
		# Create the locations for nametag and image scroller
		if numberOfUsers == 2:
			userLocation2.append([self.width/2, 40, 0])
			userLocation2.append([self.width/2, self.height - 40, 180])
			
			imageScrollerLocation2.append([self.width/2, 130, 0])
			imageScrollerLocation2.append([self.width/2, self.height - 130, 180])
		elif numberOfUsers in range(3, 5): 
			userLocation2.append([40, self.height/2, -90])
			userLocation2.append([self.width/2, 40, 0])
			userLocation2.append([self.width - 40, self.height/2, 90])
			userLocation2.append([self.width/2, self.height - 40, 180])
			
			imageScrollerLocation2.append([130, self.height/2, -90])
			imageScrollerLocation2.append([self.width/2, 130, 0])
			imageScrollerLocation2.append([self.width - 130, self.height/2, 90])
			imageScrollerLocation2.append([self.width/2, self.height - 130, 180])
		elif numberOfUsers in [5, 6]:
			userLocation2.append([40, self.height/2, -90])
			userLocation2.append([self.width/4, 40, 0])
			userLocation2.append([self.width*3/4, 40, 0])
			userLocation2.append([self.width - 40, self.height/2, 90])
			
			imageScrollerLocation2.append([130, self.height/2, -90])
			imageScrollerLocation2.append([self.width/4, 130, 0])
			imageScrollerLocation2.append([self.width*3/4, 130, 0])
			imageScrollerLocation2.append([self.width - 130, self.height/2, 90])
			
			if numberOfUsers == 6: 
				userLocation2.append([self.width*3/4, self.height - 40, 180])
				userLocation2.append([self.width/4, self.height - 40, 180])
				
				imageScrollerLocation2.append([self.width*3/4, self.height - 130, 180])
				imageScrollerLocation2.append([self.width/4, self.height - 130, 180])
			else:
				userLocation2.append([self.width/2, self.height - 40, 180])
				
				imageScrollerLocation2.append([self.width/2, self.height - 130, 180])
			
		# Get the location information
		#user_loc = userLocation[numberOfUsers - 2]
		user_loc = userLocation2
		
		# Add a nametag widget for each user
		for user_num in range(numberOfUsers):
			widget = NameTagWidget(user = str(user_num + 1), color = userColours[user_num])
			widget.center_x = user_loc[user_num][0]
			widget.center_y = user_loc[user_num][1]
			widget.angle = user_loc[user_num][2]
			widget.size_hint = (None, None)
			self.add_widget(widget)
			
		if option is True:
			timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			f.write("Start option selection for stage 1 at " + timestamp + "\n")
			self.add_widget(Stage1MessageWidget(id = 'stage1message', pos = (0, 0), size = self.size))
			self.scripting = True
			print "It's true"
		else:
			self.withoutScripting()
			self.scripting = False
			print "It's false"
		
		#self.add_widget(SelectionTransferWidget(pos = (0, 0), id = '1'))
		
		#self.call_selection1()
		#self.selection1.center = (683, 383)
		
		#self.call_stage1()
		
		#self.call_stage2()
		
		#self.add_widget(self.stage1)
		#self.stage1.start()
		
		#self.call_stage3()
	
	def withoutScripting(self):
		self.stage1options['disable'] = False
		
		if Config.getboolean('options', 'need_hardcoded_script_add_image_button') is True:
			self.add_button_all_at_once()
		
		# Add the image scroller for all the users
		for user_num in range(numberOfUsers):
			self.add_image_scroller(user_num + 1)
			
		self.add_garbage_bin()
			
		self.call_stage3()

	def add_picture_from_phone_to_users_scroller(self, user, filename_path, description, is_scripted):
		# find the correct scroller thing (adapted from looking at the callback function)
		widgetId = "user{0}".format(user)
		scroller = None
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		print user

		# guard against not being able to find the scroller
		if scroller is None:
			return False

		# don't add duplicates (i.e. same image sent 5 times, only allow to go into the scroller once).
		for picture in scroller.items.children:
			if picture.source == filename_path:
				return False

		# Clean up the description slightly from the filename to present on the screen
		parts = description.split(".")
		parts = ".".join(parts[:-1]) # remove the .jpg/.png junk
		parts = parts.split("_") # make underscores less ugly.
		parts = " ".join(parts)
		description = parts

		# load into memory
		picture = Picture(source = filename_path,
						  description = description,
						  description_background_colour = [0,.5,.5,1])

		#if is_scripted:
		if self.scripting:
			if self.stage1options['colour']:
				picture.border_colour = userColours[user - 1]
				picture.description_background_colour = userColours[user - 1] # update the colour of the filename label
		else:
				picture.border_colour = userColours[user - 1]
				picture.description_background_colour = userColours[user - 1] # update the colour of the filename label

		scroller.add_item(picture)

		# give feedback to send back to phone
		return True

	def process_image_from_phone(self, user, filename_path, description):
		if self.scripting is False or (self.scripting and self.stage1options['sharing'] is False):
			# Code for the non-scripting version
			return self.add_picture_from_phone_to_users_scroller(user, filename_path, description, False)

		else:
			# Code for the scripting version
			if user != self.track_user:
				# Ignore if we received a file from a user, when it was not their turn
				return False

			return self.add_picture_from_phone_to_users_scroller(user, filename_path, description, True)

	def callback(self, instance):
		widgetId = "user" + str(self.track_user)
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		fullpath = self.all_fullpath[self.track_user - 1]
		description = self.all_description[self.track_user - 1]
				
		if self.image_num < len(fullpath):
			picture = Picture(source = fullpath[self.image_num],
								description = description[self.image_num],
								description_background_colour = [0,.5,.5,1])
			
			if self.stage1options['colour']:
				picture.border_colour = userColours[self.track_user - 1]
			
			scroller.add_item(picture)
			self.image_num = self.image_num + 1
			
	def callback1(self, instance):
		widgetId = "user" + instance.id.split("_")[1]
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		if self.image_num1 < len(self.fullpath1):
			picture = Picture(source = self.fullpath1[self.image_num1],
								description = self.description1[self.image_num1],
								description_background_colour = [0,.5,.5,1],
								id = self.description1[self.image_num1])	
			
			if self.scripting is True:
				print "callback1 im in"
				if self.stage1options['colour']:
					print "I've passed the color"
					picture.border_colour = userColours[0]
			
			scroller.add_item(picture)
			self.image_num1 = self.image_num1 + 1
			
	def callback2(self, instance):
		widgetId = "user" + instance.id.split("_")[1]
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		if self.image_num2 < len(self.fullpath2):
			picture = Picture(source = self.fullpath2[self.image_num2],
								description = self.description2[self.image_num2],
								description_background_colour = [0,.5,.5,1])
			
			if self.scripting is True:
				if self.stage1options['colour']:
					picture.border_colour = userColours[1]
			
			scroller.add_item(picture)
			self.image_num2 = self.image_num2 + 1
			
	def callback3(self, instance):
		widgetId = "user" + instance.id.split("_")[1]
		for child in self.children:
			if child.id == widgetId:
				scroller = child
				
		if self.image_num3 < len(self.fullpath3):
			picture = Picture(source = self.fullpath3[self.image_num3],
								description = self.description3[self.image_num3],
								description_background_colour = [0,.5,.5,1])
			
			if self.scripting is True:
				if self.stage1options['colour']:
					picture.border_colour = userColours[2]
			
			scroller.add_item(picture)
			self.image_num3 = self.image_num3 + 1
			
	def add_button_add_images(self):
		if Config.getboolean('options', 'need_hardcoded_script_add_image_button') is False:
			return

		# Change the location of the button depending on which users turn it is
		if self.track_user == 1:
			if numberOfUsers in range(3, 7):
				self.button.pos = (0, 0)
				self.button.angle = -90
			elif numberOfUsers == 2:
				self.button.pos = (self.width - 100, 0)
				self.button.angle = 0
			self.add_widget(self.button)
				
		elif self.track_user == 2:
			if numberOfUsers in range(3, 6):
				self.button.pos = (self.width - 100, 0)
				self.button.angle = 0
			elif numberOfUsers == 2:
				self.button.pos = (100, self.height - 100)
				self.button.angle = 180
			#elif numberOfUsers == 6:
			
			
		elif self.track_user == 3:
			self.button.pos = (self.width - 100, self.height - 100)
			self.button.angle = 90
			
		elif self.track_user == 4:
			self.button.pos = (100, self.height - 100)
			self.button.angle = 180
			
	def add_button_all_at_once(self):
		if Config.getboolean('options', 'need_hardcoded_script_add_image_button') is False:
			return
		
		for i in range(1, numberOfUsers + 1):
			button = RotateButton(text='Add Image', font_size=14, id = "buttonaddimage_" + str(i), size_hint = (None, None))
			self.buttons.append(button)
			
			# Change the location of the button depending on which users turn it is
			if i == 1:
				button.bind(on_press=self.callback1)
				if numberOfUsers in range(3, 7):
					button.pos = (0, 0)
					button.angle = -90
				elif numberOfUsers == 2:
					button.pos = (self.width - 100, 0)
					button.angle = 0
					
			elif i == 2:
				button.bind(on_press=self.callback2)
				if numberOfUsers in range(3, 6):
					button.pos = (self.width - 100, 0)
					button.angle = 0
				elif numberOfUsers == 2:
					button.pos = (100, self.height - 100)
					button.angle = 180
				#elif numberOfUsers == 6:
				
				
			elif i == 3:
				button.bind(on_press=self.callback3)
				button.pos = (self.width - 100, self.height - 100)
				button.angle = 90
				
			elif i == 4:
				button.pos = (100, self.height - 100)
				button.angle = 180
				
			self.add_widget(button)
			
	def add_image_scroller(self, user_num):
		self.track_user = user_num
		self.image_num = 0
		
		#user_scroller_loc =	imageScrollerLocation[numberOfUsers - 2]
		user_scroller_loc =	imageScrollerLocation2
		
		widget = VerticalScroller(scrollview_height = 80,
									scrollview_width = 450, border_width = 30,
									description = "User " + str(user_num) + " Pictures", id = "user" + str(user_num))
		
		# Colour coded or not
		'''if self.stage1_options['colour']:
			widget.background_colour = userColours[user_num - 1]
		else:
			widget.background_colour = [0,0,0,0.5]'''
			
		widget.background_colour = [0,0,0,0.5]
		
		widget.center_x = user_scroller_loc[user_num - 1][0]
		widget.center_y = user_scroller_loc[user_num - 1][1]
		widget.rotation = user_scroller_loc[user_num - 1][2]
		
		print user_scroller_loc[user_num - 1]
		
		#print current_path_directory+os.sep+"user_images"+os.sep+"Planning a trip around Australia"+os.sep+"user"+str(user_num)
		'''for top, dirs, files in os.walk(current_path_directory+os.sep+"user_images"+os.sep+"Planning a trip around Australia"+os.sep+"user"+str(user_num)):
			for f in Utilities.natural_sort(files):
				fullpath = os.path.join(top, f)
				print fullpath
				description = f.split(".")[0]
				picture = Picture(source = fullpath,
									description = description,
									description_background_colour = [0,.5,.5,1])
				if self.stage1options['colour']:
					picture.border_colour = userColours[self.track_user - 1]
				
				widget.scroller.bar_color = [0, .7, .7, 1]
				widget.add_item(picture)'''
				
		widget.can_drop_items_in = False
		
		if self.stage1options['disable']:
			#widget.bind(on_touch_down=scroller_touch_down)
			widget.allowed_to_touch = False
		self.add_widget(widget)
		
	def add_background_scroller(self):
	
		user_scroller_loc =	imageScrollerLocation[numberOfUsers - 2]

		widget = VerticalScroller(scrollview_height = 80,
									scrollview_width = 250, border_width = 30,
									description = "Poster Backgrounds")
			
		widget.background_colour = [0,0,0,0.5]
		
		if numberOfUsers == 2:
			widget.center_x = 100
			widget.center_y = self.height/2
			widget.rotation = 90
		else:
			widget.center_x = self.center_x*3/8
			widget.center_y = self.height - 70
		#widget.rotation = user_scroller_loc[user_num - 1][2]
		
		for top, dirs, files in os.walk(current_path_directory+os.sep+"images"+os.sep+"poster_backgrounds"):
			for f in Utilities.natural_sort(files):
				fullpath = os.path.join(top, f)
				description = f.split(".")[0]
				picture = PosterBackground(source = fullpath,
											description = description,
											description_background_colour = [0,.5,.5,1])
					
				widget.scroller.bar_color = [0, .7, .7, 1]
				widget.add_item(picture)
				
		widget.can_drop_items_in = False
			
		self.add_widget(widget)
		
	def add_garbage_bin(self):
		widget = VerticalScroller(scrollview_height = 80,
									scrollview_width = 250, border_width = 30,
									description = "Garbage Bin")
			
		widget.background_colour = [0,0,0,0.5]
	
		if numberOfUsers == 2:
			widget.center_x = self.width - 100
			widget.center_y = self.height/2
			widget.rotation = -90
		else:
			widget.center_x = self.width - 155
			widget.center_y = self.height - 70
		#widget.rotation = user_scroller_loc[user_num - 1][2]
			
		self.add_widget(widget)
		
	def set_options(self, name, option, stage_num = 1):
		
		if self.stage_tracker == 1:
			self.stage1options[name] = option
		elif self.stage_tracker == 2:
			self.stage2options[name] = option
		elif self.stage_tracker == 3:
			self.stage3options[name] = option
		
		# Remove the previous option selection
		for child in self.children[:]:
			if child.id == str(self.selection_tracker):
				self.remove_widget(child)
			if stage_num == 2 and child.id == 'time':
				self.remove_widget(child)
		
		if self.stage_tracker == 1:
			if self.selection_tracker == 1:
				self.add_widget(SelectionDisableWidget(pos = (0, 0), id = '2'))
			elif self.selection_tracker == 2:
				self.add_widget(SelectionColourWidget(pos = (0, 0), id = '3'))
			elif self.selection_tracker == 3:
				stage = SelectionTimeWidget(stage = 1, pos = (0, 0), id = '4')
				if self.stage1options['sharing']:
					stage.stage_duration = 3
				else:
					stage.stage_duration = 1
				self.add_widget(stage)
			else:
				self.call_stage1()
				
		elif self.stage_tracker == 2:
			if self.selection_tracker == 5:
				self.add_widget(SelectionTimeWidget(pos = (0, 0), id = '6', stage_duration = 9))
			else:
				self.call_stage2()
				
		elif self.stage_tracker == 3:
				self.call_stage3()
		
		self.selection_tracker += 1
		
	def call_selection1(self):
	
		app = App.get_running_app().root
	
		# Remove stage1Message widget
		for child in self.children[:]:
			if child.id == 'stage1message':
				print "I've removed Stage1MessageWidget"
				self.remove_widget(child)
				
		self.add_widget(SelectionTransferWidget(pos = (0, 0), id = '1'))
		
		# Add selection1 widget
		'''self.selection1.pos = (0, 0)
		self.selection1.size = self.size
		self.add_widget(self.selection1)'''
		
	'''def call_stage1(self, options, stage_duration):
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
		self.stage1.start()'''
		
	def call_stage1(self):
		timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		f.write("End option selection for stage 1 at " + timestamp + "\n")
		
		f.write("Selection1 options:\n")
		f.write(str(self.stage1options))
		f.write("\n")
		
		# Disable tabletop interaction??
		'''if self.stage1options['disable']:
			self.set_disable(True)'''
		
		# What stage was selected??
		if self.stage1options['sharing']:
			self.stage1 = shareOneAtATime(self.stage1options, self.stage1options['time'], id = "idForRemoving")
		else:
			self.stage1 = shareAllAtOnce(self.stage1options, self.stage1options['time'], id = "idForRemoving")
			
		self.add_widget(self.stage1)
		self.stage1.start()
		
	def call_selection2(self):
	
		timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		f.write("\nStart option selection for stage 2 at " + timestamp + "\n")
		
		self.stage_tracker += 1
		if (Config.getboolean('options', 'need_hardcoded_script_add_image_button') is True):
			if self.stage1options['sharing']:
				self.remove_widget(self.button)
			else:
				for i in range(numberOfUsers):
					self.remove_widget(self.buttons[i])
		
		self.remove_widget(self.stage1)
		
		self.selection2.pos = (0, 0)
		#self.selection2.size = (1366, 768)
		self.selection2.size = (self.width, self.height)
		self.add_widget(self.selection2)
		
	def call_stage2options(self):
		self.remove_widget(self.selection2)
		self.add_widget(Selection2DisableWidget(stage = 2, pos = (0, 0), id = "5" ))
		
	def call_stage2(self):
	
		timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		f.write("End option selection for stage 2 at " + timestamp + "\n")
		
		f.write("Selection 2 options:\n")
		f.write(str(self.stage2options))
		f.write("\n")
		
		self.remove_widget(self.selection2)
		
		# Enable the scrollers if they were disabled
		if self.stage1options['disable'] is True and self.stage2options['disable'] is False:
			for i in range(1, numberOfUsers + 1):
				for child in self.children:
					if child.id == "user" + str(i):
						child.allowed_to_touch = True
		elif self.stage1options['disable'] is False and self.stage2options['disable'] is True:
			for i in range(1, numberOfUsers + 1):
				for child in self.children:
					if child.id == "user" + str(i):
						child.allowed_to_touch = False
			
		self.stage2 = viewingInformation(self.stage2options['time'], id = "idForRemoving")
		self.add_widget(self.stage2)
		self.stage2.start()
		
	def enable_user_scroller(self, scroller_num):
		for child in self.children:
			if child.id == "user" + str(scroller_num):
				child.allowed_to_touch = True
		
	def call_selection3(self):
		self.remove_widget(self.stage2)
		
		self.stage_tracker += 1
		
		self.selection3.pos = (0, 0)
		self.selection3.size = (1366, 768)
		self.add_widget(self.selection3)
		
	def call_stage3options(self):
		self.remove_widget(self.selection3)
		self.add_widget(Selection3KeyboardWidget(stage = 3, pos = (0, 0), id = "7" ))
		
	def call_stage3(self):
		f.write("Stage 3 Poster Creation\n")
		self.remove_widget(self.selection3)
		
		# 1.Add the note icon and keyboard icon next to the nametag
		# 2.Add functionality --> When you press the note icon, a note appears in the persons colour
		#					  --> When you press the keyboard icon, a keyboard appears on the table
		#user_loc = userLocation[numberOfUsers - 2]
		
		user_loc = userLocation2
		
		for user_num in range(numberOfUsers):
		
			button_note = RotateButton(user = user_num + 1)
			button_note.size_hint = (None, None)
			button_note.bind(on_press = self.callback_note)
			
			button_keyboard = RotateButton (user = user_num + 1)
			button_keyboard.size_hint = (None, None)
			button_keyboard.bind(on_press = self.callback_keyboard)
			
			button_note.angle = user_loc[user_num][2]
			button_note.size = (70, 70)
			
			button_keyboard.angle = user_loc[user_num][2]
			button_keyboard.size = (80, 80)
			
			if user_loc[user_num][2] == 0:
				button_note.center_x = user_loc[user_num][0] + 120
				button_note.center_y = user_loc[user_num][1]
				
				button_keyboard.center_x = user_loc[user_num][0] - 120
				button_keyboard.center_y = user_loc[user_num][1] + 5
			elif user_loc[user_num][2] == 180:
				button_note.center_x = user_loc[user_num][0] - 120
				button_note.center_y = user_loc[user_num][1]
				
				button_keyboard.center_x = user_loc[user_num][0] + 120
				button_keyboard.center_y = user_loc[user_num][1]
			elif user_loc[user_num][2] == -90:
				button_note.center_x = user_loc[user_num][0]
				button_note.center_y = user_loc[user_num][1] - 120
				
				button_keyboard.center_x = user_loc[user_num][0]
				button_keyboard.center_y = user_loc[user_num][1] + 120
			elif user_loc[user_num][2] == 90:
				button_note.center_x = user_loc[user_num][0]
				button_note.center_y = user_loc[user_num][1] + 120
				
				button_keyboard.center_x = user_loc[user_num][0]
				button_keyboard.center_y = user_loc[user_num][1] - 120
				
			button_note.background_normal = current_path_directory+os.sep+"images"+os.sep+"note.png"
			button_note.background_down = current_path_directory+os.sep+"images"+os.sep+"note.png"
			
			button_keyboard.background_normal = current_path_directory+os.sep+"images"+os.sep+"keyboard.png"
			button_keyboard.background_down = current_path_directory+os.sep+"images"+os.sep+"keyboard.png"

			self.add_widget(button_note)
			self.add_widget(button_keyboard)
			
		self.add_background_scroller()
		
		# Add clock widget and start the countdown
		if (self.clock.parent == None):
			#self.clock.call_function = self.time_run_out
			self.clock.size_hint = (None, None)
			self.clock.center_x = 40
			self.clock.center_y = self.height - 60
			self.add_widget(self.clock)
			self.clock.start_up(0)
	
	# After the Cancel Clock message, if the user presses Yes then this method is called to stop the clock
	def stop_clock(self):
		self.remove_widget(self.backgroundwidget)
		
		for child in self.children[:]:
			if child.id == "cancel_message":
				self.remove_widget(child)
				
		time = self.clock.stop_clock()
		f.write("Poster creation stage duration: " + time + "\n")
		f.write("Number of notes created by user: " + str(self.number_of_notes) + " (this is not the number of notes used in the poster)\n")
		
		print "Im just before setup"
		self.setup()
		
	# Call this function when the clock is tapped to ask the user if they want to stop the clock
	def cancel_clock(self):
	
		# Add the black see through background
		self.backgroundwidget.size_hint = (None, None)
		self.backgroundwidget.size = (self.parent.width, self.parent.height)
		self.backgroundwidget.pos = (0, 0)
		self.add_widget(self.backgroundwidget)
		
		# Add the message widget
		cancel_message = MessageClock(id = "cancel_message")
		cancel_message.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		cancel_message.rotation = 0
		self.add_widget(cancel_message)
	
	# If user decides not to stop the clock then resume from where the clock stopped
	def resume_clock(self):
		for child in self.children[:]:
			if child.id == "cancel_message":
				self.remove_widget(child)
				
		self.remove_widget(self.backgroundwidget)
				
		self.clock.resume_up()
			
	def callback_note(self, instance):
		
		self.number_of_notes[instance.user - 1] += 1
		
		note = Note()
		note.text = "Write something"
		
		if (numberOfUsers == 2 and instance.user == 1) or (numberOfUsers in [3, 4] and instance.user == 2) or (numberOfUsers in [5, 6] and instance.user in [2, 3]):
			note.center_x = imageScrollerLocation2[instance.user - 1][0]
			note.center_y = imageScrollerLocation2[instance.user - 1][1] + 200
		elif (numberOfUsers == 2 and instance.user == 2) or (numberOfUsers == 4 and instance.user == 4) or (numberOfUsers == 5 and instance.user == 5) or (numberOfUsers == 6 and instance.user in [5, 6]):
			note.center_x = imageScrollerLocation2[instance.user - 1][0]
			note.center_y = imageScrollerLocation2[instance.user - 1][1] - 200
		elif (instance.user == 1):
			note.center_x = imageScrollerLocation2[instance.user - 1][0] + 200
			note.center_y = imageScrollerLocation2[instance.user - 1][1]
		elif (numberOfUsers in [3, 4] and instance.user == 3) or (numberOfUsers in [5, 6] and instance.user == 4):
			note.center_x = imageScrollerLocation2[instance.user - 1][0] - 200
			note.center_y = imageScrollerLocation2[instance.user - 1][1]
			
		note.rotation = userLocation2[instance.user - 1][2]

		# Figure out if we have colour code on/off
		group = ToggleButton.get_widgets('colour')

		# In what format to send the options to the main program????
		colour_code_on = False
		for x in group:
			if x.text == 'Yes' and x.state == 'down':
				colour_code_on = True

		if colour_code_on:
			note.colour = userColours[instance.user - 1]
			note.border_colour = userColours[instance.user - 1]
		else:
			anonymous_color = json.loads(Config.get('options', 'anonymous_color'))

			note.colour = anonymous_color
			note.border_colour = anonymous_color
			note.text_colour = [0, 0, 0, 1]

		note.keyboard_can_link_to = True
		self.add_widget(note)
		
	def callback_keyboard(self, instance):
		print "Keyboard " + str(instance.user)
		
		# Has the keyboard already been added for this user?
		found = False

		mykeyboard = None

		for child in self.children[:]:
			if (self.scripting is False) and (child.id == "Keyboard " + str(instance.user)):
				found = True
				mykeyboard = child
			if self.scripting:
				if (self.stage3options['keyboard'] is True):
					if child.id != None and (child.id.split(' ')[0] == 'Keyboard'):
						found = True
						mykeyboard = child
				elif child.id == "Keyboard " + str(instance.user):
					found = True
					mykeyboard = child

		'''for child in self.children[:]:
			if child.id == "Keyboard " + str(instance.user):
				# fix from ajc:
				# remember to disconnect any attached item, solves weird line artefact bug
				child.disconnect_linked_object_from_keyboard()

				self.remove_widget(child)
				found = True'''
		
		if found == False: 
			mykeyboard = PosterKeyboard(size_hint_x = None, size_hint_y=None)
			#mykeyboard.pos = (100, 280)

			mykeyboard.set_colour((0.8,0.8,0.8))
			self.add_widget(mykeyboard)

			mykeyboard.scale = 0.001
			mykeyboard.center = Window.size[0]/2, Window.size[1]/2

		# guard against no keyboard found (this should never happen I think?)
		if mykeyboard is None:
			return

		Animation(scale = 1, d=0.5, t='in_out_cubic').start(mykeyboard)

		if (numberOfUsers == 2 and instance.user == 1) or (numberOfUsers in [3, 4] and instance.user == 2) or (numberOfUsers in [5, 6] and instance.user in [2, 3]):
			x, y = imageScrollerLocation2[instance.user - 1][0], imageScrollerLocation2[instance.user - 1][1]
			Animation(center=(x,y), d=0.5, t='in_out_cubic').start(mykeyboard)
		elif (numberOfUsers == 2 and instance.user == 2) or (numberOfUsers == 4 and instance.user == 4) or (numberOfUsers == 5 and instance.user == 5) or (numberOfUsers == 6 and instance.user in [5, 6]):
			x, y = imageScrollerLocation2[instance.user - 1][0], imageScrollerLocation2[instance.user - 1][1]
			Animation(center=(x,y), d=0.5, t='in_out_cubic').start(mykeyboard)
		elif (instance.user == 1):
			x, y = imageScrollerLocation2[instance.user - 1][0], imageScrollerLocation2[instance.user - 1][1]
			Animation(center=(x,y), d=0.5, t='in_out_cubic').start(mykeyboard)
		elif (numberOfUsers in [3, 4] and instance.user == 3) or (numberOfUsers in [5, 6] and instance.user == 4):
			x, y = imageScrollerLocation2[instance.user - 1][0], imageScrollerLocation2[instance.user - 1][1]
			Animation(center=(x,y), d=0.5, t='in_out_cubic').start(mykeyboard)


		mykeyboard.id = "Keyboard " + str(instance.user)

		Animation(rotation = imageScrollerLocation2[instance.user - 1][2], d=0.5, t='in_out_cubic').start(mykeyboard)
		#mykeyboard.rotation = imageScrollerLocation2[instance.user - 1][2]

		if self.scripting is False or (self.scripting and self.stage1options['colour']):
			r,g,b = userColours[instance.user - 1][0], userColours[instance.user - 1][1], userColours[instance.user - 1][2]
			extra = 0.2 # compensate for how set_color does things
			r = max(0, r+extra)
			g = max(0, g+extra)
			b = max(0, b+extra)
			mykeyboard.set_colour((r,g,b))
		else:
			mykeyboard.set_colour((0.8,0.8,0.8)) # grey

	'''def on_touch_down(self, touch):
		if self.disable_touch:
			return True
		else:
			handled = super(MainWidget, self).on_touch_down(touch)'''
			
	'''def set_disable(self, disable):
		pass'''
		#self.disable_touch = disable
		

class MainApp(App):

	def doscreenshot(self, dt, *largs):
		#Window.screenshot(name='screenshot%(counter)04d.jpg')
		pass
	
	def build(self):
		# Create a listener for the incoming filenames from the phone
		reactor.listenTCP(7894, TCPServerFactoryWithRoot(self, FilenameReceiverServer))

		Clock.schedule_interval(self.doscreenshot, 5)
		return MainWidget()
	
	def on_stop(self):
		timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		f.write("\nFinished at: " + timestamp + "\n")
		
if __name__ == '__main__':
    MainApp().run()