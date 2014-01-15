import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock

class ClockWidget(Widget):
	minutes = StringProperty("00")
	seconds = StringProperty("00")
	
	angle = NumericProperty(90)
	
	call_function = None

	def __init__(self, **kwargs):
		# make sure we aren't overriding any important functionality
		super(ClockWidget, self).__init__(**kwargs)
		
	def start(self, num):
		# calculate the minutes and seconds to display on clock
		min = num/60
		self.minutes = str(min).zfill(2)
		
		sec = num - min*60
		self.seconds = str(sec).zfill(2)
		
		self.time = num - 1
		
		Clock.schedule_interval(self.countdown, 1)
		
	def start_up(self, num):
		# calculate the minutes and seconds to display on clock
		min = num/60
		self.minutes = str(min).zfill(2)
		
		sec = num - min*60
		self.seconds = str(sec).zfill(2)
		
		self.time = num + 1
		
		Clock.schedule_interval(self.countup, 1)
		
	def cancel_clock(self):
		Clock.unschedule(self.countdown)
		Clock.unschedule(self.countup)
		
		self.parent.cancel_clock()
		print "I'm in cancel clock"
		
	def resume(self):
		Clock.schedule_interval(self.countdown, 1)
	
	def resume_up(self):
		Clock.schedule_interval(self.countup, 1)
		
	def stop_clock(self):
		time = self.minutes + ":" + self.seconds
		
		Clock.unschedule(self.countdown)
		Clock.unschedule(self.countup)
		
		return time
		
	def call_need_more_time(self):
		func = self.call_function
		if (func != None):
			self.call_function()
		
	# Countdown method 
	# num is time in seconds
	def countdown(self, dt):
		# calculate the minutes and seconds to display on clock
		min = self.time/60
		self.minutes = str(min).zfill(2)
		
		sec = self.time - min*60
		self.seconds = str(sec).zfill(2)
		
		self.time = self.time - 1
		
		if (self.time < 0):
			self.stop_clock()
			self.call_need_more_time()
		
		# if the time is more than 0 then call countdown again
		# else let the main program now the clock has finished
		'''if num > 0:
			Clock.schedule_once(lambda dt: self.countdown(num - 1), 1)
		elif (num == 0):
			func = self.call_function
			if (func != None):
				#app = self.parent
				#app.func()
				
				self.call_function()'''
				
	# Countdown method 
	# num is time in seconds
	def countup(self, dt):
		# calculate the minutes and seconds to display on clock
		min = self.time/60
		self.minutes = str(min).zfill(2)
		
		sec = self.time - min*60
		self.seconds = str(sec).zfill(2)
		
		self.time = self.time + 1