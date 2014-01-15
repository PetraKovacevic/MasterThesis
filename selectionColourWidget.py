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

class SelectionColourWidget(Widget):
	
	stage_duration = NumericProperty(1)
	page = NumericProperty(1)
	title = StringProperty()
	body = StringProperty()
		
	def submit_button(self):
	
		name = 'colour'
		option = False
		group = ToggleButton.get_widgets('colour')
		
		# In what format to send the options to the main program????
		for x in group:
			if x.text == 'Yes' and x.state == 'down':
				option = True
				
		app = App.get_running_app().root
		app.set_options(name, option)

class SelectionColourWidgetApp(App):
	def build(self):
		return SelectionColourWidget()
		
if __name__ == '__main__':
    SelectionColourWidgetApp().run()