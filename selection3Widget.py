import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty

class Selection3Widget(Widget):
	
	stage_duration = NumericProperty(5)
		
	def submit_button(self):
				
		app = App.get_running_app().root
		app.call_stage3options()

class Selection3WidgetApp(App):
	def build(self):
		return Selection3Widget()
		
if __name__ == '__main__':
    Selection3WidgetApp().run()