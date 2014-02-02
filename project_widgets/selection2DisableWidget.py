import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

class Selection2DisableWidget(Widget):
	
	stage_duration = NumericProperty(1)
	page = NumericProperty(1)
	title = StringProperty()
	body = StringProperty()
		
	def submit_button(self):
	
		name = 'disable'
		option = False
		group = ToggleButton.get_widgets('disable')
		
		# In what format to send the options to the main program????
		for x in group:
			if x.text == 'Enable' and x.state == 'down':
				option = True
				#option = False
				
		app = App.get_running_app().root
		app.set_options(name, option)
		
class Selection2DisableWidgetApp(App):
	def build(self):
		return Selection2DisableWidget()
		
if __name__ == '__main__':
    Selection2DisableWidgetApp().run()