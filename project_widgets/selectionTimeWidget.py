import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

class SelectionTimeWidget(Widget):
	
	# If the stage is 1 (1st stage: Transfer) then the time is added or reduced by 0.5. If the stage is 2 then it's reduced or added by 1.
	
	stage_duration = NumericProperty(1)
	stage = NumericProperty(1)

	def reduce_time(self):
		if self.stage == 1:
			if self.stage_duration > 0.5:
				self.stage_duration = self.stage_duration - 0.5
		else:
			if self.stage_duration > 1:
				self.stage_duration = self.stage_duration - 1
			
	def add_time(self):
		if self.stage == 1:
			if self.stage_duration < 10:
				self.stage_duration = self.stage_duration + 0.5
		else:
			if self.stage_duration < 20:
				self.stage_duration = self.stage_duration + 1
		
	def submit_button(self):
		name = 'time'		
		app = App.get_running_app().root
		app.set_options(name, self.stage_duration, self.stage)