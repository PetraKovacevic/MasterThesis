import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty

class Selection1Widget(Widget):
	
	stage_duration = NumericProperty(1)

	def reduce_time(self):
		if self.stage_duration > 0.5:
			self.stage_duration = self.stage_duration - 0.5
			
	def add_time(self):
		if self.stage_duration < 2:
			self.stage_duration = self.stage_duration + 0.5
		
	def submit_button(self):
	
		options = {'disable': False, 'colour': False, 'sharing': False}
		
		disable_group = ToggleButton.get_widgets('disable')
		colour_group = ToggleButton.get_widgets('colour')
		sharing_group = ToggleButton.get_widgets('sharing')
		
		# In what format to send the options to the main program????
		for x in disable_group:
			if x.text == 'Yes' and x.state == 'down':
				options['disable'] = True
				print x.text + " " + x.state
			
		for x in colour_group:
			if x.text == 'Yes' and x.state == 'down':
				options['colour'] = True
				print x.text + " " + x.state
				
		for x in sharing_group:
			if x.text == '(1)' and x.state == 'down':
				options['sharing'] = True
				print x.text + " " + x.state
				
		app = App.get_running_app().root
		app.call_stage1(options, self.stage_duration)

class Selection1App(App):
	def build(self):
		return Selection1Widget()
		
if __name__ == '__main__':
    Selection1App().run()