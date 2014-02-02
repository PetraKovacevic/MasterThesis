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

class SelectionTransferWidget(Widget):
	
	stage_duration = NumericProperty(1)
	page = NumericProperty(1)
	title = StringProperty()
	body = StringProperty()
		
	def submit_button(self):
		print "I'm in SelectionTransferWidget"
		name = 'sharing'
		option = False
		sharing_group = ToggleButton.get_widgets('sharing')
		
		# In what format to send the options to the main program????
		for x in sharing_group:
			if x.text == '(1)' and x.state == 'down':
				option = True
		
		print option
		app = App.get_running_app().root
		app.set_options(name, option)
		print "I'm going to set_option"

class SelectionApp(App):
	def build(self):
		return SelectionWidget()
		
if __name__ == '__main__':
    SelectionApp().run()