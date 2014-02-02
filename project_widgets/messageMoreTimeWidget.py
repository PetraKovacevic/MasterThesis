import kivy
kivy.require('1.6.0')

#Imports
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.scatter import Scatter

class MessageMoreTimeWidget(Scatter):
	
	def on_yes_button(self):
		print "Calling yes_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		#app = self.parent
		#app.yes_pressed()
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.yes_pressed()
				
		
		
	def on_no_button(self):
		print "Calling yes_button!!!!!!!!!!!!"
		#app = App.get_running_app().root
		
		#app = self.parent
		#app.no_pressed()
		
		for child in self.parent.children:
			if child.id == "idForRemoving":
				child.no_pressed()