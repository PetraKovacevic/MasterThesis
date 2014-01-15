import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty
from selectionTransferWidget import SelectionTransferWidget

class ChooseWidget(Widget):
	
	numberOfUsers = NumericProperty(3)

	# this is a confusing function name
	def reduce_num(self):
		if self.numberOfUsers > 2: # your thing crashes on 1 user, so changing this :)
			self.numberOfUsers = self.numberOfUsers - 1
			
	def add_num(self):
		if self.numberOfUsers < 6:
			self.numberOfUsers = self.numberOfUsers + 1
		
	def choose_button(self):
				
		app = App.get_running_app().root
		#app.add_widget(SelectionTransferWidget(pos = (0, 0), id = '1'))
		
		name = 'scripting'
		option = False
		group = ToggleButton.get_widgets('scripting')
		
		# In what format to send the options to the main program????
		for x in group:
			if x.text == 'Yes' and x.state == 'down':
				option = True
				
		user_study = 1
		group = ToggleButton.get_widgets('user_study')
		
		# In what format to send the options to the main program????
		for x in group:
			if x.text == '2' and x.state == 'down':
				user_study = 2
				
		app.start(self.numberOfUsers, option, user_study)