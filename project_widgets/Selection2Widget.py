import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty

class Selection2Widget(Widget):
	
	stage_duration = NumericProperty(5)
		
	def submit_button(self):
				
		app = App.get_running_app().root
		app.call_stage2options()
